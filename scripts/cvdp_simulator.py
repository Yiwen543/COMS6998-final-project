"""Immutable, whitespace-safe EDA runner for the reviewed CVDP modules."""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from agent_core import dump
from coverage import load, summary
from cvdp_modules import FIELDS, source, verify_source, check
from predicates import ROOT
from run_step1 import run


class CVDPSimulator:
    def __init__(self, name, out):
        self.name, self.out = name, out
        self.provenance = verify_source(name)
        self.stage = Path(tempfile.mkdtemp(prefix='coms6998-cvdp-', dir='/private/tmp'))
        rtl = source(name)
        tb = f'examples/cvdp/{name}/verif/tb.sv'
        hashes = {}
        for relative in (rtl, tb):
            dst = self.stage / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dst)
            hashes[relative] = hashlib.sha256(dst.read_bytes()).hexdigest()
        cpp = (ROOT / 'scripts/sim_main.cpp').read_text().replace('Vtb_fixed_priority_arbiter', 'Vtb')
        (self.stage / 'sim_main.cpp').write_text(cpp)
        dump(out / 'build-inputs.json', {'build_directory': str(self.stage), 'sources': hashes,
                                        'driver_sha256': hashlib.sha256(cpp.encode()).hexdigest()})
        self.build_seconds, _ = run([
            'verilator', '--cc', '--exe', '--build', '--timing', '--assert', '-Wno-fatal',
            '--coverage-line', '--coverage-toggle', '--coverage-expr',
            '--top-module', 'tb', '--Mdir', 'obj_dir', '-j', '2', rtl, tb, 'sim_main.cpp'],
            out / 'compile.log', cwd=self.stage)
        run(['iverilog', '-g2012', '-s', 'tb', '-o', 'sim.vvp', rtl, tb],
            out / 'iverilog-compile.log', cwd=self.stage)

    def simulate(self, vectors, folder, crosscheck=False):
        folder.mkdir(parents=True, exist_ok=True)
        text = ''.join(' '.join(str(v[k]) for k in FIELDS[self.name]) + '\n' for v in vectors)
        (self.stage / 'vectors.txt').write_text(text)
        (folder / 'vectors.txt').write_text(text)
        seconds, log = run([self.stage / 'obj_dir/Vtb',
                            f'+verilator+coverage+file+{folder / "coverage.dat"}'],
                           folder / 'simulation.log', cwd=self.stage)
        traces = self.parse_trace(log, len(vectors))
        checked = check(self.name, vectors, traces)
        points = load(folder / 'coverage.dat', source=source(self.name))
        result = {'checker': checked, 'coverage': summary(points), 'points': points,
                  'simulation_seconds': seconds}
        if crosscheck:
            elapsed, ilog = run(['vvp', 'sim.vvp'], folder / 'icarus.log', cwd=self.stage)
            itraces = self.parse_trace(ilog, len(vectors))
            if itraces != traces:
                raise ValueError('Verilator/Icarus output mismatch')
            result['icarus_crosscheck'] = {'identical_outputs': True, 'checks': len(itraces),
                                           'simulation_seconds': elapsed}
        dump(folder / 'result.json', result)
        return result

    @staticmethod
    def parse_trace(log, count):
        rows = re.findall(r'^TRACE (\d+) (.*)$', log, flags=re.M)
        if [int(i) for i, _ in rows] != list(range(count)) or not re.search(rf'^DONE {count}$', log, re.M):
            raise ValueError('Incomplete or reordered simulation trace')
        try:
            return [[int(x) for x in values.split()] for _, values in rows]
        except ValueError:
            raise ValueError('Unknown/X/Z output in binary-input experiment') from None
