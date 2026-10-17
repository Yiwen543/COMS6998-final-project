#!/usr/bin/env python3
"""Real multi-module CVDP EDA validation, with deterministic C/D witness controls."""
import argparse
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from agent_core import ast_text, dump, feedback, simplify
from coverage import join
from cvdp_modules import (NAMES, candidates, environment, expanded_suite, initial,
                          targets, source, FIELDS)
from cvdp_simulator import CVDPSimulator
from predicates import ROOT, parse, evaluate
from run_step1 import run


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def point_ids(points, hit_only=False):
    return {(p['source'], p['line'], p['column'], p['type'], p['outcome'])
            for p in points if not hit_only or p['hits'] > 0}


def validate_representatives(name, ts, graph):
    roots = {t['id']: t for t in graph['targets']}
    checked = 0
    domain = candidates(name)
    for t in ts:
        raw = parse(t['compact'])
        c = parse(roots[t['id']]['representative'])
        d = simplify(raw)
        for v in domain:
            env = environment(name, v)
            if evaluate(raw, env) != evaluate(c, env) or evaluate(raw, env) != evaluate(d, env):
                raise ValueError(f'Semantic mismatch: {name}/{t["id"]}')
            checked += 1
    return {'checked_target_input_pairs': checked, 'candidate_inputs': len(domain),
            'scope': 'complete guard-variable projection for these reviewed adapters; not full temporal verification'}


def witnesses(name, ts, graph, points, group):
    roots = {t['id']: t for t in graph['targets']}
    added, seen, decisions = [], set(), []
    for t in join(ts, graph, points):
        if not t['uncovered']:
            continue
        expr = parse(roots[t['id']]['representative']) if group == 'C' else simplify(parse(t['compact']))
        witness = next((v for v in candidates(name) if evaluate(expr, environment(name, v))), None)
        decisions.append({'id': t['id'], 'expression': ast_text(expr), 'witness': witness,
                          'no_witness_scope': None if witness else 'exhaustive guard projection; raw counter retained'})
        if witness is not None:
            key = tuple(witness.values())
            if key not in seen:
                seen.add(key)
                added.append(witness)
    return added, decisions


def run_module(name, out):
    out.mkdir()
    started = time.perf_counter()
    ts = targets(name)
    dump(out / 'predicates.json', ts)
    start = time.perf_counter()
    proc = subprocess.run([str(ROOT / 'egraph/target/debug/rtl-predicate-egraph')],
                          input=json.dumps(ts), text=True, capture_output=True, check=True, timeout=20)
    graph = json.loads(proc.stdout)
    egg_seconds = time.perf_counter() - start
    dump(out / 'egraph.json', graph)
    semantic_check = validate_representatives(name, ts, graph)
    sim = CVDPSimulator(name, out)
    baseline = initial(name)
    measured = sim.simulate(baseline, out / 'initial', crosscheck=True)
    # Joining is a checked source map, not a coverage-point inference from semantics.
    join(ts, graph, measured['points'])
    universe = point_ids(measured['points'])
    arms, previews, suites = {}, {}, {}
    for group in 'BCD':
        start = time.perf_counter()
        fb = feedback(group, ts, graph if group == 'C' else None, measured['points'])
        elapsed = time.perf_counter() - start
        preview = {
            'module': name, 'rtl': (ROOT / source(name)).read_text(),
            'task_context': json.loads((ROOT / 'examples/cvdp' / name / 'upstream_problem.json').read_text())['prompt'],
            'input_integer_bounds': FIELDS[name], 'predicate_atoms': ts[0]['atom_definitions'],
            'fixed_checker_initial_result': measured['checker'], 'previous_inputs': baseline,
            **fb}
        dump(out / f'{group}-feedback-preview.json', preview)
        previews[group] = preview
        if group == 'B':
            continue
        added, decisions = witnesses(name, ts, graph, measured['points'], group)
        suite = baseline + added
        suites[group] = suite
        dump(out / f'{group}-witness-decisions.json', decisions)
        current = sim.simulate(suite, out / f'{group}-refined', crosscheck=True)
        if point_ids(current['points']) != universe:
            raise ValueError('Raw counter identities changed')
        if not point_ids(measured['points'], True) <= point_ids(current['points'], True):
            raise ValueError('Replayed suite lost previous coverage')
        # Every satisfiable requested target must hit its own source counter.
        joined = {t['id']: t for t in join(ts, graph, current['points'])}
        for decision in decisions:
            if decision['witness'] is not None and joined[decision['id']]['uncovered']:
                raise ValueError(f'Predicate/source-map witness failed: {decision["id"]}')
        arms[group] = {'vectors': len(suite), 'added_vectors': len(added),
                       'suite_sha256': digest(suite), 'checker': current['checker'],
                       'coverage': current['coverage'], 'icarus_crosscheck': current['icarus_crosscheck'],
                       'feedback_encoding_seconds': elapsed,
                       'uncovered_targets': [t['id'] for t in joined.values() if t['uncovered']]}
    all_inputs = baseline + expanded_suite(name)
    extended = sim.simulate(all_inputs, out / 'expanded', crosscheck=True)
    if point_ids(extended['points']) != universe:
        raise ValueError('Expanded suite changed raw counter identities')
    record = {
        'module': name, 'provenance': sim.provenance,
        'mode': 'real-EDA-with-deterministic-witness-controls', 'live_api_calls': 0,
        'input_tokens': None, 'output_tokens': None, 'token_roi': None,
        'checker_scope': measured['checker']['scope'], 'semantic_validation': semantic_check,
        'egg_seconds': egg_seconds, 'egg_stop_reason': graph['stop_reason'],
        'verilator_build_seconds': sim.build_seconds,
        'checker_sha256': hashlib.sha256((ROOT / 'scripts/cvdp_modules.py').read_bytes()).hexdigest(),
        'initial': {k: measured[k] for k in ('checker', 'coverage', 'icarus_crosscheck')},
        'arms': arms, 'C_D_same_stimulus': suites['C'] == suites['D'],
        'C_D_same_feedback': previews['C'] == previews['D'],
        'feedback_preview_bytes': {g: len(json.dumps(p, ensure_ascii=False).encode()) for g, p in previews.items()},
        'feedback_preview_sha256': {g: digest(p) for g, p in previews.items()},
        'expanded': {k: extended[k] for k in ('checker', 'coverage', 'icarus_crosscheck')},
        'wall_seconds': time.perf_counter() - started,
        'limitation': 'No LLM/token benefit measured. Deterministic witnesses are diagnostic, not an LLM baseline. CVDP context RTL only, not official CVDP-ECov evaluation.'}
    dump(out / 'summary.json', record)
    return record


