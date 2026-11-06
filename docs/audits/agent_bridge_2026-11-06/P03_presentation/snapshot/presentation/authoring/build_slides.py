from pathlib import Path
import json,html
P=Path(__file__).parent
D=json.loads((P/'chart_data.json').read_text())
O=P/'svg_output';O.mkdir(exist_ok=True)
N='#132A49';B='#245DB5';C='#008B8B';G='#5D6B7C';L='#D8E1EC';BG='#F4F7FC';W='#FFFFFF';A='#A86612'
def esc(s):return html.escape(str(s),quote=False)
def rect(x,y,w,h,fill,stroke=None,sw=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def line(x1,y1,x2,y2,color=L,sw=1):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>'
def tx(x,y,lines,size=28,color=N,bold=False,width=1100,lead=None,anchor=None):
 if isinstance(lines,str):lines=[lines]
 lead=lead or size*1.25
 a=f' text-anchor="{anchor}"' if anchor else ''
 t=f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}"'+(' font-weight="700"' if bold else '')+a+'>'
 if len(lines)==1:t+=esc(lines[0])
 else:
  for i,s in enumerate(lines):t+=f'<tspan x="{x}" y="{y+i*lead}">{esc(s)}</tspan>'
 return t+'</text>'
def group(id,body):return f'<g id="{id}">{body}</g>'
def header(n,kicker,title):
 return group('header',tx(64,55,f'COMS6998  /  {kicker.upper()}',20,B,True)+tx(64,119,title,44,N,True))
def footer(n,source):
 return group('footer',line(64,662,1216,662)+tx(64,690,source,16,G)+tx(1216,690,f'{n:02d} / 06',16,G,anchor='end'))
def save(n,name,body,role='content'):
 text=f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" font-family="Arial" data-pptx-page-role="{role}">'+rect(0,0,1280,720,W)+body+'</svg>'
 (O/f'{n:02d}_{name}.svg').write_text(text)
# P01: question, proposal and purpose.
s=rect(1004,0,276,720,BG)+rect(64,92,68,6,B)
s+=tx(64,55,'COMS6998  /  MIDTERM · NOV 6',20,B,True)
s+=group('research-question',tx(64,195,['Can semantic feedback','improve RTL verification?'],64,N,True,lead=76))
s+=group('proposal',tx(68,346,['Use verified E-graph groups to make','LLM verification feedback more actionable.'],28,N,lead=38))
for x,num,label in [(68,'01','Coverage efficiency'),(440,'02','Monitor correctness'),(836,'03','Fault detection')]:
 s+=line(x,441,x+286,441,L,2)+tx(x,482,num,28,B,True)+tx(x,524,label,28,N)
s+=group('scope',tx(68,580,'Coverage ≠ correctness. Semantic classes ≠ RTL coverage points.',20,G))
s+=tx(68,626,'Chiyu Chen  ·  Mingyuan Zheng  ·  Yiwen Chen',24,N,True)
s+=footer(1,'Proposal → prototype → controlled experiments → preliminary evidence')
save(1,'question',s,'cover')
# P02: architecture, branch and separate experiment tracks.
s=header(2,'Implementation','One tool loop, two verification tasks')
s+=tx(64,170,'Implemented prototype: Python orchestration + Rust egg + standard EDA tools',24,G)
xs=[64,360,656,952];labels=[('Frozen inputs',['Specification + RTL','Fixed task contract']),('GPT generation',['Stimulus JSON or','passive SV monitor']),('Compile + check',['Icarus / Verilator','Yosys + SMT diagnostics']),('Measured feedback',['Actual tool counters','Independent grading'])]
for i,(x,(title,details)) in enumerate(zip(xs,labels)):
 s+=rect(x,220,264,148,BG)+rect(x,220,264,5,B if i<3 else C)+tx(x+18,262,title,28,N,True)+tx(x+18,305,details,20,G,lead=28)
 if i<3:s+=line(x+264,294,x+292,294,B,2)
