#!/usr/bin/env python3
"""Leva 2: despachante Canoas, advocacia Alvorada, imobiliaria Campo Bom, odonto SL + cidade de 3 ambiguous."""
import hunt, json

Q2 = ['despachante Canoas contato email',
      'advocacia Alvorada contato email',
      'imobiliária Campo Bom contato email',
      'clínica odontológica São Leopoldo contato email']

res = hunt.hunt(Q2, per_q=9, max_pages=36)
json.dump(res, open('/home/hermes/.hermes/profiles/era4/comercial/hunt2.json', 'w'), ensure_ascii=False, indent=1)
print('== batch2:', len(res), 'lead(s) com contato ==')
for r in res:
    print('---')
    print('Q:', r['query'])
    print('URL:', r['url'])
    print('T:', r['title'])
    print('EM:', ';'.join(r['emails'][:4]))
    print('WA:', ';'.join(r['wa'][:3]), '| IG:', ';'.join(r['insta'][:3]))
    for d in r['dor'][:3]:
        print(' DOR:', d[:160])

print()
print('== confirmacao de cidade ==')
CITY = ['canoas', 'gravatai', 'cachoeirinha', 'porto alegre', 'portoalegre',
        'sao leopoldo', 'novohamburgo', 'novo hamburgo', 'campo bom', 'sapiranga']
for name, u in [('IMA', 'https://imaima.com.br/os.html'),
                ('Alano', 'https://www.clinicaalano.com.br/contato.php'),
                ('Sebben', 'https://www.gustavosebben.com.br/'),
                ('OrtopediaDaDor', 'https://clinicaortopediadador.com.br/contato/')]:
    p = hunt.fetch(u).lower()
    hits = sorted({c for c in CITY if c in p.replace('\n', ' ')})
    print(name, '->', hits)
