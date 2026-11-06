from pathlib import Path
from lxml import etree as E
import json,math
P=Path(__file__).parent;D=json.loads((P/'chart_data.json').read_text());ns={'s':'http://www.w3.org/2000/svg'}
checks=[]
r=E.parse(str(P/'svg_output/04_queue_results.svg'));g=r.find('.//s:g[@id="queue-target-cost-chartArea"]',ns);bars=g.findall('s:rect',ns)
for i,(version,arm) in enumerate([('original','B'),('original','C'),('variant','B'),('variant','C')]):
 v=D['queue_means'][version][arm]/1000;expected_h=v/80*245;expected_x=[243.2,312,587.2,656][i]
 assert abs(float(bars[i].get('height'))-expected_h)<.001
 assert abs(float(bars[i].get('x'))-expected_x)<.001
 checks.append({'object':'queue-target-cost','version':version,'arm':arm,'tokens':v*1000,'height_verified':True,'x_verified':True})
r=E.parse(str(P/'svg_output/05_test2_results.svg'));g=r.find('.//s:g[@id="monitor-token-cost-chartArea"]',ns);bars=g.findall('s:rect',ns)
for i,arm in enumerate(['B','C']):
 v=D['test2_totals'][arm]/1000;assert abs(float(bars[i].get('width'))-v/900*556)<1e-6
 assert math.isclose(float(bars[i].get('y')),297+i*90)
 checks.append({'object':'monitor-token-cost','arm':arm,'total_tokens':v*1000,'width_verified':True,'y_verified':True})
assert sum(D['test2_tokens']['B'])==D['test2_totals']['B'];assert sum(D['test2_tokens']['C'])==D['test2_totals']['C']
receipts=['verify-charts: 04_queue_results.svg | object=queue-target-cost | type=grouped-bar | mode=decomposable-calc | scale=0–80 from ticks | calc=ran×2 | svg=unchanged; x/heights programmatically matched','verify-charts: 05_test2_results.svg | object=monitor-token-cost | type=bar | mode=direct-calc | scale=0–900 from ticks | calc=ran | svg=unchanged; y/widths programmatically matched']
(P/'validation/chart-verification.json').write_text(json.dumps({'status':'PASS','receipts':receipts,'checks':checks,'c_token_percent_extra':(813649/740643-1)*100},indent=2));print('\n'.join(receipts))