s+=group('semantic-branch',rect(64,395,1152,64,BG)+tx(84,435,'C adds: typed guards → restricted E-graph groups → Z3 equivalence checks',24,C,True))
s+=group('stimulus-track',tx(64,510,'TRACK S',20,B,True)+tx(250,510,'Generate stimuli; measure real RTL coverage.',28,N))
s+=group('monitor-track',tx(64,564,'TEST2',20,C,True)+tx(250,564,'Fix stimuli; generate monitors; detect hidden faults.',28,N))
s+=group('independence-limit',tx(64,615,'Claude reference ≠ GPT candidate. Two-state guard proof ≠ sequential / four-state proof.',20,G))
s+=footer(2,'Sources: workflow + experiment protocol; restricted semantics and independent reference retained')
save(2,'prototype',s)
# P03: fair comparison and isolation.
s=header(3,'Methodology','B and C differ in feedback, not the test bench')
s+=tx(64,170,'Latest test2 cohort · fixed-stimulus passive monitor generation',24,G)
for x,col,letter,title,lines in [(64,B,'B','Raw feedback',['Raw coverage + shared','development feedback']),(656,C,'C','Semantic feedback',['Everything in B + verified','E-graph guard groups'])]:
 s+=rect(x,211,560,176,BG)+rect(x,211,6,176,col)+tx(x+26,258,letter,44,col,True)+tx(x+94,256,title,28,N,True)+tx(x+94,307,lines,28,N,lead=38)
s+=group('invariants',tx(64,434,'SAME',20,B,True)+tx(185,434,'DUT · Claude checker · stimuli · gpt-6.1-sol / low',28,N)+tx(185,476,'3 sessions / arm × 6 rounds · 64k input / 8192 output caps',24,G))
s+=group('freeze',rect(64,511,1152,67,BG)+tx(88,554,'Generate 36 candidates',24,N,True)+tx(471,554,'Freeze every round',24,N,True)+tx(871,554,'Hidden grading',24,N,True)+line(377,546,437,546,B,2)+line(748,546,834,546,B,2))
s+=group('isolation-limit',tx(64,614,['No hidden faults, evaluation traces or reference code in prompts.','Equal caps ≠ equal actual tokens; no token-matched placebo in this cohort.'],20,G,lead=27))
s+=footer(3,'Preregistered configuration + prompt hashes + frozen candidates + saved grading / usage evidence')
save(3,'methodology',s)
# P04: native-ready grouped bars (fallback shapes remain the default export).
s=header(4,'Results · Stimulus generation','Queue pilot: a small, mixed efficiency signal')
s+=tx(64,169,'gpt-6-sol · 1 queue IP, 2 RTL forms · 3 sessions / arm / form · 4 rounds',24,G)
s+=tx(64,220,'Mean API tokens to reach 41/41 line/case points (thousands)',24,N,True)
q=D['queue_means'];valsB=[q['original']['B']/1000,q['variant']['B']/1000];valsC=[q['original']['C']/1000,q['variant']['C']/1000]
x0,y0,x1,y1=140,275,828,520;h=y1-y0;slot=(x1-x0)/2;cluster=slot/2.5;bw=cluster/2
meta={'name':'queue-target-cost','x':76,'y':245,'width':780,'height':330,'type':'column','grouping':'clustered','categories':['Original','Syntax variant'],'series':[{'name':'B: raw','values':valsB},{'name':'C: semantic','values':valsC}],'gap_width':150,'plot_area':{'x':x0,'y':y0,'width':x1-x0,'height':h},'show_legend':False,'axes':{'value':{'minimum':0,'maximum':80,'major_unit':20}},'style':{'colors':[B,C]}}
z=f'<g id="queue-target-cost" data-pptx-replace-with="chart"><metadata type="application/json">{esc(json.dumps(meta))}</metadata><g id="queue-target-cost-chartArea">'
for v in [0,20,40,60,80]:
 y=y1-v/80*h;z+=line(x0,y,x1,y,L)+tx(x0-18,y+7,str(v),20,G,anchor='end')
z+=f'<!-- chart-plot-area: object=queue-target-cost | {x0},{y0},{x1},{y1} -->'
for i,label in enumerate(['Original','Syntax variant']):
 center=x0+(i+.5)*slot
 for j,(v,col) in enumerate([(valsB[i],B),(valsC[i],C)]):
  x=center-cluster/2+j*bw;y=y1-v/80*h
  z+=rect(round(x,3),round(y,3),round(bw,3),round(y1-y,3),col)+tx(x+bw/2,y-12,f'{v:.1f}',24,col,True,anchor='middle')
 z+=tx(center,555,label,24,N,anchor='middle')
