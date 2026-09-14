#!/usr/bin/env python3
"""Append leads validados em leads.csv com dedupe + confirmacao de cidade nas paginas."""
import hunt, csv, os, re, urllib.parse

CSV = '/home/hermes/.hermes/profiles/era4/comercial/leads.csv'
CITY = ['canoas', 'gravatai', 'cachoeirinha', 'alvorada', 'viamao',
        'porto alegre', 'portoaalegre', 'sao leopoldo', 'novo hamburgo',
        'novohamburgo', 'campo bom', 'sapiranga', 'esteio', 'sapucaia']

# (empresa, cidade_a_confirmar, seg, site, contato_tipo, contato_valor, dor, fonte_url, prox_passo)
ROWS = [
    ('OdontoCanoas', 'Canoas', 'odontologia', 'https://odontocanoas.com.br',
     'email;whatsapp;instagram', 'contato@odontocanoas.com.br;wa.me/5551982330246;@odontocanoas',
     'pagina de contato so com formulario + 1 WhatsApp de atendimento - triagem e agendamento manuais',
     'https://odontocanoas.com.br/contato/', 'toque 1 por WhatsApp (agenda automatica de consultas no zap)'),
    ("L'Amore Odontologia", 'Canoas', 'odontologia', 'https://www.lamoreodontologia.com.br',
     'email;whatsapp;instagram', 'contato@lamoreodontologia.com.br;lamoreodontologia@gmail.com;wa.me/5551985833951;@lamoreodontologia',
     'consulta agendada pela pagina de contato/WhatsApp - sem agenda online',
     'https://www.lamoreodontologia.com.br/contato/', 'toque 1 por WhatsApp (automatizar confirmacao de consultas)'),
    ('Centro Odontologico Canoas', 'Canoas', 'odontologia', 'https://centroodontologicocanoas.com.br',
     'whatsapp;instagram', 'wa.me/555198131007;@centroodontologicocanoas',
     'FAQ do site manda agendar consulta pelo telefone (51) - agendamento telefonico manual',
     'https://centroodontologicocanoas.com.br/', 'toque 1 por WhatsApp (FAQ/respostas automaticas + agenda)'),
    ('Bhem+ Clinica Odontologica', 'Canoas', 'odontologia', 'https://bhem.com.br',
     'whatsapp;instagram', 'wa.me/5551990188338;@bhem_odontologia',
     'formulario Nome/E-mail/WhatsApp no site soh para agendar consulta - agendamento manual via zap',
     'https://bhem.com.br/', 'toque 1 por WhatsApp (agendamento automatico)'),
    ('Clinica Odontologica Gustavo Sebben', 'Canoas', 'odontologia', 'https://www.gustavosebben.com.br',
     'email;whatsapp', 'clinica@gustavosebben.com.br;wa.me/5551981307828',
     'agendamento por telefone/WhatsApp, sem portal de agenda online visivel no site',
     'https://www.gustavosebben.com.br/', 'toque 1 por WhatsApp (lembretes e agenda)'),
    ('Open Clinic Gravatai', 'Gravatai', 'clinica medica', 'https://openclinic.com.br',
     'email;whatsapp', 'atendimento@openclinic.com.br;wa.me/5551992562102',
     'pagina dedicada a telefone para agendar consulta; atendimento e RH na mesma caixa de e-mail',
     'https://openclinic.com.br/telefone-clinica-medica/', 'toque 1 por WhatsApp (fila de agendamento automatica)'),
    ('Clinica IMA', 'a confirmar', 'clinica medica', 'https://imaima.com.br',
     'email', 'atendimento@imaima.com.br;contato@imaima.com.br',
     'sem WhatsApp nem Instagram publicados - contato soh por e-mail',
     'https://imaima.com.br/os.html', 'toque 1 por e-mail (digitalizar agenda e triagem)'),
    ('Clinica Juliana Kerbes', 'a confirmar', 'clinica medica', 'https://clinicajulianakerbes.com.br',
     'instagram', '@clinicajulianakerbes',
     'e-mail publicado no site e da agencia web (sites@witu.digital) - a clinica nao tem contato proprio por e-mail',
     'https://clinicajulianakerbes.com.br/contato/', 'toque 1 no Instagram (DM; verificar @linkado no Maps)'),
    ('Espaco Vital Clinica e Formacao', 'Gravatai', 'clinica medica', 'https://www.espacovitalgravatai.com.br',
     'email;instagram', 'contato@espacovitalgravatai.com.br;@espacovitalgravatai',
     'clinica + cursos com contatos espalhados (e-mail/Insta) - sem sistema central de agendamento',
     'https://www.espacovitalgravatai.com.br/contato', 'toque 1 por e-mail (agenda + matriculas de cursos)'),
    ('Clinica Ortopedia da Dor', 'Gravatai', 'clinica medica', 'https://clinicaortopediadador.com.br',
     'email', 'clinicaortopediadador@gmail.com',
     'agendar consulta exige formulario/e-mail - e-mail em Gmail, sem dominio propre',
     'https://clinicaortopediadador.com.br/contato/', 'toque 1 por e-mail (agenda online)',
                                     ),
    ('Clinica Ineuro', 'Porto Alegre', 'clinica medica', 'https://ineuro.med.br',
     'email;whatsapp;instagram', 'contato@ineuro.med.br;wa.me/555197302302;@clinicaineuro',
     'Atendimento via whatsapp publicado ao lado de formulario - triagem dupla manual',
     'https://ineuro.med.br/contato/', 'toque 1 por WhatsApp (triagem automatica + lembretes)'),
    ('Clinica Alano', 'Cachoeirinha', 'clinica medica', 'https://www.clinicaalano.com.br',
     'email;whatsapp;instagram', 'contato@clinicaalano.com.br;wa.me/5551993492063;@clinicaalano',
     '"Ligue Agora" com telefone fixo no site - agendamento por telefone',
     'https://www.clinicaalano.com.br/contato.php', 'toque 1 por WhatsApp (agenda automatica)'),
    ('Salute Cachoeirinha', 'Cachoeirinha', 'clinica medica', 'https://www.clinicasalute.com.br',
     'email;whatsapp;instagram', 'salute@clinicasalute.com.br;wa.me/555130141111;@redesalute',
     'tabela de preços e agendamento exibidos no site com botao Agendar por formulario/WA',
     'https://www.clinicasalute.com.br/salute-cachoeirinha', 'toque 1 por WhatsApp (fila de agendamento)'),
    ('Cardioclin Cachoeirinha', 'Cachoeirinha', 'clinica medica', 'https://clinicacardioclin.com.br',
     'email;whatsapp;instagram', 'auxadm@clinicacardioclin.com.br;wa.me/5551999055771;@cardioclinoficial',
     'pre-agendamento via pagina Fale Conosco - agenda manual',
     'https://clinicacardioclin.com.br/fale-conosco/', 'toque 1 por WhatsApp (pre-agendamento automatico)'),
    ('Despachante Gonzalez', 'a confirmar', 'despachante', 'https://despachantegonzale.wixsite.com/meusite',
     'email', 'despachantegonzalez@gmail.com',
     'despachante com site gratuito wixsite e e-mail Gmail - processos e protocolos manuais',
     'https://despachantegonzale.wixsite.com/meusite', 'toque 1 por e-mail (digitalizar protocolos e acompanhamento)'),
    ('Despachante Postal', 'a confirmar', 'despachante', 'https://www.despachantepostal.com.br',
     'email;whatsapp;instagram', 'postal@despachantepostal.com.br;wa.me/555134632484;@despachantepostal',
     'atendimento por fixo/WA + formulario - fluxo manual de consultas e protocolos',
     'https://www.despachantepostal.com.br/', 'toque 1 por WhatsApp (bot de consulta de protocolo)'),
    ('Borges Advogados', 'a confirmar', 'advocacia', 'https://borgesadvogados.wixsite.com/borgesadvogados',
     'email;whatsapp', 'advocacia.cfborges@gmail.com;wa.me/5551996380475',
     'escritorio pequeno em wixsite gratuito - captação e agendamento de clientes manuais',
     'https://borgesadvogados.wixsite.com/borgesadvogados', 'toque 1 por WhatsApp (triagem de casos no zap)'),
    ('Lidiane Rossato Issi Advogados', 'a confirmar', 'advocacia', 'https://lriadv.com',
     'email;instagram', 'lidianerossatoissi@hotmail.com;@dra.lidianerossatoissi',
     'e-mail de contato em hotmail e placeholder "seuemail@gmail.com" publicado no site',
     'https://lriadv.com/contato/', 'toque 1 no Instagram/WhatsApp (DM profissional da dra.)'),
    ('Mello Imoveis', 'a confirmar', 'imobiliaria', 'https://melloimoveis.net',
     'email;whatsapp', 'melloimoveis@melloimoveis.net;rose@melloimoveis.net;wa.me/5551993140586;wa.me/5551997402980;wa.me/5551999888565',
     '3 numeros de WhatsApp publicados para atendimento - consulta de imoveis por zap sem CRM',
     'https://melloimoveis.net/contato', 'toque 1 por WhatsApp (CRM + triagem de leads de imoveis)'),
    ('Imobiliaria Walric', 'a confirmar', 'imobiliaria', 'https://www.walric.com.br',
     'email;whatsapp;instagram', 'atendimento@walric.com.br;wa.me/5551997789600;@imobiliariawalric',
     'atendimento por WhatsApp e formulario - captação de leads manual',
     'https://www.walric.com.br/contatos', 'toque 1 por WhatsApp (qualificaçao automatica de leads)'),
    ('Imobiliaria Dreger', 'a confirmar', 'imobiliaria', 'https://imobiliariadreger.com.br',
     'email;instagram', 'dreger@imobiliariadreger.com.br;@imobiliariadreger',
     'contato soh por e-mail/Insta - sem chat nem agenda online para visitas',
     'https://imobiliariadreger.com.br/contato', 'toque 1 no Instagram (DM; agendamento de visitas)'),
    ('AJG Imoveis', 'a confirmar', 'imobiliaria', 'https://www.ajgimoveis.com.br',
     'email;instagram', 'jgimobiliaria.adm@gmail.com;@ajgimoveis',
     'e-mail Gmail do negocio + formulario - sem dominio nem sistema',
     'https://www.ajgimoveis.com.br/contato', 'toque 1 no Instagram (DM; ofertar CRM leve)'),
    ('Imobiliaria Brasil Campo Bom', 'a confirmar', 'imobiliaria', 'http://www.aimobiliariabrasil.com.br',
     'email', 'brasil@aimobiliariabrasil.com.br',
     'site em HTTP sem WhatsApp/Instagram publicados - comunicacao soh por e-mail',
     'http://www.aimobiliariabrasil.com.br/', 'toque 1 por e-mail (modernizar presenca digital + leads)'),
    ('SorriOrto', 'a confirmar', 'odontologia', 'https://www.sorriorto.com.br',
     'email;whatsapp;instagram', 'sorriorto@hotmail.com;sorriorto@gmail.com;wa.me/5551981416629;@sorriorto',
     'dois e-mails (hotmail+gmail) + WA para agendar - agenda manual e dados espalhados',
     'https://www.sorriorto.com.br/', 'toque 1 por WhatsApp (agenda e recall de retorno)'),
    ('Paulo Zorzella Odontologia', 'a confirmar', 'odontologia', 'https://www.paulozorzella.com.br',
     'instagram', '@paulozorzella',
     '"Agendamento de Consulta: envie um e-mail ou ligue" - agendamento manual por e-mail/telefone',
     'https://www.paulozorzella.com.br/contato', 'toque 1 no Instagram (DM; verificar @linkado no Maps)'),
]

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

