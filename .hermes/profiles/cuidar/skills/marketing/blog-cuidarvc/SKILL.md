---
name: blog-cuidarvc
description: Operar, ajustar e auditar o blog do cuidar.vc e o Agente 9 Redator (diário 16h UTC, job 10f502a4aa15, profile cuidar). Use quando o Rob pedir artigo novo, edição ou correção no blog, ao diagnosticar run do redator, ao mexer na capa/imagem do artigo, na hospedagem de imagens, no RPC de publicação do Supabase ou na legibilidade do blog para LLMs e Google (prerender, sitemap, og:image).
category: marketing
---

# Blog do cuidar.vc e Agente 9 Redator

> 📎 **Receita completa e estado atual**: `references/blog-redator-agente9.md` (payload do RPC, escada de hospedagem de imagem, receita da capa, vigia de capas, pendências de dev). Bloco do Agente 9 no `cuidarvc/PENDENTES.md` tem as regras de conteúdo do Rob e o handoff dev (15/09).

**O que é**: o blog publica DIRETO no site via RPC do Supabase, sem revisão prévia (design do Rob). Agente 9 = cron diário 16h UTC (13h BRT) no profile cuidar; o CMO audita o artigo no briefing 18h e corrige republicando o mesmo slug. Pasta de trabalho: `/home/hermes/cuidarvc/squad/blog/` (payloads em `artigos/`, capas em `capas/`, banco de pautas em `pautas-blog.md`, script blindado `publicar.py`).

## Regras que não se violam
- Chaves do RPC (cvblog_ do agente + publishable key) moram SÓ como segredo no `.env` do profile cuidar: nunca no prompt, nunca em payload.
- **Republicar o mesmo slug = SUBSTITUI TUDO**: reenviar todos os campos do JSON canônico `artigos/<slug>.json`, nunca só o campo alterado.
- Prompt do redator ENXUTO: skill pesada no prompt estourou o limite de SAÍDA do run e derrubou o artigo (motivo do prompt v2). Artigo só no arquivo JSON, chat em 3 linhas.
- Regras de conteúdo do Rob (sem número sem fonte, saúde sem dose/diagnóstico, lei com gov.br + data, caminhos de ouro no /profissionais) valem no artigo e na capa.

## Capa e imagens
- Padrão 1200x630: foto pura z-image-turbo (zero texto no prompt) + painel de vidro; arquivo local `capas/<slug>.jpg`; URL vai no `p_imagem_url` do payload.
- Hospedagem: durável = domínio próprio via repo ou bucket do projeto (exige dev); provisório = litterbox 72h + vigia diário `ee8234ba33ab` (14h05 UTC, no_agent) que re-sobe a capa e republica. O handoff dev está no PENDENTES; entregue a hospedagem fixa, migrar URL e EXCLUIR o vigia.
- WAF da litterbox throttleia uploads anônimos em rajada (404/"uploads disabled" transitórios): gap entre uploads >=65s, User-Agent próprio no curl, e NUNCA rajada de testes manuais.

## Pegadinhas
- Erros do RPC retornam com HTTP 200: ler `ok:` e `erro` (`limite_diario` = 5 artigos NOVOS/24h; updates liberados).
- Cron `no_agent` (script puro, sem LLM): o script precisa morar em `~/.hermes/profiles/<profile>/scripts/<nome>.py` (a mensagem de erro cita `~/.hermes/scripts/`, mas o resolvedor real é o scripts DO PROFILE) e tem teto de ~120s (curl -m 40, gap 65s, no máximo 2 tentativas + fallback). Stdout vazio = entrega silenciosa (padrão vigia: só fala quando quebra); resultado real em `profiles/<profile>/cron/output/<job_id>/<timestamp>.md`.
- Legibilidade p/ LLMs: lado conteúdo já está no redator (resposta no 1º parágrafo, blocos ###, fonte oficial com link, zero travessão). O gargalo é o LADO SITE e é dev: HTML cru do artigo é shell genérico (Google e ChatGPT não enxergam título, conteúdo nem og:image); pedidos de prerender/SSR + sitemap dinâmico no PENDENTES.