z+='</g></g>';s+=z
s+=rect(456,238,18,18,B)+tx(484,254,'B: raw',20,G)+rect(623,238,18,18,C)+tx(651,254,'C: semantic',20,G)
s+=line(884,245,884,563,L,2)+group('result-summary',tx(928,328,'2 / 6',64,C,True)+tx(928,375,['C earlier by 1 round','4 comparisons tied'],24,N,lead=33)+tx(928,469,['Same final coverage','in all 12 runs'],28,N,True,lead=38))
s+=group('coverage-endpoints',tx(64,603,'Final: line/case 41/41 · branch 14/14 · toggle 344/408',24,N,True)+tx(64,635,'Exploratory, not a causal result: selected guard members were already hit after round 1.',20,G))
s+=footer(4,'Source: queue_bc_gpt6sol_20261026/target_costs.csv; index-matched comparisons, not paired RNG trials')
save(4,'queue_results',s)
# P05: fixed-trace endpoint plus cost and formal scope.
s=header(5,'Results · Fixed-stimulus monitors','test2: equal final detection, higher C token cost')
s+=tx(64,170,'Latest trace_done cohort · 3 sessions / arm × 6 rounds · all 6 final monitors',24,G)
s+=tx(64,224,'Total API tokens, all 18 rounds / arm (thousands)',24,N,True)
x0,y0,x1,y1=154,270,710,450;slot=(y1-y0)/2;bh=slot/2.5
meta={'name':'monitor-token-cost','x':64,'y':246,'width':720,'height':258,'type':'bar','grouping':'clustered','categories':['B: raw','C: semantic'],'series':[{'name':'API tokens','values':[740.643,813.649],'point_colors':[B,C]}],'gap_width':150,'plot_area':{'x':x0,'y':y0,'width':x1-x0,'height':y1-y0},'show_legend':False,'axes':{'value':{'minimum':0,'maximum':900,'major_unit':300}},'style':{'colors':[B]}}
z=f'<g id="monitor-token-cost" data-pptx-replace-with="chart"><metadata type="application/json">{esc(json.dumps(meta))}</metadata><g id="monitor-token-cost-chartArea">'
for v in [0,300,600,900]:
 x=x0+v/900*(x1-x0);z+=line(x,y0-4,x,y1,L)+tx(x,y1+31,str(v),20,G,anchor='middle')
z+=f'<!-- chart-plot-area: object=monitor-token-cost | {x0},{y0},{x1},{y1} -->'
for i,(v,label,col) in enumerate([(740.643,'B',B),(813.649,'C',C)]):
 y=y0+(i+.5)*slot-bh/2;w=v/900*(x1-x0)
 z+=tx(x0-28,y+bh/2+8,label,28,col,True,anchor='end')+rect(x0,y,w,bh,col)+tx(x0+w+12,y+bh/2+7,f'{v:.1f}',24,col,True)
z+='</g></g>';s+=z
s+=group('fixed-endpoint',tx(842,284,'11 / 11',64,N,True)+tx(842,328,'observable fault types',24,N)+tx(842,377,'C: +9.86% tokens',28,C,True)+tx(842,418,['No extra final fixed-trace kills.','N10 stays in 12 raw types.'],20,G,lead=28))
s+=group('formal-disclosure',rect(64,512,1152,94,BG)+tx(84,547,'Formal: 75 PASS · 104 FAIL · 361 TIMEOUT  /  540 checks',24,N,True)+tx(84,582,'94 BMC FAIL → 20 physical alarm reproductions + 74 unreproduced / unresolved (all C)',20,A))
s+=group('secondary-limit',tx(64,637,'Secondary prefix-type union: B 3 / C 7; no same-sample oracle confirmation or 128-cycle proof.',20,G))
s+=footer(5,'Sources: live-report-v4 + acceptance-v3 + formal-disclosure-v1; P02 PASS_WITH_LIMITS (reporting scope)')
save(5,'test2_results',s)
# P06: honest conclusion and research steps.
s=header(6,'Analysis · P2 plan','Next: remove the ceiling, then test attribution')
s+=group('interpretation',tx(64,191,['A working pipeline does not yet establish','a general E-graph advantage.'],36,N,True,lead=46))
for y,num,title,detail in [(318,'01','Unsaturated temporal obligations','Use held-out cases that separate safety from finite completion.'),(414,'02','Token-matched placebo','Separate semantic value from extra feedback and token spend.'),(510,'03','Qualify formal-to-physical mapping','Resolve four-state representation limits; retain unknowns.')]:
 s+=tx(64,y,num,28,C,True)+tx(140,y,title,28,N,True)+tx(140,y+37,detail,24,G)
s+=group('planning-limits',tx(64,596,'Proposed for Nov 9 P2; R0/R1/R2 recovery comparisons remain planned.',20,G))
s+=group('feedback-request',rect(64,617,1152,32,BG)+tx(80,640,'Feedback: prioritize temporal completion, or a semantics-only ablation?',24,B,True))
s+=footer(6,'Implemented: frozen generation, independent grading, mock/replay and explicit coverage / cost evidence')
save(6,'analysis',s,'ending')
print('Authored 6 sequential, editable SVG slides.')
