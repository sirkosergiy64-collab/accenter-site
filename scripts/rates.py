"""Оновлює catalog/rates.json: курс продажу USD та EUR з валютного аукціону Мінфіну.
Якщо джерело недоступне або цифри підозрілі — файл не змінюється."""
import json, re, sys, urllib.request, html, datetime, zoneinfo

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
      'Accept-Language': 'uk-UA,uk;q=0.9'}

def text(url):
    req = urllib.request.Request(url, headers=UA)
    raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')
    raw = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', raw, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw)))

def sell(cur):
    t = text(f'https://minfin.com.ua/ua/currency/auction/{cur}/buy/all/')
    m = re.search(r'Середній продаж\D{0,80}?(\d{2}[.,]\d{2,4})', t) or re.search(r'Средняя продажа\D{0,80}?(\d{2}[.,]\d{2,4})', t)
    if not m:
        raise ValueError(f'{cur}: не знайдено «Середній продаж»')
    return round(float(m.group(1).replace(',', '.')), 2)

try:
    usd, eur = sell('usd'), sell('eur')
except Exception as e:
    print('Курс не оновлено:', e); sys.exit(0)
if not (30 < usd < 90 and 30 < eur < 100 and eur > usd):
    print('Підозрілі значення, пропускаю:', usd, eur); sys.exit(0)
now = datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Kyiv'))
path = 'catalog/rates.json'
old = json.load(open(path, encoding='utf-8'))
new = {'date': now.strftime('%d.%m.%Y'), 'time': now.strftime('%H:%M'), 'USD': usd, 'EUR': eur,
       'src': 'валютний ринок (Мінфін), продаж'}
if old.get('USD') == usd and old.get('EUR') == eur and old.get('date') == new['date']:
    print('Без змін', usd, eur); sys.exit(0)
json.dump(new, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
print('Оновлено', new)
