"""Наступний пост для Telegram-каналу @accentr_home.

python3 scripts/tg_next.py            -> JSON з типом поста й матеріалами
python3 scripts/tg_next.py --record ID TYPE [KEY] [TOPIC]
                                     -> дописати опублікований пост у ops/tg-log.json

Правила черги (номер поста N = кількість записів у журналі + 1):
  N % 10 == 0 -> tech   (доставка, упаковка, перевірка якості, оплата…)
  N % 5  == 0 -> trend  (тренди, виставки, матеріали, зручність, технології)
  інакше       -> model / category / designers по колу (model, category, model, designers)
"""
import json, os, random, sys, datetime, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://accenter.agency'
LOG = os.path.join(ROOT, 'ops', 'tg-log.json')

def load_log():
    try:
        return json.load(open(LOG, encoding='utf-8'))
    except FileNotFoundError:
        return []

def seo_pages():
    spec = importlib.util.spec_from_file_location('seo', os.path.join(ROOT, 'scripts', 'seo.py'))
    src = open(spec.origin, encoding='utf-8').read()
    ns = {}
    start = src.index('PAGES = ['); end = src.index(']\n', start) + 2
    exec(src[start:end], ns)
    return [(p[0], p[1], p[2]) for p in ns['PAGES']]

TECH = [
    'Перевірка якості на складі в Гуанчжоу: комплектація, сколи, відповідність замовленню; фото й відео перед відправкою',
    'Упаковка: камінь, скло й дзеркала їдуть у посиленій упаковці з дерев\'яною обрешіткою',
    'Що входить у ціну під ключ: доставка по Китаю, перевірка, упаковка, море, розмитнення, доставка до Львова',
    'Етапи замовлення: розрахунок, передоплата 50%, виготовлення, склад, перевірка, море, Львів, перевізник',
    'Оплата: долари, гривні (зокрема на рахунок ФОП чи ТОВ) або криптовалюта; курс фіксуємо перед оплатою',
    'Скільки триває доставка: морем 2–3 місяці в дорозі плюс термін виготовлення, який називаємо в розрахунку',
    'Вологість дерева: чому недосушене дерево деформується в гарячому контейнері і навіщо перевіряти це до відправки',
    'Кілька фабрик в одному замовленні: збираємо все на складі в одну партію',
    'Доставка по Україні: зі Львова Новою поштою або іншим перевізником за тарифом перевізника; підйом на поверх — окремо',
    'Виготовлення під проєкт: змінюємо розмір, колір і оздоблення моделі',
]
TREND = [
    'Новини меблевих виставок (Salone del Mobile, Maison&Objet, Design Shanghai, CIFF Guangzhou тощо): що показали',
    'Тренд сезону в інтер\'єрі: кольори, форми, текстури',
    'Матеріали, що зараз у моді: травертин, кап, рифлене дерево, метал, букле',
    'Зручність і ергономіка: як обрати висоту столу, глибину консолі, розміри приліжкової тумби',
    'Технологічність меблів: доводчики, приховані ручки, стійкі покриття, догляд за каменем',
    'Стилі: італійський мінімалізм, світла розкіш, вінтаж, ваб-сабі — як поєднувати',
    'Як підібрати меблі під розмір кімнати й не перевантажити простір',
    'Колір року та як вписати його в інтер\'єр через меблі й декор',
]

def price_txt(rows):
    lo = min(r[1] for r in rows); hi = max(r[2] or r[1] for r in rows)
    return f'${lo:,}'.replace(',', ' ') if lo == hi else f'від ${lo:,}'.replace(',', ' ')

def pick_model(D, log, cat=None):
    used = {e.get('key') for e in log[-300:]}
    recent_cats = [e.get('cat') for e in log[-3:]]
    pool = [d for d in D if d.get('p') and d['p'][0][1] and d['a'] not in used
            and (cat is None or d['c'] == cat)
            and os.path.exists(os.path.join(ROOT, 'catalog', 'img', d['a'] + '.jpg'))]
    pool = [d for d in pool if any('см' in r[0] for r in d['p'])] or pool
    fresh = [d for d in pool if d['c'] not in recent_cats] or pool
    d = random.choice(fresh)
    return {
        'key': d['a'], 'cat': d['c'], 'name': d['n'], 'category': d['c'],
        'price': price_txt(d['p']),
        'sizes': [r[0] for r in d['p']][:4],
        'materials': d.get('mt') or d.get('m'), 'styles': d.get('s'), 'about': d.get('d'),
        'photo': f"{SITE}/catalog/img/{d['a']}.jpg",
        'link': f"{SITE}/catalog/m/{d['a']}/",
    }

def main():
    log = load_log()
    if len(sys.argv) > 1 and sys.argv[1] == '--record':
        mid, typ = sys.argv[2], sys.argv[3]
        key = sys.argv[4] if len(sys.argv) > 4 else ''
        topic = sys.argv[5] if len(sys.argv) > 5 else ''
        cat = sys.argv[6] if len(sys.argv) > 6 else ''
        log.append({'n': len(log) + 1, 'type': typ, 'key': key, 'topic': topic, 'cat': cat,
                    'message_id': mid, 'date': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')})
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('recorded', len(log)); return
    random.seed()
    N = len(log) + 1
    D = json.load(open(os.path.join(ROOT, 'catalog', 'data.json'), encoding='utf-8'))
    insp = [f'{SITE}/assets/insp/{i}.jpg' for i in range(1, 9)]
    used_topics = [e.get('topic') for e in log]
    if N % 10 == 0:
        topic = min(TECH, key=lambda t: (used_topics.count(t), random.random()))
        out = {'type': 'tech', 'topic': topic, 'link': f'{SITE}/dostavka/',
               'photo': random.choice(insp + [f'{SITE}/assets/posts/kontrol-pered-vidpravkoyu.jpg']),
               'key': '', 'cat': ''}
    elif N % 5 == 0:
        topic = min(TREND, key=lambda t: (used_topics.count(t), random.random()))
        m = pick_model(D, log)
        out = {'type': 'trend', 'topic': topic, 'link': f'{SITE}/catalog/',
               'photo': random.choice(insp), 'model_option': m, 'key': '', 'cat': ''}
    else:
        regular = sum(1 for e in log if e['type'] in ('model', 'category', 'designers'))
        kind = ['model', 'category', 'model', 'designers'][regular % 4]
        if kind == 'model':
            out = {'type': 'model', **pick_model(D, log)}
        elif kind == 'category':
            pages = seo_pages()
            recent = [e.get('key') for e in log[-12:]]
            cands = [p for p in pages if p[1] not in recent] or pages
            cat, slug, h1 = random.choice(cands)
            m = pick_model(D, log, cat)
            out = {'type': 'category', 'key': slug, 'cat': cat, 'title': h1,
                   'link': f'{SITE}/catalog/{slug}/', 'photo': m['photo'], 'example': m}
        else:
            out = {'type': 'designers', 'key': 'designers', 'cat': '', 'link': f'{SITE}/designers/',
                   'photo': random.choice(insp)}
    out['n'] = N
    # UTM-мітка, щоб Google Analytics бачила переходи з Telegram
    utm = f"utm_source=telegram&utm_medium=social&utm_campaign={out['type']}"
    for k in ('link',):
        if out.get(k) and 'utm_source=' not in out[k]:
            out[k] += ('&' if '?' in out[k] else '?') + utm
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
