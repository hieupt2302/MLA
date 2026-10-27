"""Budgeted host controller. All dataset training/inference runs on Colab."""
import json
import math
import re
import shlex
import shutil
import subprocess
import tarfile
import time
import zipfile
from pathlib import Path

from .budget import Budget, Colab, parse_usage
from .common import digest, now, read_json, sha256, write_json


class Controller:
    def __init__(self, config, config_path):
        self.config = config
        self.workspace = Path(__file__).resolve().parents[2]
        self.artifacts = self.workspace/'artifacts'; self.artifacts.mkdir(exist_ok=True)
        self.temporary = self.workspace/'tmp'; self.temporary.mkdir(exist_ok=True)
        self.colab = Colab()
        ledger=self.artifacts/'budget.json'
        if not ledger.exists():
            balance,rate=parse_usage(self.colab.command('usage'))
            self.budget=Budget(ledger,initial_balance=balance); self.budget.sample(balance,rate)
        else: self.budget=Budget(ledger)
        self.state_path = self.artifacts/'remote_state.json'
        self.state = read_json(self.state_path) if self.state_path.exists() else {'jobs':{},'skipped':[],'created_at':now()}
        self.config_path = Path(config_path).resolve()
        self.backup_failures = 0
        self.save()

    def save(self): write_json(self.state_path,self.state)

    def allowance(self, seconds=0, reserve=5):
        balance,rate = parse_usage(self.colab.command('usage'))
        self.budget = Budget(self.artifacts/'budget.json'); self.budget.sample(balance,rate)
        return self.budget.can_start(seconds*rate/3600,reserve,seconds,
                                     0 if reserve==0 else self.final_reserve_seconds())

    def final_test_seconds(self, extra_performance=None):
        audit_path=self.workspace/'data'/'audit.json'
        if not audit_path.exists(): return 1800
        count=read_json(audit_path)['splits']['test']['segments']
        seconds=3600  # Linear predictions, evaluation, uncached performance and export.
        for path in self.artifacts.glob('runs/*/metadata.json'):
            meta=read_json(path)
            metric=path.parent/'metrics_validation.json'
            if meta.get('family')=='llm' and not meta.get('pilot') and (path.parent/'selection.json').exists():
                seconds+=read_json(path.parent/'selection.json').get('estimated_test_seconds',0) or 0
            if meta.get('family')=='neural' and not meta.get('pilot') and metric.exists():
                speed=read_json(metric).get('performance',{}).get('examples_second')
                if speed: seconds+=count/speed
        for path in self.artifacts.glob('embeddings/*/validation.json'):
            record=read_json(path)
            seconds+=count*record['seconds']/max(1,len(record['segment_ids']))
        if extra_performance and extra_performance.get('examples_second'):
            seconds+=count/extra_performance['examples_second']
        return seconds

    def final_reserve_seconds(self, extra_performance=None):
        return max(2*3600,self.final_test_seconds(extra_performance)*1.25+900)

    def final_reserve_cu(self, extra_performance=None):
        seconds=self.final_test_seconds(extra_performance)
        rate=max(self.budget.state.get('rate_cu_hour',1),self.state.get('gpu_rate_cu_hour',0))
        return max(5,seconds*rate/3600*1.25+1)

    def epochs_that_fit(self, three_epoch_seconds, test_performance=None, other_seconds=0, other_performance=None):
        self.allowance(0)
        rate=self.budget.state['rate_cu_hour']
        reserve=self.final_reserve_cu(test_performance)
        reserve_seconds=self.final_reserve_seconds(test_performance)
        if other_performance and other_performance.get('examples_second'):
            count=read_json(self.workspace/'data'/'audit.json')['splits']['test']['segments']
            reserve+=count/other_performance['examples_second']*rate/3600*1.25
            reserve_seconds+=count/other_performance['examples_second']*1.25
        for epochs in [3,2,1]:
            seconds=three_epoch_seconds*epochs/3+other_seconds
            if self.budget.can_start(seconds*rate/3600,reserve,seconds,reserve_seconds): return epochs
        return None

    def register(self, session):
        self.budget = Budget(self.artifacts/'budget.json')
        self.budget.state['owned_sessions'] = sorted(set(self.budget.state['owned_sessions'])|{session})
        self.budget.save()

    def neural_resume_plan(self, name, three_epoch_seconds, fit_n):
        directory=self.artifacts/'runs'/name
        if not (directory/'resume.json').exists(): return None
        identity=read_json(directory/'metadata.json')['identity']
        saved=read_json(directory/'resume.json')
        argv=self.state['jobs'][name]['argv']
        assert argv[argv.index('--run')+1]==name and '--resume' in argv, 'Unknown checkpoint owner/command'
        assert int(argv[argv.index('--epochs')+1])==identity['epochs'], 'Checkpoint epoch plan changed'
        finished=saved['epoch']+saved['cursor']/fit_n
        remaining=max(0,identity['epochs']-finished)
        return {'epochs':identity['epochs'],'argv':argv,'seconds':three_epoch_seconds*remaining/3+120}

    def resume_jobs(self):
        """Observe an existing worker; never launch a duplicate on resume."""
        for name, job in list(self.state['jobs'].items()):
            if job.get('status') != 'running': continue
            session=job.get('session')
            self.budget=Budget(self.artifacts/'budget.json')
            if session not in self.budget.state['owned_sessions']:
                raise RuntimeError('Running job lacks a verified owned session: '+name)
            runtime=self.colab.command('status','-s',session,check=False)
            if 'Hardware:' not in runtime:
                job.update(status='interrupted',interrupted_at=now(),reason='Runtime disappeared; restore saved artifacts before resuming')
                self.save(); continue
            argv=job['argv']
            code=("import json,sys\nfrom pathlib import Path\n"
                  "state=json.loads(Path("+repr('/content/mla/artifacts/job_status_'+name+'.json')+").read_text())\n"
                  "if state.get('status')=='running':\n"
                  " path=Path('/proc/'+str(int(state['pid']))+'/cmdline')\n"
                  " try: command_bytes=path.read_bytes()\n"
                  " except FileNotFoundError: command_bytes=b''\n"
                  " state['worker_present']=bool(command_bytes)\n"
                  " if command_bytes:\n"
                  "  command=command_bytes.decode().rstrip('\\0').split('\\0')\n"
                  "  assert command==[sys.executable,'-u','-m','mla_exp','--config','/content/mla/config.json']+"+repr(argv)+", 'Resume worker PID/command mismatch'\n"
                  "print(json.dumps(state))")
            print('OBSERVE existing Colab job:',name,flush=True)
            while True:
                self.budget=Budget(self.artifacts/'budget.json')
                if self.budget.expired():
                    self.colab.command('stop','-s',session,check=False)
                    raise RuntimeError('CU/deadline guard stopped resumed runtime')
                try:
                    state=json.loads(self.colab.shell(session,'python -c '+shlex.quote(code)))
                except RuntimeError as error:
                    if 'Already-active SSH session (HTTP 429)' not in str(error): raise
                    print('WAIT for Colab SSH connection:',name,flush=True)
                    time.sleep(30)
                    continue
                if state.get('status')=='complete': break
                if state.get('status')!='running':
                    job.update(status='failed',error=state.get('error','Unknown worker state')); self.save()
                    if state.get('status')=='failed' and job.get('optional') and job.get('cancel_reason'):
                        self.collect(session,force=True)
                        if job.get('log'):
                            self.colab.transfer(session,job['log'],self.artifacts/'logs'/(name+'.log'))
                        self.state['skipped'].append({'job':name,'reason':job['cancel_reason']})
                        self.save()
                        break
                    raise RuntimeError('Previously running Colab job failed: '+name)
                if job.get('optional') and state.get('worker_present') and not job.get('cancel_reason'):
                    self.stop_optional_at_reserve(session,name,argv,self.final_reserve_cu())
                self.collect(session)
                if job.get('log'):
                    self.colab.transfer(session,job['log'],self.artifacts/'logs'/(name+'.log'))
                print('OBSERVING',name,'CU',self.budget.state['consumed_account_cu'],flush=True)
                time.sleep(30)
            if job.get('status')=='failed':
                continue
            self.collect(session,force=True)
            if job.get('log'):
                self.colab.transfer(session,job['log'],self.artifacts/'logs'/(name+'.log'))
            self.snapshot(session,'mla_resumed_stage_results',self.job_snapshot_paths(argv))
            job.update(status='complete',finished_at=now(),cu_end=Budget(self.artifacts/'budget.json').state['consumed_account_cu'])
            self.save()
            print('COMPLETE observed job:',name,flush=True)

    def extract(self, path, destination, preserve_completed_neural_metadata=False):
        destination = Path(destination).resolve(); destination.mkdir(parents=True,exist_ok=True)
        with tarfile.open(path) as archive:
            selected=[]
            for member in archive.getmembers():
                target = (destination/member.name).resolve()
                if not target.is_relative_to(destination) or member.issym() or member.islnk(): raise ValueError('Unsafe export member')
                if preserve_completed_neural_metadata and member.isfile() and target.name=='metadata.json' and target.exists():
                    previous=read_json(target)
                    if previous.get('family')=='neural' and 'train_segments' in previous and 'optimizer_steps' in previous:
                        incoming=json.load(archive.extractfile(member))
                        if 'train_segments' not in incoming:
                            if previous.get('identity')!=incoming.get('identity') or previous.get('encoder_revision')!=incoming.get('encoder_revision') or previous['environment']['code_digest']!=incoming['environment']['code_digest']:
                                raise ValueError('Checkpoint metadata differs from completed training identity')
                            continue
                selected.append(member)
            archive.extractall(destination,members=selected,filter='data')

    def bundle(self):
        bundle = self.temporary/'mla_code.zip'
        with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in (self.workspace/'experiments'/'mla_exp').glob('*.py'):
                archive.write(path,'mla_exp/'+path.name)
            archive.write(self.config_path,'config.json')
        write_json(self.artifacts/'code_provenance.json',{'bundle_sha256':sha256(bundle),'files':{path.name:sha256(path) for path in (self.workspace/'experiments'/'mla_exp').glob('*.py')},'at':now()})
        archive=self.artifacts/'code_bundles'/(sha256(bundle)+'.zip'); archive.parent.mkdir(exist_ok=True)
        if not archive.exists(): shutil.copyfile(bundle,archive)
        return bundle

    def restore_runtime(self, session):
        # An existing runtime may already have every durable file. Compare
        # hashes before retransmitting large models and embedding arrays.
        files=[]
        for folder in ['runs','embeddings','llm_cache']:
            source=self.artifacts/folder
            if source.exists():
                files.extend(path for path in source.rglob('*') if path.is_file() and 'checkpoints' not in path.relative_to(source).parts)
        expected={path.relative_to(self.artifacts).as_posix():sha256(path) for path in files}
        inventory=("import hashlib,json; from pathlib import Path; root=Path('/content/mla/artifacts'); "
                   "names="+repr(list(expected))+"; result={}\n"
                   "for name in names:\n"
                   " path=root/name\n"
                   " if path.is_file():\n"
                   "  h=hashlib.sha256()\n"
                   "  with path.open('rb') as stream:\n"
                   "   for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)\n"
                   "  result[name]=h.hexdigest()\n"
                   "print(json.dumps(result))")
        present=json.loads(self.colab.shell(session,'python -c '+shlex.quote(inventory),timeout=300))
        data_archive=self.artifacts/'mla_data_snapshot.tar.gz'
        remote_data=self.colab.shell(session,'sha256sum /content/mla_data_snapshot.tar.gz 2>/dev/null || true').split()
        if not remote_data or remote_data[0]!=sha256(data_archive):
            self.colab.transfer(session,'/content/mla_data_snapshot.tar.gz',data_archive,upload=True)
        restore=self.temporary/'mla_restore.tar.gz'
        def resumable_only(member):
            relative=member.name.removeprefix('artifacts/')
            if member.isfile() and relative in expected and present.get(relative)==expected[relative]: return None
            parts=Path(member.name).parts
            if len(parts)>=4 and parts[:2]==('artifacts','runs') and parts[3]=='checkpoints':
                run=parts[2]
                if run=='smoke_resume_contract' or self.state['jobs'].get(run,{}).get('status')=='complete': return None
                resume=self.artifacts/'runs'/run/'resume.json'
                if not resume.exists(): return None
                latest=Path(read_json(resume)['checkpoint']).name
                if len(parts)>4 and parts[4]!=latest: return None
            return member
        with tarfile.open(restore,'w:gz',compresslevel=1) as archive:
            for folder in ['runs','embeddings','llm_cache']:
                source=self.artifacts/folder
                if source.exists(): archive.add(source,arcname='artifacts/'+folder,filter=resumable_only)
            for source in self.artifacts.glob('*.json'):
                if source.name not in ['budget.json','remote_state.json','export_latest.json'] and not source.name.startswith('job_status_'):
                    archive.add(source,arcname='artifacts/'+source.name)
        self.colab.transfer(session,'/content/mla_restore.tar.gz',restore,upload=True)
        self.colab.shell(session,'mkdir -p /content/mla && tar -xzf /content/mla_data_snapshot.tar.gz -C /content/mla && tar -xzf /content/mla_restore.tar.gz -C /content/mla',timeout=600)
        self.colab.transfer(session,'/content/mla_code.zip',self.bundle(),upload=True)
        code="import zipfile,sys; zipfile.ZipFile('/content/mla_code.zip').extractall('/content/mla'); sys.path.insert(0,'/content/mla'); from mla_exp.data import refresh_audit; refresh_audit('/content/mla/data')"
        self.colab.shell(session,'python -c '+shlex.quote(code),timeout=120)

    def provision_gpu(self, session):
        self.register(session)
        if 'Hardware:' not in self.colab.command('status','-s',session,check=False):
            try: self.colab.command('new','-s',session,'--gpu','T4',timeout=180)
            except RuntimeError: self.colab.command('new','-s',session,'--gpu','L4',timeout=180)
        self.restore_runtime(session)
        self.install_requirements(session,neural=True)
        self.allowance(0)
        self.state['gpu_rate_cu_hour']=self.budget.state['rate_cu_hour']; self.save()

    def provision_cpu(self, session):
        self.register(session)
        status=self.colab.command('status','-s',session,check=False)
        if 'BUSY' in status: raise RuntimeError('CPU runtime already busy; refusing duplicate work')
        if 'Hardware:' not in status:
            try: self.colab.command('new','-s',session,'--high-mem',timeout=180)
            except RuntimeError: self.colab.command('new','-s',session,timeout=180)
        self.restore_runtime(session); self.install_requirements(session)
        code="import json,os; print(json.dumps({'cpus':len(os.sched_getaffinity(0)), 'ram_bytes':os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')}))"
        resources=json.loads(self.colab.shell(session,'python -c '+shlex.quote(code)))
        jobs=4 if resources['cpus']>=4 and resources['ram_bytes']>=40*1024**3 else 2 if resources['cpus']>=2 and resources['ram_bytes']>=20*1024**3 else 1
        self.state['cpu_resources']={**resources,'cv_jobs':jobs}; self.save()
        return jobs

    def install_requirements(self, session, neural=False):
        # CLI uploads only the named file. Upload/install the base first so the
        # neural file's relative -r requirements.txt reference resolves remotely.
        names=['requirements.txt']+(['requirements-neural.txt'] if neural else [])
        logs=self.artifacts/'logs'; logs.mkdir(exist_ok=True)
        expected={}
        for name in names:
            for line in (self.workspace/'experiments'/name).read_text().splitlines():
                if '==' in line:
                    package,version=line.strip().split('==',1); expected[package]=version
        probe=("import importlib.metadata as m,json; names="+repr(list(expected))+"; actual={}\n"
               "for name in names:\n"
               " try: actual[name]=m.version(name)\n"
               " except m.PackageNotFoundError: actual[name]=None\n"
               "print(json.dumps(actual))")
        actual=json.loads(self.colab.shell(session,'python -c '+shlex.quote(probe)))
        if actual==expected:
            write_json(logs/(session+'_verified_dependencies.json'),{'packages':actual,'verification':'Colab SSH; already matched pinned requirements'})
            print('Pinned dependencies already verified:',session,flush=True)
            return
        for name in names:
            if self.state.get('job_transport')=='ssh':
                remote='/content/mla/'+name
                self.colab.transfer(session,remote,self.workspace/'experiments'/name,upload=True)
                output=self.colab.shell(session,'python -m pip install --disable-pip-version-check -r '+shlex.quote(remote),timeout=900)
                (logs/(session+'_'+name+'.log')).write_text(output,encoding='utf-8')
            else:
                self.colab.command('install','-s',session,'-r','/workspace/experiments/'+name,timeout=900,
                                   log_path=logs/(session+'_'+name+'.log'))
            for line in (self.workspace/'experiments'/name).read_text().splitlines():
                if '==' in line:
                    package,version=line.strip().split('==',1); expected[package]=version
        code=("import importlib.metadata as m,json,sys; expected="+repr(expected)+
              "; actual={name:m.version(name) for name in expected}; print(json.dumps({'python':sys.executable,'packages':actual})); "
              "assert actual==expected, 'Installed versions differ from pinned requirements'")
        verified=self.colab.shell(session,'python -c '+shlex.quote(code),timeout=120)
        (logs/(session+'_verified_dependencies.json')).write_text(verified,encoding='utf-8')

    def collect(self, session, force=False):
        remote='/content/mla/artifacts/export_latest.json'
        local=self.temporary/'export_latest.json'
        try:
            available=self.colab.shell(session,'test -f '+remote+' && echo yes || true')
            if 'yes' not in available: return
            self.colab.transfer(session,remote,local)
            manifest=read_json(local); generation=manifest['generation']
            if generation == self.state.get('backup_generation'): return
            folder=self.artifacts/'remote_backups'/generation
            folder.parent.mkdir(parents=True,exist_ok=True)
            self.colab.transfer(session,'/content/mla/artifacts/exports/'+generation,folder,recursive=True)
            archive=self.temporary/(generation+'.tar.gz')
            with archive.open('wb') as output:
                for part in manifest['parts']:
                    source=folder/Path(part['path']).name
                    if sha256(source)!=part['sha256']: raise ValueError('Backup checksum mismatch')
                    with source.open('rb') as stream:
                        while block:=stream.read(1024*1024): output.write(block)
            self.extract(archive,self.artifacts,preserve_completed_neural_metadata=True)
            acknowledge="from mla_exp.backup import acknowledge; acknowledge('/content/mla/artifacts',"+repr(generation)+")"
            self.colab.shell(session,'cd /content/mla && python -c '+shlex.quote(acknowledge))
            self.state['backup_generation']=generation; self.state['backup_at']=now(); self.save()
            self.prune_verified_checkpoints(generation)
            self.backup_failures=0
            print('Durable checkpoint saved:',generation,flush=True)
        except Exception as error:
            self.backup_failures+=1
            self.state['backup_error']={'at':now(),'message':str(error)}; self.save()
            if force or self.backup_failures>=3: raise RuntimeError('Checkpoint export failed; refusing more GPU work') from error

    def prune_verified_checkpoints(self, generation):
        """Keep two verified host copies per run after a successful restore."""
        if not self.artifacts.resolve().is_relative_to(self.workspace.resolve()) or not self.temporary.resolve().is_relative_to(self.workspace.resolve()):
            raise ValueError('Checkpoint storage outside workspace')
        match=re.fullmatch(r'([A-Za-z0-9_-]+)_step_\d{8}_epoch_\d{2}_cursor_\d{8}(?:_[0-9a-f]{10})?',generation)
        if not match: raise ValueError('Unexpected checkpoint generation')
        owner=match.group(1)
        metadata=self.artifacts/'runs'/owner/'metadata.json'
        if not metadata.exists() or read_json(metadata).get('family')!='neural':
            raise ValueError('Checkpoint owner is not a verified neural run')
        backups=(self.artifacts/'remote_backups').resolve()
        current=backups/generation
        if not (current/'manifest.json').exists(): raise ValueError('Current backup manifest missing')
        candidates=[]
        for folder in backups.glob(owner+'_step_*'):
            if folder.is_symlink() or folder.resolve().parent!=backups: raise ValueError('Unexpected backup path')
            if folder.is_dir() and (folder/'manifest.json').exists():
                if not re.fullmatch(re.escape(owner)+r'_step_\d{8}_epoch_\d{2}_cursor_\d{8}(?:_[0-9a-f]{10})?',folder.name) or read_json(folder/'manifest.json').get('generation')!=folder.name:
                    raise ValueError('Unexpected completed backup generation')
                candidates.append(folder)
        previous=sorted([folder for folder in candidates if folder!=current],key=lambda p:(p.stat().st_mtime,p.name),reverse=True)
        retained=[current]+previous[:1]
        checkpoints=(self.artifacts/'runs'/owner/'checkpoints').resolve()
        removed=[]
        for folder in candidates:
            if folder in retained: continue
            target=checkpoints/folder.name[len(owner)+1:]
            if target.is_symlink() or target.resolve().parent!=checkpoints or not target.resolve().is_relative_to(self.artifacts.resolve()):
                raise ValueError('Unexpected checkpoint path')
            if target.exists(): shutil.rmtree(target)
            if not folder.resolve().is_relative_to(self.artifacts.resolve()): raise ValueError('Backup outside artifacts')
            shutil.rmtree(folder); removed.append(folder.name)
            transport=self.temporary/(folder.name+'.tar.gz')
            if transport.resolve().parent!=self.temporary.resolve() or transport.is_symlink(): raise ValueError('Unexpected transport path')
            transport.unlink(missing_ok=True)
        transport=self.temporary/(generation+'.tar.gz')
        if transport.resolve().parent!=self.temporary.resolve() or transport.is_symlink(): raise ValueError('Unexpected transport path')
        transport.unlink(missing_ok=True)
        path=self.artifacts/'checkpoint_retention.json'
        record=read_json(path) if path.exists() else {}
        record[owner]={'at':now(),'retained':[folder.name for folder in retained],'removed':removed}
        write_json(path,record)

    @staticmethod
    def job_snapshot_paths(argv):
        if argv[0]=='freeze': return ['selection.lock.json']
        if argv[0]=='report': return ['REPORT_VI.md','leaderboard.csv','performance.csv','uncached_pipeline_performance.csv','seed_stability.csv','paired_comparisons.json','lopo.csv','lopo.json','calibration_ablation.csv','encoding_performance.csv','pilot_leaderboard.csv']
        if '--run' not in argv: return None
        run=argv[argv.index('--run')+1]
        if not re.fullmatch(r'[A-Za-z0-9_-]+',run): raise ValueError('Unsafe snapshot run')
        if argv[0]=='embed':
            split=argv[argv.index('--split')+1]
            if split not in ['fit','validation','calibration','test']: raise ValueError('Unsafe snapshot split')
            return [f'embeddings/{run}/{split}.npy',f'embeddings/{run}/{split}.json']
        if argv[0] in ['predict','evaluate','benchmark']:
            split=argv[argv.index('--split')+1]
            if split not in ['validation','calibration','test']: raise ValueError('Unsafe snapshot split')
            if argv[0]=='benchmark': return [f'runs/{run}/uncached_performance_{split}.json']
            if argv[0]=='evaluate': return [f'runs/{run}/metrics_{split}.json',f'runs/{run}/error_examples.csv',f'runs/{run}/confusion.png',f'runs/{run}/reliability.png']
            return [f'runs/{run}/predictions_{split}.csv.gz',f'runs/{run}/metrics_{split}.json',f'runs/{run}/decision_scores_{split}.csv.gz',f'runs/{run}/logits_{split}.npy','llm_cache']
        return ['runs/'+run,'llm_cache']

    def snapshot(self, session, name='mla_results_snapshot', paths=None):
        remote='/content/'+name+'.tar.gz'; local=self.artifacts/(name+'.tar.gz')
        # Exclude optimizer generations and transport copies; immutable latest
        # checkpoint has already been collected by collect().
        if paths:
            for path in paths:
                if not re.fullmatch(r'(selection\.lock\.json|REPORT_VI\.md|(?:leaderboard|performance|uncached_pipeline_performance|seed_stability|lopo|calibration_ablation|encoding_performance|pilot_leaderboard)\.csv|(?:paired_comparisons|lopo)\.json|runs/[A-Za-z0-9_-]+(?:/(?:uncached_performance_(?:validation|calibration|test)\.json|metrics_(?:validation|calibration|test)\.json|predictions_(?:validation|calibration|test)\.csv\.gz|decision_scores_(?:validation|calibration|test)\.csv\.gz|logits_(?:validation|calibration|test)\.npy|error_examples\.csv|confusion\.png|reliability\.png))?|embeddings/[A-Za-z0-9_-]+/(fit|validation|calibration|test)\.(npy|json)|llm_cache)',path):
                    raise ValueError('Unsafe snapshot artifact path')
            code=("from pathlib import Path;import subprocess;root=Path('/content/mla/artifacts'); "
                  "paths="+repr(paths)+"; assert (root/paths[0]).exists(), 'Missing job artifact'; "
                  "selected=['artifacts/'+p for p in paths if (root/p).exists()]; "
                  "subprocess.run(['tar','--exclude=artifacts/runs/*/checkpoints','-czf',"+repr(remote)+
                  ",'-C','/content/mla']+selected,check=True)")
            self.colab.shell(session,'python -c '+shlex.quote(code),timeout=900)
        else:
            self.colab.shell(session,"tar --exclude=artifacts/checkpoints --exclude='artifacts/runs/*/checkpoints' --exclude=artifacts/exports --exclude=artifacts/diagnostics/deberta_smoke -czf "+remote+' -C /content/mla artifacts',timeout=900)
        self.colab.transfer(session,remote,local)
        self.extract(local,self.workspace)

    def stop_optional_at_reserve(self, session, name, argv, reserve):
        self.budget=Budget(self.artifacts/'budget.json')
        ready=self.budget.state.get('data_ready_epoch')
        time_safe=ready is None or ready+48*3600-time.time()>self.final_reserve_seconds()+300
        if self.budget.state['normal_limit_cu']-self.budget.state['consumed_account_cu']>reserve+.25 and time_safe:
            return False
        expected=['-u','-m','mla_exp','--config','/content/mla/config.json']+list(argv)
        code=("import os,signal,json;from pathlib import Path; state=json.loads(Path("+
              repr('/content/mla/artifacts/job_status_'+name+'.json')+") .read_text()); "
              "pid=state.get('pid'); stopped=False; "
              "\nif state.get('status')=='running':\n assert isinstance(pid,int) and pid>1, 'Missing worker PID'; "
              "command=(Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\\0'); "
              "assert [part.decode() for part in command[1:-1]]=="+repr(expected)+", 'Worker PID/command mismatch'; "
              "os.kill(pid,signal.SIGTERM); stopped=True\nprint(json.dumps({'stopped':stopped}))\n")
        if not json.loads(self.colab.shell(session,'python3 -c '+shlex.quote(code)))['stopped']:
            return False
        self.state['jobs'][name]['cancel_reason']='Remaining CU or time reached the final-test reserve; optional worker stopped'
        self.save()
        return True

    def job(self, session, name, argv, estimated_seconds=0, optional=False, final=False, test_performance=None):
        if self.state['jobs'].get(name,{}).get('status')=='complete': return True
        if not self.allowance(estimated_seconds, reserve=0 if final else self.final_reserve_cu(test_performance)):
            self.state['skipped'].append({'job':name,'reason':'CU/deadline estimate with 25% margin and final reserve'}); self.save()
            if optional: return False
            raise RuntimeError('Insufficient safe CU/time for required job '+name)
        script=self.workspace/'experiments'/'remote_job.py'
        code=("import os,sys,zipfile,json,subprocess\nwith zipfile.ZipFile('/content/mla_code.zip') as z: z.extractall('/content/mla')\nos.chdir('/content/mla')\nsys.path.insert(0,'/content/mla')\n"
              "for module in list(sys.modules):\n if module=='mla_exp' or module.startswith('mla_exp.'): del sys.modules[module]\n"
              "from mla_exp.common import write_json\n"
              "write_json('/content/mla/artifacts/job_status_"+name+".json',{'status':'running'})\n"
              "try:\n worker_env=os.environ.copy()\n worker_env['PYTHONUNBUFFERED']='1'\n jobs="+repr(int(argv[argv.index('--cv-jobs')+1]) if '--cv-jobs' in argv else 1)+"\n threads=max(1,min(2,len(os.sched_getaffinity(0))//jobs))\n for key in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS']: worker_env[key]=str(threads)\n worker=subprocess.Popen([sys.executable,'-u','-m','mla_exp']+"+repr(['--config','/content/mla/config.json']+list(argv))+",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=worker_env)\n write_json('/content/mla/artifacts/job_status_"+name+".json',{'status':'running','pid':worker.pid})\n for line in worker.stdout: print(line,end='',flush=True)\n if worker.wait(): raise RuntimeError('Worker exit code '+str(worker.returncode))\n"
              "except BaseException as error:\n write_json('/content/mla/artifacts/job_status_"+name+".json',{'status':'failed','error':str(error)})\n raise\n"
              "write_json('/content/mla/artifacts/job_status_"+name+".json',{'status':'complete'})\n")
        script.write_text(code,encoding='utf-8')
        log=self.artifacts/'logs'/(name+'.log'); log.parent.mkdir(exist_ok=True)
        self.state['jobs'][name]={'status':'running','session':session,'optional':optional,'final':final,'at':now(),'argv':argv,'estimate_seconds':estimated_seconds,'cu_start':self.budget.state['consumed_account_cu']}; self.save()
        print('START Colab job:',name,flush=True)
        if self.state.get('job_transport')=='ssh':
            return self.ssh_job(session,name,argv,script,log,optional,test_performance)
        with log.open('w',encoding='utf-8') as output:
            process=subprocess.Popen(self.colab.prefix+['exec','-s',session,'--timeout','43200','-f','/workspace/experiments/remote_job.py'],stdout=output,stderr=subprocess.STDOUT)
            while process.poll() is None:
                time.sleep(30)
                if self.budget.expired():
                    self.colab.command('stop','-s',session,check=False); process.wait(timeout=60)
                    raise RuntimeError('CU/deadline guard stopped experiment runtime')
                if optional and not self.state['jobs'][name].get('cancel_reason'):
                    self.stop_optional_at_reserve(session,name,argv,self.final_reserve_cu(test_performance))
                self.collect(session)
                self.budget=Budget(self.artifacts/'budget.json')
                print(f'RUNNING {name}: conservative account CU {self.budget.state["consumed_account_cu"]:.2f}/50',flush=True)
        if process.poll() is not None:
            # Verify the worker marker even when the CLI exits successfully.
            # CLI transport success alone does not prove the Python job passed.
            # A CLI observation timeout is not proof that the remote work died.
            sentinel='/content/mla/artifacts/job_status_'+name+'.json'
            observed=self.temporary/(name+'_status.json')
            self.colab.transfer(session,sentinel,observed)
            status=read_json(observed)
            while status.get('status')=='running':
                runtime=self.colab.command('status','-s',session,check=False)
                if 'Hardware:' not in runtime: raise RuntimeError('Runtime disappeared during '+name)
                self.budget=Budget(self.artifacts/'budget.json')
                if self.budget.expired(): raise RuntimeError('Budget expired while observing '+name)
                if optional and not self.state['jobs'][name].get('cancel_reason'):
                    self.stop_optional_at_reserve(session,name,argv,self.final_reserve_cu(test_performance))
                self.collect(session); time.sleep(30)
                self.colab.transfer(session,sentinel,observed); status=read_json(observed)
            if status.get('status')!='complete':
                self.state['jobs'][name]['status']='failed'; self.save()
                print(log.read_text(encoding='utf-8')[-4500:],flush=True)
                if optional:
                    self.state['skipped'].append({'job':name,'reason':self.state['jobs'][name].get('cancel_reason','Remote execution failed; see actual log'),'log':str(log)})
                    self.snapshot(session,'mla_failed_stage_results'); self.save()
                    return False
                raise RuntimeError('Colab job failed: '+name)
        self.collect(session,force=True)
        self.state['jobs'][name].update({'status':'complete','finished_at':now(),'cu_end':Budget(self.artifacts/'budget.json').state['consumed_account_cu']}); self.save()
        # A job boundary is durable even for embeddings and classical models,
        # which do not create optimizer checkpoints.
        self.snapshot(session,'mla_stage_results',self.job_snapshot_paths(argv))
        print('COMPLETE',name,flush=True)
        return True

    def ssh_job(self,session,name,argv,script,log,optional,test_performance):
        """Run the same worker on Colab, independent of the Jupyter kernel."""
        import uuid
        if not re.fullmatch(r'[A-Za-z0-9_-]+',name): raise ValueError('Unsafe job name')
        attempt=uuid.uuid4().hex[:12]
        remote_script=f'/content/mla_job_{name}_{attempt}.py'
        remote_log=f'/content/mla/artifacts/worker_logs/{name}_{attempt}.log'
        marker='/content/mla/artifacts/job_status_'+name+'.json'
        self.colab.transfer(session,remote_script,script,upload=True)
        # The launcher rejects any existing MLA worker or launcher before it
        # starts a new detached process. A lost SSH response is never retried.
        launch=("import json,os,subprocess,sys;from pathlib import Path\n"
                "for proc in Path('/proc').glob('[0-9]*'):\n"
                " try: command=(proc/'cmdline').read_bytes().decode().rstrip('\\0').split('\\0')\n"
                " except (OSError,UnicodeDecodeError): continue\n"
                " assert not ('-m' in command and 'mla_exp' in command), 'An MLA worker is already active'\n"
                " assert not any(arg.startswith('/content/mla_job_') and arg.endswith('.py') for arg in command), 'An MLA launcher is already active'\n"
                "Path("+repr(marker)+").unlink(missing_ok=True)\n"
                "target=Path("+repr(remote_log)+");target.parent.mkdir(parents=True,exist_ok=True)\n"
                "env=os.environ.copy();env['LD_LIBRARY_PATH']='/usr/lib64-nvidia';env['PYTHONUNBUFFERED']='1'\n"
                "with target.open('wb') as output:\n"
                " process=subprocess.Popen([sys.executable,'-u',"+repr(remote_script)+"],cwd='/content/mla',env=env,stdout=output,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True)\n"
                "print(json.dumps({'launcher_pid':process.pid,'script':"+repr(remote_script)+",'log':"+repr(remote_log)+"}))")
        launched=json.loads(self.colab.shell(session,'python -c '+shlex.quote(launch)))
        self.state['jobs'][name].update(transport='colab-cli-ssh',attempt=attempt,**launched); self.save()
        expected=['-u','-m','mla_exp','--config','/content/mla/config.json']+list(argv)
        inspect=("import json;from pathlib import Path\n"
                 "path=Path("+repr(marker)+")\n"
                 "if path.exists():\n"
                 " state=json.loads(path.read_text())\n"
                 " if state.get('status')=='running' and state.get('pid'):\n"
                 "  proc=Path('/proc')/str(int(state['pid']))/'cmdline'\n"
                 "  command=proc.read_bytes().decode().rstrip('\\0').split('\\0') if proc.exists() else []\n"
                 "  state['worker_present']=bool(command)\n"
                 "  if command: assert command[1:]=="+repr(expected)+", 'Worker PID/argv mismatch'\n"
                 "else:\n"
                 " proc=Path('/proc')/"+repr(str(launched['launcher_pid']))+"/'cmdline'\n"
                 " command=proc.read_bytes().decode().rstrip('\\0').split('\\0') if proc.exists() else []\n"
                 " if command: assert command[1:]==['-u',"+repr(remote_script)+"], 'Launcher PID/argv mismatch'\n"
                 " state={'status':'starting'} if command else {'status':'failed','error':'Launcher exited before creating worker marker'}\n"
                 "print(json.dumps(state))")
        while True:
            time.sleep(30)
            self.budget=Budget(self.artifacts/'budget.json')
            if self.budget.expired():
                self.colab.command('stop','-s',session,check=False)
                raise RuntimeError('CU/deadline guard stopped SSH job')
            status=json.loads(self.colab.shell(session,'python -c '+shlex.quote(inspect)))
            if status.get('status')=='complete': break
            if status.get('status')=='failed':
                self.state['jobs'][name].update(status='failed',error=status.get('error')); self.save()
                self.colab.transfer(session,remote_log,log)
                if optional:
                    self.state['skipped'].append({'job':name,'reason':'Remote SSH worker failed; see actual log','log':str(log)})
                    self.snapshot(session,'mla_failed_stage_results'); self.save(); return False
                raise RuntimeError('Colab SSH worker failed: '+name)
            if status.get('worker_present') and optional and not self.state['jobs'][name].get('cancel_reason'):
                self.stop_optional_at_reserve(session,name,argv,self.final_reserve_cu(test_performance))
            self.collect(session)
            self.colab.transfer(session,remote_log,log)
            print('RUNNING SSH',name,'CU',self.budget.state['consumed_account_cu'],flush=True)
        self.colab.transfer(session,remote_log,log)
        self.collect(session,force=True)
        self.state['jobs'][name].update(status='complete',finished_at=now(),cu_end=Budget(self.artifacts/'budget.json').state['consumed_account_cu']); self.save()
        self.snapshot(session,'mla_stage_results',self.job_snapshot_paths(argv))
        print('COMPLETE SSH',name,flush=True)
        return True

    def metric(self, session, run):
        local=self.artifacts/'runs'/run/'metrics_validation.json'
        self.colab.transfer(session,'/content/mla/artifacts/runs/'+run+'/metrics_validation.json',local)
        return read_json(local)

    def verify_embedding_cache(self, name):
        import numpy as np
        from .classical import input_signature
        from .data import load_frame
        records=[]; signature=None
        for split in ['fit','validation','calibration']:
            folder=self.artifacts/'embeddings'/name
            metadata=read_json(folder/(split+'.json'))
            array=folder/(split+'.npy'); matrix=np.load(array,mmap_mode='r')
            frame=load_frame(self.workspace/'data',split,self.config)
            if metadata['segment_ids']!=frame.segment_id.tolist() or frame.segment_id.duplicated().any():
                raise ValueError('Embedding partition coverage/order mismatch')
            if metadata['input_hashes']!=[input_signature(row,metadata['context']) for _,row in frame.iterrows()]:
                raise ValueError('Embedding input hash mismatch')
            if matrix.ndim!=2 or matrix.shape[0]!=len(frame) or sha256(array)!=metadata['array_sha256']:
                raise ValueError('Embedding shape/checksum mismatch')
            for offset in range(0,len(matrix),8192):
                if not np.isfinite(matrix[offset:offset+8192]).all(): raise ValueError('Non-finite embedding cache')
            signature=signature or metadata['model_signature']
            if signature!=metadata['model_signature']: raise ValueError('Embedding split encoder mismatch')
            records.append({'split':split,'rows':len(frame),'shape':list(matrix.shape),'model_signature':signature,'array_sha256':metadata['array_sha256']})
        write_json(self.artifacts/'embedding_cache_verified.json',{'status':'verified','run':name,'records':records,'at':now(),
                    'encoding_sha256':read_json(self.artifacts/'code_provenance.json')['files']['encoding.py']})
        print('Verified embedding cache:',name,flush=True)

    def meta(self, session, run):
        local=self.artifacts/'runs'/run/'metadata.json'
        self.colab.transfer(session,'/content/mla/artifacts/runs/'+run+'/metadata.json',local)
        return read_json(local)

    def completed_model_runs(self):
        return [path.parent.name for path in sorted(self.artifacts.glob('runs/*/metadata.json'))
                if self.state['jobs'].get(path.parent.name,{}).get('status')=='complete'
                and not read_json(path).get('pilot') and (path.parent/'metrics_validation.json').exists()]

    def test_embedding_argv(self, name):
        record=read_json(self.artifacts/'embeddings'/name/'fit.json')
        argv=['embed','--run',name,'--split','test','--encoder',record['encoder']]+(['--context'] if record['context'] else [])
        if record.get('source_run'): argv+=['--checkpoint','/content/mla/artifacts/runs/'+record['source_run']+'/best']
        return argv


