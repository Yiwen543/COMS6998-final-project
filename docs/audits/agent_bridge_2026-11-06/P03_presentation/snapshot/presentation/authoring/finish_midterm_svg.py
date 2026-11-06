from pathlib import Path
from lxml import etree as E
P=Path(__file__).parent
ns={'s':'http://www.w3.org/2000/svg'};T='{http://www.w3.org/2000/svg}'
p=P/'svg_output/02_prototype.svg';r=E.parse(str(p));t=next(t for t in r.findall('.//s:text',ns) if t.text=='Measured feedback');t.text='Tool feedback';p.write_bytes(E.tostring(r))
p=P/'svg_output/05_test2_results.svg';r=E.parse(str(p));r.find('.//s:g[@id="monitor-chart-title"]',ns).set('data-pptx-bounds','64 199 720 36');r.find('.//s:g[@id="fixed-endpoint"]',ns).set('data-pptx-bounds','842 225 374 235')
g=r.find('.//s:g[@id="formal-disclosure"]',ns);txts=g.findall('s:text',ns);txts[0].set('y','542');txts[1].set('y','596');txts[1].text='94 BMC → 20 physical alarms + 74 unreproduced / unresolved (all C)'
t=E.Element(T+'text',x='84',y='570',**{'font-size':'20','fill':'#5D6B7C'});t.text='FAIL modes: 94 BMC · 7 prove · 3 cover';g.insert(2,t);p.write_bytes(E.tostring(r))
print('Final geometry and formal-mode disclosure repaired.')
