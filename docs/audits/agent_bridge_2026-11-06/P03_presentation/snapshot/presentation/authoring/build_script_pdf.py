from pathlib import Path
import json,html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
P=Path(__file__).parent
F=P.parents[1]/'COMS6998_Midterm_Nov6_2026';F.mkdir(exist_ok=True)
records=json.loads((P/'speaker_script.json').read_text())
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
c=canvas.Canvas(str(F/'COMS6998_Speaker_Script_EN_ZH_6_Pages.pdf'),pagesize=(595.28,841.89));c.setTitle('COMS6998 Midterm — English script and Chinese rehearsal notes');c.setAuthor('Chiyu Chen; Mingyuan Zheng; Yiwen Chen')
N=HexColor('#132A49');B=HexColor('#245DB5');G=HexColor('#5D6B7C');BG=HexColor('#F4F7FC')
for i,r in enumerate(records):
 c.setFillColor(B);c.rect(0,826,595.28,16,fill=1,stroke=0)
 c.setFont('Arial-Bold',11);c.drawString(44,794,'COMS6998  /  MIDTERM REHEARSAL')
 c.setFillColor(N);c.setFont('Arial-Bold',23);c.drawString(44,752,f"Slide {i+1:02d} — {r['speaker']}")
 c.setFont('Arial',11);c.setFillColor(G);c.drawString(44,727,f"Target {r['target_seconds']} sec  |  {r['timeline']}  |  {r['english_words']} English words")
 c.setStrokeColor(HexColor('#D8E1EC'));c.line(44,708,551,708)
 y=682
 c.setFillColor(B);c.setFont('Arial-Bold',12);c.drawString(44,y,'ENGLISH — SPEAK THIS');y-=28
 style=ParagraphStyle('speech',fontName='Arial',fontSize=12.8,leading=19,textColor=N,spaceAfter=12)
 p=Paragraph(html.escape(r['english']),style);w,h=p.wrap(507,y-340);p.drawOn(c,44,y-h);y-=h+37
 c.setFillColor(B);c.setFont('STSong-Light',12);c.drawString(44,y,'中文讲解 — 仅供理解与排练，不朗读');y-=23
 sty=ParagraphStyle('zh',fontName='STSong-Light',fontSize=11.2,leading=18,textColor=N,wordWrap='CJK')
 p=Paragraph(r['chinese_explanation'],sty);w,h=p.wrap(479,300);c.setFillColor(BG);c.rect(34,y-h-15,527,h+25,fill=1,stroke=0);p.drawOn(c,48,y-h);y-=h+40
 c.setFillColor(G);c.setFont('Arial-Bold',10);c.drawString(44,y,'PREPARATION RESPONSIBILITY');y-=18
 p=Paragraph(html.escape(r['preparation']),ParagraphStyle('prep',fontName='Arial',fontSize=10,leading=15,textColor=G));w,h=p.wrap(507,100);p.drawOn(c,44,y-h);y-=h
 assert y>115,(i,y)
 c.setStrokeColor(HexColor('#D8E1EC'));c.line(44,90,551,90)
 c.setFont('Arial',9);c.setFillColor(G);c.drawString(44,71,'Chiyu 1–2  |  Mingyuan 3–4  |  Yiwen 5–6  ·  Target total 5:30; hard limit 6:00')
 c.drawString(44,55,'Timing is an estimate at ~125 words/min; rehearse once with natural handoffs.')
 c.drawRightString(551,35,f'{i+1} / 6')
 c.showPage()
c.save()
(F/'COMS6998_Speaker_Script_EN_ZH.md').write_text((P/'speaker_script_en_zh.md').read_text())
print(F/'COMS6998_Speaker_Script_EN_ZH_6_Pages.pdf')
