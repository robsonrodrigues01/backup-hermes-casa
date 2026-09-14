---
name: lead-hunting
description: "SOP do Caçador de Leads da ERA 4.0 — prospecção de PMEs com dor de automação (ICP: Brasil, foco RM de Porto Alegre e Vale dos Sinos). Use quando precisar gerar/atualizar a base de leads."
---

# SOP — Caçador de Leads (squad Comercial)

## ICP (definido pelo Rob em 11/09/2026)
- **Porte:** PMEs brasileiras (não brigar com grandes/enterprise)
- **Foco geo:** Região Metropolitana de Porto Alegre + Vale dos Sinos (RS) — cidades-chave: POA, Canoas, Cachoeirinha, Gravataí, Alvorada, Viamão, São Leopoldo, Novo Hamburgo, Campo Bom, Sapiranga, Esteio, Sapucaia
- **Sinais de dor que justificam lead:** "planilha pra tudo" / processos manuais repetitivos / agendamento e arquivamento de documentos no WhatsApp / atendimento sobrecarregado / orçamento por WhatsApp sem sistema / dados re-digitados entre sistemas / sem site ou site morto
- **Segmentos que costumam encaixar:** clínicas e consultórios, despachantes/advocacia, escritórios de contabilidade, imobiliárias, escolas e turismo local, indústrias e distribuidoras pequenas, serviços técnicos

## Cadência
- Meta por caçada: **~20 leads novos** (cron de segunda-feira 9:00). Smoke test: 3 leads.
- Canais de saída (só prepara rascunho): e-mail, Instagram, WhatsApp — envio manual pelo Rob.

## Procedimento
1. Definir o foco da caçada: 1–3 cidades + 1–2 segmentos (evita espalhamento).
2. Prospectar: Google Maps, diretórios regionais (associações comerciais, guias), Instagram local, LinkedIn quando aparecer. Registrar empresa ATIVA (site vivo, publicação recente, WhatsApp de atendimento).
3. Coletar por lead: nome, cidade, segmento, porte se visível, site, TODOS os contatos públicos (e-mail no site, @insta, WhatsApp publicado). Fonte + data da verificação.
4. Anotar `sinal_de_dor` concreto e observável na fonte (cite o que viu: "somos atendentes no WhatsApp", "orçamento em PDF manual"). Sem dor visível → descartar.
5. Dedupe: procurar o nome/CNPJ em `leads.csv` antes de adicionar. Nunca duplicar.
6. Append em `~/.hermes/profiles/era4/comercial/leads.csv` (UTF-8, uma linha por lead, `status=novo`, `proximo_passo` = toque sugerido e canal).
7. Report final: total novos, 5 destaques (dor mais forte + melhor canal de entrada), leads sem contato nenhum (marcar `proximo_passo=recaçar contato`).

## Eficiência (lições do smoke test 11/09)
- Orçamento por caçada: iterações limitadas por rodada (~20 ferramentas). Gravar no CSV CEDO, por lote (ex.: a cada 3 leads validados), nunca acumular tudo pro final da rodada.
- Scraping pesado (browser/Selenium) custa muitas iterações — caminho preferencial: busca DDG (`https://html.duckduckgo.com/html/?q=escritorio+contabilidade+Sao+Leopoldo+contato+email`) → abrir só 3–5 páginas de contato dos resultados → extrair e-mails/wa.me.
- google.com/search está bloqueado no IP do VPS (retorna /sorry captcha) — nunca usar como fonte.
- Executar Python via `terminal`; `execute_code` pode travar pedindo consentimento do Rob.
- Fontes que deram errado 2× seguidas: trocar de estratégia (diretório regional → sites diretos), não insistir na mesma rota.

## Armadilhas
- **NUNCA inventar e-mail/telefone** — só o publicado. Sem contato = linha válida com `proximo_passo` indicando onde caçar (ex.: "verificar @insta linkado no perfil do Maps").
- WhatsApp = só números publicados como contato de atendimento/site (via wa.me). Nunca extrair de listas paralelas.
- Nome fantasia vs razão social: usar o que a empresa se apresenta publicamente; razão social só se constar na fonte.
- Guardar `fonte` sempre (URL) — permite verificação posterior e follow-up.
