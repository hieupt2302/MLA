import re
import subprocess
import time
import os
from contextlib import contextmanager
from pathlib import Path

from .common import now, read_json, write_json


@contextmanager
def ledger_lock(path):
    lock = Path(str(path) + '.lck')
    deadline = time.monotonic() + 30
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if time.monotonic() > deadline:
                raise RuntimeError('CU ledger locked; refusing an unguarded job')
            time.sleep(.1)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink()


def parse_usage(output):
    balance = re.search(r"Current balance:\s*([\d.]+)\s*compute units", output)
    rate = re.search(r"Usage rate:\s*([\d.]+)/hr", output)
    if not balance or not rate:
        raise RuntimeError("Could not read authenticated Colab CU balance/rate")
    return float(balance.group(1)), float(rate.group(1))


class Colab:
    def __init__(self):
        import os
        default = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/DockerDesktop/resources/bin/docker.exe"
        import shutil
        self.docker = shutil.which("docker") or str(default)
        self.docker_prefix = [self.docker, 'exec']
        proxy_path = Path(__file__).resolve().parents[1] / 'colab_proxy.json'
        if proxy_path.exists():
            proxy = read_json(proxy_path).get('url')
            if not re.fullmatch(r'http://host\.docker\.internal:[0-9]{1,5}', proxy or ''):
                raise ValueError('Colab proxy must be a local Docker host tunnel')
            self.docker_prefix += ['-e', 'HTTPS_PROXY='+proxy, '-e', 'HTTP_PROXY='+proxy]
        self.docker_prefix += ['mla-colab-control']
        self.prefix = self.docker_prefix + ["colab", "--auth=oauth2", "--config", "/root/.config/colab-cli/mla_sessions.json"]
        self.ssh_aliases = {}

    def ssh_options(self, session):
        if not re.fullmatch(r'mla-[A-Za-z0-9_-]+',session): raise ValueError('Only named MLA runtimes are controlled')
        key = '/root/.config/colab-cli/mla_ssh'
        proxy = f'colab --auth=oauth2 --config /root/.config/colab-cli/mla_sessions.json ssh --proxy-mode -s {session} -i {key}'
        if session not in self.ssh_aliases:
            status=self.command('status','-s',session)
            endpoint=re.search(r'^\['+re.escape(session)+r'\]\s+([A-Za-z0-9_-]+)\s*\| Hardware:',status,re.MULTILINE)
            if not endpoint: raise RuntimeError('Cannot identify authenticated Colab runtime for SSH')
            self.ssh_aliases[session]='mla-'+endpoint.group(1)
        return ['-i',key,'-o','ProxyCommand='+proxy,'-o','HostKeyAlias='+self.ssh_aliases[session],'-o','StrictHostKeyChecking=accept-new']

    def ssh_run(self, args, timeout):
        # Colab permits one SSH/SCP connection. Serialize host callers; the OS
        # releases this byte-range lock if a controller exits unexpectedly.
        if os.name == 'nt':
            import msvcrt
            lock_path=Path(__file__).resolve().parents[2]/'artifacts/colab_ssh.lock'
            with lock_path.open('a+b') as lock:
                if lock.tell()==0:lock.write(b'0');lock.flush()
                deadline=time.monotonic()+timeout+30
                while True:
                    lock.seek(0)
                    try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1);break
                    except OSError:
                        if time.monotonic()>deadline:raise RuntimeError('Colab SSH operation still owned by another host caller')
                        time.sleep(.25)
                try:return self._ssh_run(args,timeout)
                finally:
                    lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)
        return self._ssh_run(args,timeout)

    def _ssh_run(self, args, timeout):
        # Colab rejects a concurrent SSH connection before running its command.
        # Retry only this rejection, never an ambiguous timeout/worker failure.
        for attempt in range(4):
            result = subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
            if not result.returncode or 'Already-active SSH session (HTTP 429)' not in result.stderr:
                return result
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
        return result

    def shell(self, session, command, timeout=120):
        args = self.docker_prefix+['ssh']+self.ssh_options(session)+['root@'+session,command]
        result = self.ssh_run(args,timeout)
        if result.returncode: raise RuntimeError('Colab SSH command failed: '+result.stderr[-1000:])
        return result.stdout

    def transfer(self, session, remote, local, upload=False, recursive=False, timeout=1800):
        workspace = Path(__file__).resolve().parents[2]
        local = Path(local).resolve()
        if not local.is_relative_to(workspace): raise ValueError('Transfer target outside experiment workspace')
        if not remote.startswith('/content/mla') or '..' in remote: raise ValueError('Unexpected remote path')
        local.parent.mkdir(parents=True,exist_ok=True)
        mounted = '/workspace/'+local.relative_to(workspace).as_posix()
        if recursive:
            if local.name != Path(remote).name: raise ValueError('Recursive transfer requires matching directory names')
            if not upload:
                mounted=mounted.rsplit('/',1)[0]+'/'
        args = self.docker_prefix+['scp','-q']+(['-r'] if recursive else [])+self.ssh_options(session)
        endpoints = ['root@'+session+':'+remote,mounted]
        if upload: endpoints.reverse()
        result = self.ssh_run(args+endpoints,timeout)
        if result.returncode: raise RuntimeError('Colab artifact transfer failed: '+result.stderr[-1000:])

    def command(self, *args, timeout=120, check=True, log_path=None):
        result = subprocess.run(self.prefix + list(args), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        if log_path:
            path=Path(log_path); path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(result.stdout+result.stderr,encoding='utf-8')
        if check and result.returncode:
            raise RuntimeError(f"Colab {args[0]} failed (exit {result.returncode}); check controller/auth/session")
        if args[0] in ['new','stop'] and '-s' in args:
            self.ssh_aliases.pop(args[args.index('-s')+1],None)
        return result.stdout + result.stderr


class Budget:
    def __init__(self, path, initial_balance=None):
        self.path = Path(path)
        if self.path.exists():
            self.state = read_json(self.path)
            self.baseline = dict(self.state)
        else:
            if initial_balance is None:
                raise ValueError("Initial account balance required")
            self.state = {"initial_balance": initial_balance, "last_balance": initial_balance, "consumed_account_cu": 0.0,
                          "limit_cu": 50.0, "normal_limit_cu": 45.0, "started_at": now(), "owned_sessions": [], "samples": [], "data_ready_epoch": None}
            self.baseline = {}
            self.save()

    def save(self):
        with ledger_lock(self.path):
            current = read_json(self.path) if self.path.exists() else {}
            for key, value in self.state.items():
                if key not in self.baseline or value != self.baseline[key]:
                    current[key] = value
            write_json(self.path, current)
            self.state, self.baseline = current, dict(current)

    def sample(self, balance, rate):
        with ledger_lock(self.path):
            state = read_json(self.path)
            state["consumed_account_cu"] += max(0, state["last_balance"] - balance)
            state["last_balance"], state["rate_cu_hour"] = balance, rate
            state["samples"].append({"at": now(), "balance": balance, "aggregate_rate": rate})
            write_json(self.path, state)
            self.state, self.baseline = state, dict(state)

    def can_start(self, estimated_cu, reserve=5, seconds=0, reserve_seconds=0):
        remaining = self.state["normal_limit_cu"] - self.state["consumed_account_cu"]
        ready = self.state.get("data_ready_epoch")
        time_ok = ready is None or time.time() + seconds * 1.25 + reserve_seconds <= ready + 48 * 3600
        return estimated_cu * 1.25 + reserve <= remaining and time_ok

    def expired(self):
        ready = self.state.get("data_ready_epoch")
        return self.state["consumed_account_cu"] >= self.state["normal_limit_cu"] or (ready is not None and time.time() >= ready + 48 * 3600)


def usage_unavailable_should_stop(state, failures, epoch=None):
    if failures < 3:return False
    from datetime import datetime
    epoch=time.time() if epoch is None else epoch
    samples=state.get('samples',[])
    if not samples:return True
    age=max(0,epoch-datetime.fromisoformat(samples[-1]['at']).timestamp())
    # Bounded read-only outage grace; no new jobs bypass fresh usage checks.
    projected=state['consumed_account_cu']+age*max(2.14,2*state.get('rate_cu_hour',0))/3600
    return age>=900 or projected>=state['normal_limit_cu']


def watchdog(path):
    colab = Colab()
    budget = Budget(path)
    failures = 0
    while True:
        # Reload the ledger: the orchestrator registers sessions/data readiness.
        budget = Budget(path)
        if budget.state.get('experiment_finished_at'):
            print('MLA experiment finished; CU ledger closed.',flush=True)
            return
        try:
            balance, rate = parse_usage(colab.command("usage", timeout=30))
            budget.sample(balance, rate)
            failures = 0
        except Exception:
            failures += 1
        if usage_unavailable_should_stop(budget.state,failures) or budget.expired():
            for session in budget.state["owned_sessions"]:
                colab.command("stop", "-s", session, check=False)
            budget.state["watchdog_stop"] = {"at": now(), "reason": "usage_unavailable" if failures else "budget_or_deadline"}
            budget.save()
            print("Stopped owned MLA sessions; CU watchdog limit/recovery reached.", flush=True)
            return
        print(f"MLA CU guard: account draw {budget.state['consumed_account_cu']:.2f}/50, aggregate rate {budget.state.get('rate_cu_hour', 0):.2f}/h", flush=True)
        time.sleep(60)
