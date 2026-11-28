"""Секція «Реальні фото меблів» на головній: фото покупців з assets/real/<ART>/N.jpg (список — cats/real.json → поле rp у data.json)."""
import json, html, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = [d for d in json.load(open(f'{R}/catalog/data.json', encoding='utf-8')) if d.get('rp')]
esc = html.escape
cards = ''
for d in D:
    lo = min(r[1] for r in d['p'])
    imgs = ''.join(f'<img src="/assets/real/{d["a"]}/{i}.jpg" alt="Реальне фото: {esc(d["n"])}" loading="lazy">' for i in range(1, min(d['rp'], 4) + 1))
    pr = format(lo, ',').replace(',', ' ')
    cards += (f'<a class="rcard" href="/catalog/m/{d["a"]}/#real"><div class="rimg">{imgs}</div>'
              f'<div class="rtx"><b>{esc(d["n"])}</b><span>від ${pr} з доставкою до Львова</span><em>Усі фото й ціни →</em></div></a>')
sec = f'''<!--REAL--><section id="real" style="padding-top:0"><div class="wrap">
 <h2>Реальні фото меблів</h2>
 <p class="sub">Клієнти часто питають живі фото, бо в інтернеті багато рендерів. Тут — фото моделей з нашого каталогу, які зробили покупці у себе вдома.</p>
 <style>.rgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}.rcard{{display:block;background:#fff;border:1px solid var(--line,#e6dfd3);border-radius:16px;overflow:hidden;text-decoration:none;color:inherit}}.rimg{{display:grid;grid-template-columns:1fr 1fr;gap:2px}}.rimg img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}.rtx{{padding:12px 14px 14px;display:flex;flex-direction:column;gap:3px}}.rtx b{{font:500 19px Lora,serif}}.rtx span{{color:#6b6357;font-size:14px}}.rtx em{{font-style:normal;color:#94723e;font-weight:600;font-size:14px;margin-top:4px}}</style>
 <div class="rgrid">{cards}</div>
</div></section><!--/REAL-->'''
p = f'{R}/index.html'; c = open(p, encoding='utf-8').read()
if '<!--REAL-->' in c:
    c = c[:c.index('<!--REAL-->')] + sec + c[c.index('<!--/REAL-->') + len('<!--/REAL-->'):]
else:
    i = c.index('<section id="inspo"')
    c = c[:i] + sec + '\n' + c[i:]
open(p, 'w', encoding='utf-8').write(c)
print('real models:', len(D))
