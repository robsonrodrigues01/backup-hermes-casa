#!/usr/bin/env python3
"""Caçador de leads ERA 4.0 — DDG html -> paginas -> contatos publicos."""
import urllib.request, urllib.parse, re, json, sys

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      'Accept-Language': 'pt-BR,pt;q=0.9'}

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', 'ignore')
    except Exception:
        return ''

def ddg(query, n=12):
    page = fetch('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote_plus(query))
    links = re.findall(r'uddg=([^&"]+)', page)
    out, seen = [], set()
    for l in links:
        u = urllib.parse.unquote(l)
        if u in seen or 'duckduckgo' in u:
            continue
        seen.add(u)
        out.append(u)
        if len(out) >= n:
            break
    return out

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
IMG_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js',
           '.woff', '.ico', '.mp4', '.mp3', '.pdf', '.webm', '.avif')

def visible_text(page):
    p = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', page, flags=re.S | re.I)
    p = re.sub(r'<[^>]+>', ' ', p)
    return re.sub(r'\s+', ' ', html.unescape(p)) if False else re.sub(r'\s+', ' ', p.replace('&amp;', '&').replace('&#63;', '?'))

import html as _html

def extract(page):
    raw = page
    emails = []
    for m in EMAIL_RE.findall(raw):
        m = m.lower().rstrip('.')
        if m.split('@')[1].endswith(IMG_EXT):
            continue
        if any(b in m for b in ('wixpress', 'sentry', 'example.com', 'domain.com', 'email.com',
                                'yourdomain', 'sentry-next', '@2x', 'jquery', 'bootstrap')):
            continue
        if m not in emails:
            emails.append(m)
    was = set(re.findall(r'wa\.me/(\d{10,15})', raw))
    api = set(re.findall(r'(?:api\.whatsapp\.com/send\?phone=|whatsapp://send\?phone=|wa\.link/)(\+?\d{10,15})', raw))
    was |= api
    wa = sorted(was)
    insta = []
    for m in re.findall(r'instagram\.com/([A-Za-z0-9_.]{2,30})/?', raw):
        if m in ('p', 'reel', 'reels', 'explore', 'tv', 'stories', 'share', 'accounts', 'direct', 'legal', 'about'):
            continue
        if f'@{m}' not in insta:
            insta.append(f'@{m}')
    txt = visible_text(raw)
    dor = []
    for pat in (r'[^.!?;]{0,90}(?:planilha)[^.!?;]{0,60}', r'[^.!?;]{0,60}(?:or[cç]amento)[^.!?;]{0,70}(?:whatsapp|zap|by莹|pelo)[^.!?;]{0,40}',
                r'[^.!?;]{0,70}(?:whatsapp|zap)[^.!?;]{0,40}(?:atendimento|agend|or[cç]amento|d[uú]vida|tira)[^.!?;]{0,40}',
                r'[^.!?;]{0,60}(?:ordem de servi[cç]o|agenda|agendamento)[^.!?;]{0,60}',
                r'[^.!?;]{0,60}(?:atendimento|converse)[^.!?;]{0,25}(?:por|via|atrav)e?s?[^.!?;]{0,30}whatsapp[^.!?;]{0,30}',
                r'[^.!?;]{0,60}(?:ligue|chame)[^.!?;]{0,40}[.!?]{0,1}'):
        for mm in re.findall(pat, txt, re.I):
            s = mm.strip()[:170]
            if s not in dor and len(s) > 15:
                dor.append(s)
    if len(dor) > 6:
        dor = dor[:6]
    return emails, wa, insta, dor

def hunt(queries, per_q=10, max_pages=30):
    seen_domains, results = set(), []
    pages_done = 0
    for q in queries:
        urls = ddg(q, per_q)
        for u in urls:
            dom = urllib.parse.urlparse(u).netloc.replace('www.', '')
            if not dom or dom in seen_domains or domainskip(dom):
                continue
            if pages_done >= max_pages:
                return results
            page = fetch(u)
            pages_done += 1
            if not page:
                continue
            em, wa, ig, dor = extract(page)
            if not (em or wa or ig):
                continue
            title = re.search(r'<title[^>]*>(.*?)</title>', page, re.S | re.I)
            title = _html.unescape(title.group(1)).strip()[:100] if title else ''
            seen_domains.add(dom)
            results.append({'query': q, 'url': u, 'dom': dom, 'title': title,
                            'emails': em, 'wa': wa, 'insta': ig, 'dor': dor})
    return results

def domainskip(dom):
    return any(x in dom for x in ('google', 'youtube', 'facebook', 'linkedin', 'tryterra',
                                  'mercadolivre', 'olx', 'instagram.com', 'wikipedia', 'gov.br',
                                  'gov.br', 'aponta', 'justo', 'ubit', 'hotmart', 'youtu',
                                  'docs.google', 'scribd', 'slideshare', 'reddit', 'x.com',
                                  'whatsapp.com', 'linktr.ee', 'link.bio', 'beacons', 'shopee'))

Q1 = [
    'clínica odontológica Canoas contato email WhatsApp',
    'clínica médica Gravataí "contato" email',
    'especialidades médicas Cachoeirinha contato email',
    'despachante Novo Hamburgo contato email',
    'escritório advocacia Novo Hamburgo contato email WhatsApp',
    'imobiliária Campo Bom contato email WhatsApp',
]

if __name__ == '__main__':
    per_q = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    res = hunt(Q1, per_q=per_q)
    with open('/home/hermes/.hermes/profiles/era4/comercial/hunt1.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f'== {len(res)} leads com contato de {len(Q1)} queries ==')
    for r in res:
        print('---')
        print('Q:', r['query'])
        print('URL:', r['url'])
        print('T:', r['title'])
        print('EM:', ';'.join(r['emails'][:4]))
        print('WA:', ';'.join(r['wa'][:3]), '| IG:', ';'.join(r['insta'][:3]))
        for d in r['dor'][:3]:
            print(' DOR:', d)
