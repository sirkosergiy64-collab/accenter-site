"""Запасний шлях без конвеєра cats: додає/оновлює моделі з catalog/extra/*.json у catalog/data.json
(з тим самим округленням цін, що й build_site.py). Звичайний шлях — cats/build_site.py, який теж читає catalog/extra/."""
import json, glob, math, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def nice(v):
    if v is None: return None
    if v < 100: return int(math.ceil(v / 5) * 5)
    if v < 1000:
        h, r = divmod(int(math.ceil(v)), 100)
        for s in (0, 20, 50, 80):
            if r <= s: return h * 100 + s
        return (h + 1) * 100
    if v < 5000: return int(math.ceil(v / 50) * 50)
    return int(math.ceil(v / 100) * 100)
D = json.load(open(f'{R}/catalog/data.json', encoding='utf-8'))
idx = {d['a']: i for i, d in enumerate(D)}
n = 0
for f in sorted(glob.glob(f'{R}/catalog/extra/*.json')):
    for x in json.load(open(f, encoding='utf-8')):
        x['p'] = [[r[0], nice(r[1]), nice(r[2])] for r in x['p']]
        if x['a'] in idx: D[idx[x['a']]] = x
        else: idx[x['a']] = len(D); D.append(x)
        n += 1
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_fix import apply as _fix
_fix(D)
for x in D:
    x['p'] = [[r[0], nice(r[1]), nice(r[2])] for r in x['p']]
json.dump(D, open(f'{R}/catalog/data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('merged', n, 'total', len(D))
