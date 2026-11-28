"""Застосовує catalog/fix.json до списку моделей (викликається з cats/build_site.py і scripts/merge_extra.py)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def apply(items):
    F = json.load(open(f'{R}/catalog/fix.json', encoding='utf-8'))
    K = float(os.environ.get('CNY', '6.7710')) / float(os.environ.get('USD', '45.1064'))
    for x in items:
        f = F.get(x['a'])
        if not f: continue
        for k, v in f.items():
            if k in ('p_cny', 'p_keep_price'): continue
            x[k] = v
        if 'p_cny' in f:
            x['p'] = [[lab, round(c * 3 * K), round(c * 3 * K)] for lab, c in f['p_cny']]
        if 'p_keep_price' in f and x.get('p'):
            x['p'] = [[f['p_keep_price'], x['p'][0][1], x['p'][0][2]]]
    return items
