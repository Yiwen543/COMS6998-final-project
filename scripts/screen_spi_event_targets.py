#!/usr/bin/env python3
"""Keep temporal event evidence separate from certified combinational source groups."""
import argparse
import json
from pathlib import Path
from coverage import load, summary
from preflight_spi_host import identity
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import SOURCE
from run_spi_host_b_development import group_status


def screen(calibration, evaluation, output):
    output.mkdir(parents=True,exist_ok=False)
    semantic_path=ROOT/'results/spi_host_semantic_validated_20261104/screen.json'
    semantic=json.loads(semantic_path.read_text())
    for name,digest in semantic['hashes'].items():
        if sha(ROOT/name)!=digest:
            raise ValueError('Legacy semantic evidence changed: '+name)
    cal=json.loads((calibration/'summary.json').read_text())
    evaluated=json.loads((evaluation/'summary.json').read_text())
    all_counts={}
    denominator=None
    for name in cal['candidate_cases']:
        points=load(calibration/name/'batch.dat',str(SOURCE.relative_to(ROOT)),include_descendants=True)
        ids={identity(p) for p in points}
        if denominator is None:denominator=ids
        if ids!=denominator or len(points)!=1299:
            raise AssertionError('Raw counter denominator drift')
        all_counts[name]={'raw_coverage':summary(points),'raw_groups':group_status(points,semantic),
            'checker':evaluated['cases']['calibration/'+name]}
    events=[e for d in all_counts.values() for e in d['checker']['events']]
    qualified=[g for g in semantic['groups'] if g['qualified_source_group']]
    result={'scope':'Offline multi-step event qualification; no new model stimulus run',
        'schema_version':1,'config_sha256':sha(ROOT/'configs/spi_host_event_screen.json'),
        'semantic_screen_sha256':sha(semantic_path),'checker_evaluation_sha256':sha(evaluation/'summary.json'),
        'qualified_combinational_groups':len(qualified),
        'qualified_nontrivial_combinational_groups':sum(g['nontrivial_egg_group'] for g in qualified),
        'all_original_counter_count':len(denominator),'cases':all_counts,
        'observed_checker_event_families':sorted({e['family'] for e in events}),
        'temporal_to_source_bindings':[],
        'binding_status':'unresolved: certified complete combinational guards do not encode the required histories; no event/source equivalence is inferred',
        'known_ceiling':'The unchanged two nontrivial combinational groups were hit in round 1 by all prior independent B repetitions. These historical outcomes are not a new B run on the new checker.',
        'ready_for_live_B':False,'ready_for_formal_abcp':False,
        'decision':'Hold: validate/adjudicate the independent checker and construct prospective source targets for the multi-step events before any fresh B model calls.',
        'caveat':'Functional event evidence is supplementary. Never pool it into line/branch/expr/toggle counters or erase failed/inconclusive cases.'}
    (output/'screen.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--calibration',type=Path,required=True)
    cli.add_argument('--evaluation',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    result=screen(args.calibration.resolve(),args.evaluation.resolve(),args.output.resolve())
    print(json.dumps({k:result[k] for k in ('observed_checker_event_families','qualified_nontrivial_combinational_groups',
        'ready_for_live_B','ready_for_formal_abcp','binding_status')},indent=2))