def report(records):
    lines = ['# CVDP 多模块本地 EDA 实测', '',
             '原始 RTL 不变；真实 Verilator 覆盖 + Icarus 输出交叉检查；没有调用 LLM API。', '',
             '| 模块 | 初始检查/错误 | C 补测检查/错误 | D 补测检查/错误 | 扩展检查/错误 | C/D 刺激相同 |',
             '|---|---:|---:|---:|---:|---|']
    def counts(row):
        c = row['checker']
        return f"{c['checks']}/{c['functional_errors']}"
    for r in records:
        lines.append(f"| {r['module']} | {counts(r['initial'])} | {counts(r['arms']['C'])} | {counts(r['arms']['D'])} | {counts(r['expanded'])} | {r['C_D_same_stimulus']} |")
    lines += ['', '## 原始覆盖点统计', '', '| 模块 | 阶段 | line | branch | toggle | expr |', '|---|---|---:|---:|---:|---:|']
    for r in records:
        for label, row in [('initial', r['initial']), ('C-refined', r['arms']['C']),
                           ('D-refined', r['arms']['D']), ('expanded', r['expanded'])]:
            values = [f"{row['coverage'][k]['covered']}/{row['coverage'][k]['total']}" if k in row['coverage'] else '无此类计数器'
                      for k in ('line', 'branch', 'toggle', 'expr')]
            lines.append('| ' + ' | '.join([r['module'], label, *values]) + ' |')
    lines += ['', '## 反馈机制诊断', '', '| 模块 | C/D 反馈相同 | B/C/D 预览字节数 | egg 停止原因 |',
              '|---|---|---|---|']
    for r in records:
        sizes = '/'.join(str(r['feedback_preview_bytes'][g]) for g in 'BCD')
        lines.append(f"| {r['module']} | {r['C_D_same_feedback']} | {sizes} | {r['egg_stop_reason']} |")
    lines += ['', '字节数不是 token 数。IterationLimit 表示有界搜索未完全饱和，不代表已发现全部等价关系。', '', '## 解释范围', '',
              '- 原始 CVDP 中 barrel/caesar 是 cid016 调试题输入，预期 checker 能发现错误；shift-register 是 cid004 增强题的原始输入，仅验证其现有端口功能，不测试尚未实现的增强要求。',
              '- C/D 各自从 uncovered predicate 找有限具体输入域中的第一个 witness；相同候选顺序和补测预算，未手工加入仅供 C 使用的刺激。',
              '- Caesar lower_path 在所有 8 位字符上不可达；2 位 mode 的 default 在二态输入上不可达。保留其原始覆盖分母。',
              '- 桶形移位和 Caesar 扩展集枚举全部输入组合。移位寄存器枚举全部 256 个先前状态、4 种模式、2 个方向、2 个串行输入，每次先 reset/load；parallel_in 在 load 测试中遍历 256 个值，但并未穷举所有信号的笛卡尔积，也不是任意时间序列证明。',
              '- 移位寄存器 checker 只检验稳定后时钟沿输出，不裁定同步/异步 reset 的文档差异。',
              '- 计数器 raw hits 是工具事件数，不能作为测试向量数。没有 branch 计数器的模块按 line/expr 单独报告。',
              '- 所有组原始覆盖身份不变。不能把 e-class 同类视为覆盖点已命中。',
              '- 这些结果仅检验多模块工具链与反馈机制；不支持 e-graph 的 LLM 覆盖率、token ROI 或统计显著性结论。', '']
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--modules', nargs='+', choices=NAMES, default=list(NAMES))
    p.add_argument('--output', required=True)
    a = p.parse_args()
    out = Path(a.output).resolve()
    if out.exists() and any(out.iterdir()):
        p.error('Choose a new/empty output directory')
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, CARGO_HOME=str(ROOT / '.cache/cargo'))
    run(['cargo', 'build', '--locked', '--offline', '--manifest-path', 'egraph/Cargo.toml'],
        out / 'egg-build.log', env=env)
    records = []
    for name in a.modules:
        print(f'Running immutable CVDP module: {name}', flush=True)
        records.append(run_module(name, out / name))
        dump(out / 'summary.json', {'completed_modules': records, 'live_api_calls': 0})
        (out / 'REPORT.md').write_text(report(records))
    print(out / 'REPORT.md')

if __name__ == '__main__':
    main()
