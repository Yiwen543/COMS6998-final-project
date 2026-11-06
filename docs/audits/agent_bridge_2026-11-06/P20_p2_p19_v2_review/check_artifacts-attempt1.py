"""P20 read-only PDF/text/template/ZIP/data checks. No compile/render/research."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,re,subprocess,zipfile
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3];P=ROOT/'output/p2/submission-b5-p19-v2';A=ROOT/'docs/audits/p2_p19_update_2026-11-06'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(p,x):
    with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2)
anchors={'B5_P2.pdf':'8b9bba7b62d2c8490768a7e226af4c8859adc3e59344cd3b7528e111eb740075','latex/main.tex':'6c63bf2a13a1028729a4576a0efb535deca7b6fd3bf7db70dfdc8a9ce7356706','B5_P2_source.zip':'7806fd0205520ed05f834820d6c97c77375f4bb967781b0321aed1b55a08e86a','latex/figure-data.json':'519103a0e2e756a8dbe7c46c1f4f320b7e07159a77dbd30566761b9b99460900','latex/images/retest-bc.pdf':'fb87ea1a738ad77d760af305b06c583f480e8d9146646bbaad38ee7dad10fe39'}
for n,h in anchors.items():assert sha(P/n)==h,n
assert sha(A/'phase.json')=='82afd2a4f7d7493bda1cd036795a432a2e62ed0ef22117ed6afc0b4715e1f972'
assert sha(A/'snapshot-manifest.json')=='4050a339373d6eed62f39181feea88628050f80c1bf42842ce6d8240934b1551'
manifest=read(A/'snapshot-manifest.json')['files']
for n,h in manifest.items():assert sha(ROOT/n)==h,n
inputs=read(A/'inputs.json')
for n,h in inputs['protected_old_outputs'].items():assert sha(ROOT/n)==h,n
for n,h in inputs['source_hashes'].items():assert sha(ROOT/n)==h,n
commands=[]
def run(argv,name):
    r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
    assert r.returncode==0,(argv,r.stderr)
    (OWN/name).write_text(r.stdout);commands.append({'argv':argv,'exit_code':r.returncode,'stdout':name,'stderr':r.stderr})
    return r.stdout
info=run(['/opt/homebrew/bin/pdfinfo',str(P/'B5_P2.pdf')],'pdfinfo.txt');assert re.search(r'Pages:\s+2\b',info) and re.search(r'Page size:\s+612 x 792 pts',info)
text=run(['/opt/homebrew/bin/pdftotext','-layout',str(P/'B5_P2.pdf'),'-'],'PDF-text.txt')
charttext=run(['/opt/homebrew/bin/pdftotext','-layout',str(P/'latex/images/retest-bc.pdf'),'-'],'figure-text.txt')
tex=(P/'latex/main.tex').read_text();template=ROOT/'output/p2/submission-b5/official-template';official=(template/'main.tex').read_text();sections=re.findall(r'\\section\{([^}]+)\}',tex)
assert sections==re.findall(r'\\section\{([^}]+)\}',official)==['Project Goal and Updates','Method Overview','Prototype and Pilot Results','Next Steps']
assert '\\documentclass[conference,10pt,letterpaper]{IEEEtran}' in tex
assert not re.search(r'\\(?:geometry|fontsize|textwidth|textheight|baselinestretch|enlargethispage)\b',tex)
classsha='da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7'
assert sha(P/'latex/IEEEtran.cls')==sha(template/'IEEEtran.cls')==classsha
with zipfile.ZipFile(template/'coms6998-project-p2.zip') as z:
    key=next(n for n in z.namelist() if n.endswith('IEEEtran.cls'));assert hashlib.sha256(z.read(key)).hexdigest()==classsha
with zipfile.ZipFile(P/'B5_P2_source.zip') as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(names))
    for name in names:
        p=Path(name);assert not p.is_absolute() and '..' not in p.parts and not name.endswith('/')
        assert z.read(name)==(P/'latex'/name).read_bytes(),name
ziprows={'CRC_bad_member':None,'members':names,'all_source_members_byte_equal':True}
receipt=read(A/'render-v2.json');assert receipt['exit_code']==0 and receipt['pages']==['page-1.png','page-2.png']
assert sha(P/'build-v2/main.pdf')==anchors['B5_P2.pdf']
for n in ['render-v2/page-1.png','render-v2/page-2.png','latex/images/retest-bc.png']:assert (P/n).is_file()
fd=read(P/'latex/figure-data.json');prior=read(ROOT/'docs/audits/agent_bridge_2026-11-06/P19_bc_retest_execution/review.json')
assert sha(ROOT/'docs/audits/agent_bridge_2026-11-06/P19_bc_retest_execution/review.json')==fd['P19_review_sha256']=='6dfbe1c0d2540773af8f3f061d2af15eebb244c8d1d1f90726033f35418c405d'
assert sha(ROOT/fd['latest_source'])==fd['latest_source_sha256'] and sha(ROOT/'test2/results/controller-done-bc-retest-v3/ledger.json')==fd['ledger_sha256'] and sha(ROOT/'test2/results/controller-done-bc-retest-v3/grade/scores.json')==fd['score_sha256']
for row in fd['rows']:
    arm=row['arm'];u=prior['token_results']['by_arm'][arm];assert row['usage']==u and row['actual_tokens']==u['input_tokens']+u['output_tokens']==u['total_tokens']
    assert row['sessions']==1 and row['rounds']==3 and row['ordinary_safety_types']==9 and row['finite_case_UNATTRIBUTED_types']==2 and row['raw_union_types']==11 and row['raw_type_denominator']==12 and row['no_eligible_N10_types']==1
    assert row['input_completion_definite_pairs']==0 and row['input_completion_eligible_pairs']==10 and row['correct_controls']==18 and row['unresolved_per_round']==38
b,c=[row['actual_tokens'] for row in fd['rows']];pct=float(Fraction(c-b,b)*100);assert pct==fd['C_extra_tokens_percent'] and (b,c)==(123663,133915)
assert prior['money']['settled_upper_total_microUSD']==1569371 and prior['money']['invoice_USD'] is None
assert round(prior['resources']['parent_wall_seconds_including_cleanup'],3)==177.995 and prior['resources']['compile']==12 and prior['resources']['monitor_replays']==990 and prior['resources']['attempted_monitor_cycles']==204444
h=fd['historical_separate_cohort'];assert sha(ROOT/h['source'])==h['source_sha256'];historical=read(ROOT/h['source'])
assert historical['arm_token_totals']==h['tokens_by_arm']=={'B2_raw':740643,'C2_semantic':813649}
assert h['generation_calls']==36 and h['sessions_per_arm']==3 and h['rounds_per_session']==6 and abs(h['C_extra_tokens_percent']-float(Fraction(813649-740643,740643)*100))<1e-12
formal={k:sum(x['statuses'][k] for x in historical['formal_by_arm'].values()) for k in ['PASS','FAIL','TIMEOUT']};assert formal==h['formal_statuses']=={'PASS':75,'FAIL':104,'TIMEOUT':361} and sum(formal.values())==540
assert sum(x['witness_statuses'].get('unresolved',0) for x in historical['formal_by_arm'].values())==h['unreproduced_BMC_witnesses']==74
endpoints=historical['endpoints'];assert len(endpoints)==6
unresolved=[{'arm':x['arm'],'rep':x['repetition'],'candidate_unknown':x['candidate_unknown_pairs'],'oracle_unknown':x['oracle_unknown_pairs'],'total_unresolved':x['unresolved_pairs']} for x in endpoints]
assert sum(x['total_unresolved']==40 and x['candidate_unknown']==12 and x['oracle_unknown']==38 for x in unresolved)==1
assert all(x['total_unresolved'] in [38,40] for x in unresolved)
for term in ['123,663','133,915','8.2903%','740,643','813,649','9.8571%','0/10','N01','N10','1.569371','177.995','204,444','75 PASS','104 FAIL','361 TIMEOUT','Chiyu Chen (cc5583)','Mingyuan Zheng (mz3143)','Yiwen Chen (yc4653)','November 9, 2026, 11:59 PM ET']:assert term in text,term
assert 'combined conservative usage-' in text and 'not an actual provider invoice' in text and 'feedback/response pending' in text and 'has not been' in text and 'submitted to the course platform' in text
for term in ['11/12','123,663','133,915','+8.29%','unattributed','N10: no eligible failure']:assert term in charttext,term
log=(P/'build-v2/main.log').read_text();assert len(re.findall(r'Overfull \\hbox',log))==0
for n,h in anchors.items():assert sha(P/n)==h
for n,h in manifest.items():assert sha(ROOT/n)==h,n
head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head=='745172e194885038a29b6d788bf2954ee02830ba'
index=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest();assert index==inputs['index_entries_sha256']
write(OWN/'checks.json',{'status':'ARTIFACT_CHECKS_PASS_PENDING_REVIEW_REPORT','anchors':anchors,'producer_phase_sha256':sha(A/'phase.json'),'producer_manifest_sha256':sha(A/'snapshot-manifest.json'),'producer_report_sha256':sha(A/'report.md'),'producer_members':len(manifest),'old_outputs_checked':len(inputs['protected_old_outputs']),'core_source_bindings_checked':len(inputs['source_hashes']),'pages':2,'page_size_pt':[612,792],'official_class_sha256':classsha,'official_sections':sections,'ZIP':ziprows,'chart_percent_independent':pct,'historical_percent_independent':float(Fraction(813649-740643,740643)*100),'historical_endpoints_unknowns':unresolved,'historical_formal':formal,'overfull':0,'underfull_observed':len(re.findall(r'Underfull \\hbox',log)),'render_receipt_bound_to_actual_PDF':True,'rendered_pages_and_figure_freshly_regenerated':False,'actual_HEAD':head,'index_unchanged':True,'index_sha256':index,'commands':commands,'actual_research_API_credential_compile_render':0})
print(json.dumps({'status':'PASS','pages':2,'ZIP_members':len(names),'producer_members':len(manifest),'old_outputs':len(inputs['protected_old_outputs']),'percent':pct,'overfull':0}))