def run(config,config_path,resume=False,cpu_only=False):
    c=Controller(config,config_path)
    cpu='mla-persuade-cpu'; gpu='mla-persuade-gpu'
    if resume: c.resume_jobs()
    elif any(job.get('status')=='running' for job in c.state['jobs'].values()):
        raise RuntimeError('Existing running jobs require --resume; refusing duplicate work')
    c.register(cpu)
    # Existing authorized CPU stage can be resumed without replacing its job.
    if not c.state.get('cpu_complete'):
        status=c.colab.command('status','-s',cpu,check=False)
        if 'Hardware:' not in status:
            c.colab.command('new','-s',cpu,timeout=180)
            c.install_requirements(cpu)
            if (c.artifacts/'mla_data_snapshot.tar.gz').exists():
                c.restore_runtime(cpu)
            else:
                c.colab.transfer(cpu,'/content/mla_code.zip',c.bundle(),upload=True)
                c.job(cpu,'prepare',['prepare','--download'],900)
            ledger=Budget(c.artifacts/'budget.json')
            if ledger.state.get('data_ready_epoch') is None:
                ledger.state['data_ready_epoch']=time.time(); ledger.save()
        cached=all(c.state['jobs'].get('BERT_frozen_'+split,{}).get('status')=='complete' for split in ['fit','validation','calibration'])
        pending_hybrids=[(method,name) for method,name in [('lr','H1_lr'),('svm','H2_svm')]
                         if c.state['jobs'].get(name,{}).get('status')!='complete']
        hybrid_cpu='mla-persuade-hybrid-cpu'
        if cached and not pending_hybrids and hybrid_cpu in c.budget.state['owned_sessions']:
            c.colab.command('stop','-s',hybrid_cpu,check=False)
        existing_hybrid=c.colab.command('status','-s',hybrid_cpu,check=False) if cached and pending_hybrids and not cpu_only else ''
        if ('BUSY' in status or 'Hardware:' in existing_hybrid) and cached and pending_hybrids and not cpu_only:
            # Frozen features are independent of the unfinished baseline.
            # Use a separate CPU runtime; the original baseline keeps running.
            if not c.allowance(3*3600): raise RuntimeError('Insufficient CU for independent hybrid CPU search')
            c.verify_embedding_cache('BERT_frozen')
            if 'BUSY' in c.colab.command('status','-s',hybrid_cpu,check=False):
                raise RuntimeError('Existing hybrid runtime requires observation; refusing a duplicate job')
            try:
                jobs=c.provision_cpu(hybrid_cpu)
                for method,name in pending_hybrids:
                    c.job(hybrid_cpu,name,['train','--method',method,'--run',name,'--embedding-run','BERT_frozen','--context','--cv-jobs',str(jobs)],3*3600)
                    c.metric(hybrid_cpu,name); c.meta(hybrid_cpu,name)
            finally:
                c.colab.command('stop','-s',hybrid_cpu,check=False)
        while True:
            status=c.colab.command('status','-s',cpu,check=False)
            if 'BUSY' not in status: break
            print('Waiting for existing baseline CPU job; CU',Budget(c.artifacts/'budget.json').state['consumed_account_cu'],flush=True)
            time.sleep(60)
            if Budget(c.artifacts/'budget.json').expired(): raise RuntimeError('Budget expired during CPU stage')
        c.snapshot(cpu,'mla_cpu_baseline_results')
        c.colab.transfer(cpu,'/content/mla_code.zip',c.bundle(),upload=True)
        for method,name,context in [('dummy','D0',False),('lr','C1_lr',False),('svm','C2_svm',False),('lr','C3_lr',True),('svm','C3_svm',True)]:
            if not (c.artifacts/'runs'/name/'metrics_validation.json').exists():
                c.job(cpu,name,['train','--method',method,'--run',name]+(['--context'] if context else []),3600)
    dataset=c.artifacts/'mla_data_snapshot.tar.gz'
    if not dataset.exists():
        c.colab.shell(cpu,'tar -czf /content/mla_data_snapshot.tar.gz -C /content/mla data',timeout=900)
        c.colab.transfer(cpu,'/content/mla_data_snapshot.tar.gz',dataset)
    c.extract(dataset,c.workspace)
    if not c.state.get('cpu_complete'):
        c.colab.transfer(cpu,'/content/mla_code.zip',c.bundle(),upload=True)
        c.job(cpu,'audit_description',['audit-summary'],60)
        c.colab.transfer(cpu,'/content/mla/data/audit.json',c.workspace/'data'/'audit.json')
        shutil.copyfile(c.workspace/'data'/'audit.json',c.artifacts/'audit.json')
        c.job(cpu,'LOPO_development',['lopo'],3600,optional=True)
        c.snapshot(cpu,'mla_cpu_results')
        for name in ['D0','C1_lr','C2_svm','C3_lr','C3_svm']:
            if not (c.artifacts/'runs'/name/'metrics_validation.json').exists(): raise RuntimeError('CPU baseline stage incomplete: '+name)
            source_bundle=c.artifacts/'source_bundle_CPU.zip'
            if source_bundle.exists():
                metadata=read_json(c.artifacts/'runs'/name/'metadata.json')
                metadata['training_bundle_sha256']=sha256(source_bundle)
                write_json(c.artifacts/'runs'/name/'metadata.json',metadata)
        c.state['cpu_complete']=True; c.save()
    if cpu_only: return {'status':'cpu_complete'}
    c.colab.command('stop','-s',cpu)
    if not c.allowance(1800): raise RuntimeError('Insufficient CU to provision GPU')
    try:
        c.provision_gpu(gpu)
        for name in ['C1_lr','C3_lr']:
            c.job(gpu,name+'_calibration_choice',['choose-calibration','--run',name],120)
        c.job(gpu,'smoke',['smoke','--steps','100'],600)
        c.colab.transfer(gpu,'/content/mla/artifacts/gpu_smoke.json',c.artifacts/'gpu_smoke.json')
        smoke=read_json(c.artifacts/'gpu_smoke.json'); micro=smoke['seconds_microbatch']
        fit_n=read_json(c.workspace/'data'/'audit.json')['splits']['fit']['segments']
        full_seconds=micro*math.ceil(fit_n/config['batch_size'])*config['epochs']*1.25
        c.state['measured_estimate']={'full_encoder_seconds':full_seconds,'smoke':smoke}; c.save()
        for split in ['fit','validation','calibration']:
            c.job(gpu,'BERT_frozen_'+split,['embed','--run','BERT_frozen','--split',split,'--context'],full_seconds/6)
        c.verify_embedding_cache('BERT_frozen')
        # Once semantic features are cached, release the GPU while the linear
        # search runs; identical Colab CPU features/classifiers use the cache.
        hybrid=[]
        missing=[(method,name) for method,name in [('lr','H1_lr'),('svm','H2_svm')]
                 if c.state['jobs'].get(name,{}).get('status')!='complete']
        if missing:
            c.colab.command('stop','-s',gpu)
            cv_jobs=c.provision_cpu(cpu)
            for method,name in missing:
                c.job(cpu,name,['train','--method',method,'--run',name,'--embedding-run','BERT_frozen','--context','--cv-jobs',str(cv_jobs)],3*3600)
                c.metric(cpu,name); c.meta(cpu,name)
            c.colab.command('stop','-s',cpu)
            c.provision_gpu(gpu)
        for name in ['H1_lr','H2_svm']:
            if not (c.artifacts/'runs'/name/'metrics_validation.json').exists(): raise RuntimeError('Hybrid stage incomplete: '+name)
            hybrid.append(name)
        pilots=[]
        for architecture,encoder,lrs in [('bert','google-bert/bert-base-uncased',[2e-5,3e-5]),('deberta','microsoft/deberta-v3-base',[1e-5,2e-5])]:
            for lr in lrs:
                for balanced in [False,True]:
                    name=f'pilot_{architecture}_{lr:g}_{int(balanced)}'.replace('.','p').replace('-','m')
                    argv=['train','--method','neural','--run',name,'--encoder',encoder,'--lr',str(lr),'--context','--pilot']+(['--balanced'] if balanced else [])
                    if c.job(gpu,name,argv,full_seconds/20,optional=True):
                        pilots.append((architecture,encoder,lr,balanced,name,c.metric(gpu,name)))
        neural=[]; full_plans=[]
        for architecture in ['bert','deberta']:
            choices=[p for p in pilots if p[0]==architecture]
            if not choices: continue
            best=max(choices,key=lambda p:p[5]['macro_f1'])
            pilot_meta=c.meta(gpu,best[4])
            measured_three=pilot_meta['train_seconds']*fit_n/max(1,pilot_meta.get('train_segments',fit_n/10))*3
            full_plans.append((best,measured_three))
        full_plans.sort(key=lambda plan:plan[0][5]['macro_f1'],reverse=True)
        for index,(best,measured_three) in enumerate(full_plans):
            architecture=best[0]
            name='N1_bert_42' if architecture=='bert' else 'N2_deberta_42'
            if c.state['jobs'].get(name,{}).get('status')=='complete':
                neural.append(name); c.metric(gpu,name); c.meta(gpu,name); continue
            following=full_plans[index+1] if index+1<len(full_plans) else None
            if following and c.state['jobs'].get('N1_bert_42' if following[0][0]=='bert' else 'N2_deberta_42',{}).get('status')=='complete':
                following=None
            other_seconds=following[1]/3 if following else 0
            other_performance=following[0][5].get('performance') if following else None
            resume_plan=c.neural_resume_plan(name,measured_three,fit_n)
            selected_epochs=resume_plan['epochs'] if resume_plan else c.epochs_that_fit(measured_three,best[5].get('performance'),other_seconds,other_performance)
            if selected_epochs is None and following:
                # If one epoch of both cannot fit, favor the stronger pilot.
                selected_epochs=c.epochs_that_fit(measured_three,best[5].get('performance'))
            if selected_epochs is None:
                c.state['skipped'].append({'job':'full_'+architecture,'reason':'Even one measured epoch threatens final test reserve','estimated_three_epoch_seconds':measured_three}); c.save()
                continue
            argv=resume_plan['argv'] if resume_plan else ['train','--method','neural','--run',name,'--encoder',best[1],'--lr',str(best[2]),'--epochs',str(selected_epochs),'--context','--resume']+(['--balanced'] if best[3] else [])
            estimated_seconds=resume_plan['seconds'] if resume_plan else measured_three*selected_epochs/3
            if c.job(gpu,name,argv,estimated_seconds,optional=True,test_performance=best[5].get('performance')):
                neural.append(name); c.metric(gpu,name); c.meta(gpu,name)
        if neural:
            best_neural=max(neural,key=lambda name:read_json(c.artifacts/'runs'/name/'metrics_validation.json')['macro_f1'])
            task_source=best_neural
            meta=c.meta(gpu,best_neural); identity=meta['identity']
            if c.allowance(full_seconds/2):
                for split in ['fit','validation','calibration']:
                    c.job(gpu,'Task_embedding_'+split,['embed','--run','Task_embedding','--encoder',identity['encoder'],'--checkpoint','/content/mla/artifacts/runs/'+best_neural+'/best','--context','--split',split],full_seconds/6)
                # Task-aware linear search uses the cached embeddings on CPU.
                # Finish this core fusion comparison before optional extra seeds.
                c.colab.command('stop','-s',gpu)
                c.provision_cpu(cpu)
                for method,name in [('lr','H3_lr'),('svm','H3_svm')]:
                    if c.job(cpu,name,['train','--method',method,'--run',name,'--embedding-run','Task_embedding','--context'],3600,optional=True):
                        hybrid.append(name); c.metric(cpu,name); c.meta(cpu,name)
                c.colab.command('stop','-s',cpu)
                c.provision_gpu(gpu)
            else:
                c.state['skipped'].append({'job':'H3','reason':'Preserve final test CU before task-aware embedding and classifiers'}); c.save()
            for seed in [43,44]:
                name=best_neural.rsplit('_',1)[0]+'_'+str(seed)
                argv=['train','--method','neural','--run',name,'--encoder',identity['encoder'],'--seed',str(seed),'--lr',str(identity['lr']),'--epochs',str(identity['epochs']),'--amp-dtype',identity['amp_dtype'].removeprefix('torch.'),'--context','--resume']+(['--balanced'] if identity['balanced'] else [])
                seed_resume=c.neural_resume_plan(name,meta['train_seconds']*3/identity['epochs'],fit_n)
                if seed_resume: argv=seed_resume['argv']
                if c.job(gpu,name,argv,seed_resume['seconds'] if seed_resume else meta['train_seconds'],optional=True,test_performance=read_json(c.artifacts/'runs'/best_neural/'metrics_validation.json').get('performance')):
                    neural.append(name); c.metric(gpu,name); c.meta(gpu,name)
            best_hybrid=max(hybrid,key=lambda name:read_json(c.artifacts/'runs'/name/'metrics_validation.json')['macro_f1'])
            c.job(gpu,'E1',['train','--method','ensemble','--run','E1','--members',best_hybrid,best_neural],120)
            c.metric(gpu,'E1'); c.meta(gpu,'E1')
            same=[name for name in neural if name.rsplit('_',1)[0]==best_neural.rsplit('_',1)[0]]
            if len(same)==3:
                c.job(gpu,'Neural_seed_mean',['train','--method','ensemble','--run','Neural_seed_mean','--members']+same,120)
                neural.append('Neural_seed_mean'); c.metric(gpu,'Neural_seed_mean'); c.meta(gpu,'Neural_seed_mean')
            # Long context is conditional and must fit inside the extension
            # envelope as well as the total remaining CU.
            truncated=read_json(c.artifacts/'runs'/best_neural/'metrics_validation.json').get('truncation',{}).get('context_truncated',0)
            # Reserve the whole optional comparison: encoder, three embedding
            # partitions and both validation-selected linear classifiers.
            extension_seconds=full_seconds*3.0+full_seconds/2+2*3600
            extension_cu=extension_seconds*Budget(c.artifacts/'budget.json').state.get('rate_cu_hour',0)/3600*1.25
            if truncated>.1 and extension_cu<=config['stage_caps']['extension'] and c.allowance(extension_seconds):
                modern=['train','--method','neural','--encoder','answerdotai/ModernBERT-base','--max-length','2048','--batch-size','2','--lr','2e-5','--context','--resume']
                if c.job(gpu,'ModernBERT_pilot',modern+['--run','pilot_modern','--pilot'],extension_seconds/30,optional=True):
                    c.metric(gpu,'pilot_modern')
                    if c.job(gpu,'N3_modern_42',modern+['--run','N3_modern_42'],full_seconds*3,optional=True,test_performance=read_json(c.artifacts/'runs'/'pilot_modern'/'metrics_validation.json').get('performance')):
                        neural.append('N3_modern_42'); c.metric(gpu,'N3_modern_42'); c.meta(gpu,'N3_modern_42')
                        modern_embeddings=True
                        for split in ['fit','validation','calibration']:
                            modern_embeddings=c.job(gpu,'Modern_embedding_'+split,['embed','--run','Modern_embedding','--encoder','answerdotai/ModernBERT-base','--checkpoint','/content/mla/artifacts/runs/N3_modern_42/best','--context','--split',split],full_seconds/6,optional=True) and modern_embeddings
                        if modern_embeddings:
                            for method,name in [('lr','H3_modern_lr'),('svm','H3_modern_svm')]:
                                if c.job(gpu,name,['train','--method',method,'--run',name,'--embedding-run','Modern_embedding','--context'],3600,optional=True):
                                    hybrid.append(name); c.metric(gpu,name); c.meta(gpu,name)
                            best_hybrid=max(hybrid,key=lambda name:read_json(c.artifacts/'runs'/name/'metrics_validation.json')['macro_f1'])
                        if read_json(c.artifacts/'runs'/'N3_modern_42'/'metrics_validation.json')['macro_f1']>read_json(c.artifacts/'runs'/best_neural/'metrics_validation.json')['macro_f1']:
                            c.job(gpu,'E2_modern',['train','--method','ensemble','--run','E2_modern','--members',best_hybrid,'N3_modern_42'],120)
                            c.metric(gpu,'E2_modern'); c.meta(gpu,'E2_modern')
            else:
                c.state['skipped'].append({'job':'ModernBERT','reason':'Context-loss gate or measured extension CU/deadline envelope','context_truncated':truncated,'estimated_cu':extension_cu}); c.save()
            bert_options=[p for p in pilots if p[0]=='bert']
            if bert_options:
                bert_choice=max(bert_options,key=lambda p:p[5]['macro_f1'])
                bert_metadata=c.artifacts/'runs'/'N1_bert_42'/'metadata.json'
                ablation_epochs=read_json(bert_metadata)['identity']['epochs'] if bert_metadata.exists() else config['epochs']
                if c.job(gpu,'N1_bert_no_context',['train','--method','neural','--run','N1_bert_no_context','--encoder',bert_choice[1],'--lr',str(bert_choice[2]),'--epochs',str(ablation_epochs),'--resume']+(['--balanced'] if bert_choice[3] else []),full_seconds*ablation_epochs/config['epochs'],optional=True,test_performance=bert_choice[5].get('performance')):
                    neural.append('N1_bert_no_context'); c.metric(gpu,'N1_bert_no_context'); c.meta(gpu,'N1_bert_no_context')
        baselines=['D0','C1_lr','C2_svm','C3_lr','C3_svm']
        candidates=baselines+hybrid+neural+(['E1'] if neural else [])+(['E2_modern'] if 'E2_modern' in c.state['jobs'] and c.state['jobs']['E2_modern']['status']=='complete' else [])
        # A resume must retain completed models even when a later budget gate
        # declines to repeat their stage.
        candidates.extend(c.completed_model_runs())
        candidates=list(dict.fromkeys(candidates))
        hybrid=[name for name in candidates if read_json(c.artifacts/'runs'/name/'metadata.json')['family'].startswith('hybrid_')]
        for name in baselines: c.metric(gpu,name); c.meta(gpu,name)
        best_run=max([name for name in candidates if read_json(c.artifacts/'runs'/name/'metadata.json').get('seed',42)==42],key=lambda name:read_json(c.artifacts/'runs'/name/'metrics_validation.json')['macro_f1'])
        best_metric=read_json(c.artifacts/'runs'/best_run/'metrics_validation.json')
        linear_metrics=[read_json(c.artifacts/'runs'/name/'metrics_validation.json') for name in baselines[1:]]
        best_linear=max(max(metric['macro_f1'],metric.get('raw_classifier_metrics',{}).get('macro_f1',0)) for metric in linear_metrics)
        best_hybrid=max(read_json(c.artifacts/'runs'/name/'metrics_validation.json')['macro_f1'] for name in hybrid)
        gates=config['gates']
        if best_metric['macro_f1']<gates['macro_f1'] or best_metric['recall_at_precision_0.4']<gates['recall_at_precision'] or best_hybrid-best_linear<gates['hybrid_gain']:
            ledger=Budget(c.artifacts/'budget.json').state
            llm_test_seconds=max(0,(ledger['normal_limit_cu']-ledger['consumed_account_cu']-max(10,c.final_reserve_cu()+5))/max(.01,ledger.get('rate_cu_hour',1))*3600/1.25)
            if ledger.get('data_ready_epoch') is not None:
                time_for_llm=max(0,(ledger['data_ready_epoch']+48*3600-time.time()-c.final_reserve_seconds()-3*3600)/1.25)
                llm_test_seconds=min(llm_test_seconds,time_for_llm)
            if c.job(gpu,'L1',['train','--method','llm','--run','L1','--members',best_run,'--llm-test-budget-seconds',str(llm_test_seconds)],3*3600,optional=True):
                if not c.meta(gpu,'L1')['pilot']: candidates.append('L1')
        c.job(gpu,'freeze',['freeze','--runs']+candidates,60,final=True)
        # Test inputs may now be encoded; test labels have never selected settings.
        embeddings=sorted({read_json(c.artifacts/'runs'/name/'metadata.json')['embedding_run'] for name in candidates if read_json(c.artifacts/'runs'/name/'metadata.json').get('embedding_run')})
        for emb in embeddings:
            argv=c.test_embedding_argv(emb)
            c.job(gpu,emb+'_test',argv,full_seconds/6,final=True)
        for name in candidates:
            validation=read_json(c.artifacts/'runs'/name/'metrics_validation.json')
            speed=validation.get('performance',{}).get('examples_second',validation.get('examples_second'))
            test_seconds=read_json(c.workspace/'data'/'audit.json')['splits']['test']['segments']/speed if speed else 900
            if name=='L1': test_seconds=read_json(c.artifacts/'runs'/name/'selection.json')['estimated_test_seconds']+120
            c.job(gpu,name+'_test',['predict','--run',name,'--split','test'],test_seconds,final=True)
            c.job(gpu,name+'_evaluate',['evaluate','--run',name,'--split','test'],300,final=True)
            c.job(gpu,name+'_benchmark',['benchmark','--run',name,'--split','test'],900 if name=='L1' else 180,final=True)
        c.job(gpu,'final_report',['report'],60,final=True)
        c.snapshot(gpu)
        c.state['status']='complete'; c.state['final_runs']=candidates; c.save()
        return c.state
    finally:
        # Never stop unrelated Colab runtimes.
        pending_sessions={job.get('session') for job in c.state['jobs'].values() if job.get('status')=='running'}
        try:
            if c.state.get('status')!='complete' and gpu not in pending_sessions: c.snapshot(gpu,'mla_last_results')
        except Exception: pass
        for session in [gpu,cpu]:
            if session not in pending_sessions: c.colab.command('stop','-s',session,check=False)
        if pending_sessions:
            c.state['observation_interrupted_at']=now(); c.save()
            print('Runtime retained for unverified/running jobs; budget watchdog remains active. Resume observation before retrying.',flush=True)
        try:
            balance,rate=parse_usage(c.colab.command('usage'))
            ledger=Budget(c.artifacts/'budget.json'); ledger.sample(balance,rate)
            if c.state.get('status')=='complete':
                ledger.state['experiment_finished_at']=now(); ledger.save()
        except Exception:
            pass
        # Host CPU analysis only: recompute the written report using the final
        # CU ledger; all model predictions were produced in Colab.
        if list(c.artifacts.glob('runs/*/metrics_validation.json')):
            from .evaluation import report
            report(c.artifacts)