# --- dedupe vs CSV existente (nome normalizado ou dominio) ---
existing = []
if os.path.exists(CSV):
    with open(CSV, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            r = {k.strip(): (v.strip() if v else '') for k, v in r.items()}  # type: ignore
            if not r.get('empresa'):
                continue
            existing.append((norm(r['empresa']), urllib.parse.urlparse(r.get('site', '')).netloc.replace('www.', '')))

def site_net(u):
    return urllib.parse.urlparse(u).netloc.replace('www.', '')

today = '2026-09-14'
new_rows = []
for emp, cid, seg, site, ct, cv, dor, fnt, pp in ROWS:
    e_dom = site_net(site)
    dup = any(nx == norm(emp) or (e_dom and ex_dom and e_dom == ex_dom)
              for nx, ex_dom in existing)  # type: ignore
    if dup:
        print('DUP (ignorado):', emp)
        continue
    # confirma cidade na pagina se cidade a confirmar
    if cid == 'a confirmar':
        p_raw = hunt.fetch(fnt)
        p = p_raw.lower()
        hits = sorted({c for c in CITY if c in p.replace('\n', ' ')})
        if len(hits) >= 1:
            cid = {'gravatai': 'Gravataí', 'canoas': 'Canoas', 'cachoeirinha': 'Cachoeirinha',
                   'alvorada': 'Alvorada', 'viamao': 'Viamão', 'porto alegre': 'Porto Alegre',
                   'portoaalegre': 'Porto Alegre', 'sao leopoldo': 'São Leopoldo',
                   'novo hamburgo': 'Novo Hamburgo', 'novohamburgo': 'Novo Hamburgo',
                   'campo bom': 'Campo Bom', 'sapiranga': 'Sapiranga', 'esteio': 'Esteio',
                   'sapucaia': 'Sapucaia'}.get(hits[0], 'a confirmar')
            if len(hits) > 1:
                print('CITY multi:', emp, hits, '-> usando', cid)
    new_rows.append([today, emp, cid, seg, '', site, ct.replace(';', ';'), cv, dor, fnt, 'novo', pp])

if not new_rows:
    print('NADA a append')
else:
    exists = os.path.getsize(CSV) > 10
    with open(CSV, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        for r in new_rows:
            w.writerow(r)
    print('APPEND OK:', len(new_rows), 'linhas')

# totais
with open(CSV, encoding='utf-8-sig') as f:
    rows = [r for r in csv.DictReader(f)]
print('TOTAL linhas no CSV:', len(rows))
print('DATA (novos hoje):', sum(1 for r in rows if r.get('data_captura', '').strip() == today))
print('SEM contato qualquer:', sum(1 for r in rows if r and not (r.get('email') or r.get('whatsapp') or r.get('instagram') or r.get('contato_valor'))))
