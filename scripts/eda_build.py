"""Stage immutable Verilator inputs into a build path GNU Make can handle."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


def build_verilator(root, out, execute):
    scratch_parent = Path('/private/tmp') if Path('/private/tmp').is_dir() else Path(tempfile.gettempdir())
    stage = Path(tempfile.mkdtemp(prefix='coms6998-eda-', dir=scratch_parent))
    if any(char.isspace() for char in str(stage)):
        raise ValueError('Verilator requires a temporary build directory without whitespace')
    sources = [
        'examples/arbiter/rtl/fixed_priority_arbiter.sv',
        'examples/arbiter/verif/tb_fixed_priority_arbiter.sv',
        'scripts/sim_main.cpp']
    manifest = {'workspace': str(root), 'build_directory': str(stage), 'sources': {}}
    for relative in sources:
        original = root / relative
        copied = stage / relative
        copied.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, copied)
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        if hashlib.sha256(copied.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Build source changed during staging: {relative}')
        manifest['sources'][relative] = digest
    (out / 'build-inputs.json').write_text(json.dumps(manifest, indent=2) + '\n')
    seconds, _ = execute([
        'verilator', '--cc', '--exe', '--build', '--timing', '--assert',
        '--coverage-line', '--coverage-toggle', '--coverage-expr',
        '--top-module', 'tb_fixed_priority_arbiter', '--Mdir', 'obj_dir', '-j', '2',
        *sources], out / 'compile.log', cwd=stage)
    return stage / 'obj_dir/Vtb_fixed_priority_arbiter', seconds
