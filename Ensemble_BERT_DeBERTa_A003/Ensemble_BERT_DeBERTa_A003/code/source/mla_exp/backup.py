"""Chunked immutable exports readable through the Colab Contents API."""
import io
import shutil
import tarfile
from pathlib import Path

from .common import sha256, write_json


def checkpoint_due(step, saved_step, elapsed, step_interval, seconds_interval):
    return step - saved_step >= step_interval or elapsed >= seconds_interval


class Chunks(io.RawIOBase):
    def __init__(self, root, size=32*1024*1024):
        self.root, self.size = Path(root), size
        self.root.mkdir(parents=True, exist_ok=True)
        self.file, self.cursor, self.paths = None, 0, []
    def writable(self): return True
    def write(self, data):
        data = memoryview(data); count = len(data)
        while data:
            if self.file is None:
                path = self.root / f'part_{len(self.paths):04d}.bin'
                self.paths.append(path); self.file = path.open('wb'); self.cursor = 0
            amount = min(len(data), self.size-self.cursor)
            self.file.write(data[:amount]); self.cursor += amount; data = data[amount:]
            if self.cursor == self.size:
                self.file.close(); self.file = None
        return count
    def finish(self):
        if self.file: self.file.close(); self.file = None
        return [{'path':str(path), 'sha256':sha256(path), 'bytes':path.stat().st_size} for path in self.paths]


def export(config_root, generation, paths):
    root = Path(config_root) / 'exports' / generation
    if (root/'manifest.json').exists(): return
    chunks = Chunks(root)
    with tarfile.open(fileobj=chunks, mode='w|gz', compresslevel=1) as archive:
        for path, name in paths:
            path = Path(path)
            if path.exists(): archive.add(path, arcname=name)
    manifest = {'generation':generation, 'parts':chunks.finish(), 'format':'tar.gz', 'root':str(config_root)}
    write_json(root/'manifest.json',manifest)
    write_json(Path(config_root)/'export_latest.json',manifest)


def checkpoint_export(directory, checkpoint):
    root = directory.parents[1]
    paths = [(checkpoint,f'runs/{directory.name}/checkpoints/{checkpoint.name}'),
             (directory/'best', f'runs/{directory.name}/best')]
    paths.extend((p,f'runs/{directory.name}/{p.name}') for p in directory.glob('*.json'))
    export(root, directory.name+'_'+checkpoint.name, paths)


def acknowledge(root, generation):
    """Called only after host verified and restored the immutable export."""
    root=Path(root).resolve()
    manifest=root/'exports'/generation/'manifest.json'
    from .common import read_json
    if not manifest.exists() or read_json(manifest)['generation']!=generation: raise ValueError('Unknown export generation')
    owner=generation.split('_step_',1)[0]
    exports=root/'exports'
    for folder in exports.iterdir():
        if folder.name.startswith(owner+'_step_') and folder.name<generation and folder.resolve().parent==exports:
            shutil.rmtree(folder)
    checkpoints=root/'runs'/owner/'checkpoints'
    latest=generation[len(owner)+1:]
    if checkpoints.exists():
        for folder in checkpoints.iterdir():
            if folder.name.startswith('step_') and folder.name<latest and folder.resolve().parent==checkpoints:
                shutil.rmtree(folder)
    write_json(root/'backup_ack.json',{'generation':generation})
