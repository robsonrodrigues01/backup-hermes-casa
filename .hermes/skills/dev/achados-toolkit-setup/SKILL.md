---
name: achados-toolkit-setup
description: >-
  Como instalar e operar as agent-tools já verificadas nesta máquina
  (Agent-Reach, last30days, Headroom, Remotion, Crawlee, Maxun/gstack) —
  paths duráveis, pitfalls e comandos de prova. Use quando o Rob mandar
  um novo "ACHADO" (print de skill/tool de IA), quando algum desses tools
  faltar, ou para reutilizar os pilotos (ex.: render de vídeo, CSV de scraping).
---

# Achados: toolkit de agentes nesta máquina

Contexto da máquina (SEMPRE assume): Linux, user `hermes`, **sem sudo**,
Python 3.12 com **PEP 668** (usar `uv`), npm global bloqueado (prefix `/usr`,
sem root), Node 22 OK, docker ausente. Quirk: **`/tmp` não é garantido entre
chamadas de execute_code** — clone + use no MESMO script. Fontes duráveis em
`~/tools/`, demos em `~/<nome>-test|demo/`. Regra forte: **prova real sempre,
nunca fabricar output**.

## Fluxo ACHADOS (aprovado pelo Rob — repita p/ cada print novo)
Prints chegam de human__academy (IG) e syntax.ai (X), às vezes com typo
(phrym→phuryn) — corrigir antes de catalogar. Ordem:
1. `git clone <repo> ~/tools/<nome>` — inventariar skills/SKILL.md de cada
   casa no MESMO script.
2. Confirmar que é real via API GitHub (stars, último push) — já achamos
   falsos Agent-Reach de marca e repos vizinhos mal lidos no print.
3. Revisar segurança à mão (grep subprocess/cookies/env/URLs) antes de
   qualquer coisa. Se `hermes skills install` bloquear (community +
   verdict dangerous — `--force` NÃO passa), instalar por cópia manual
   para `~/.hermes/skills/<categoria>/<nome>` e rodar o `--diagnose`
   do próprio tool como prova desinfetada.
4. Instalar o melhor em mim + prova real com número na mão
   (render MP4, CSV, % de compressão).
5. Distribuir pro era4/cuidar SÓ com OK explícito do Rob no chat.

## Agent-Reach (CLI de internet p/ agentes, ★79k)
- Fonte: `~/tools/agent-reach` · venv: `~/.agent-reach-venv` · bins linkados em `~/.local/bin` (`agent-reach`, `yt-dlp`)
- Estado: `~/.local/bin/agent-reach doctor` — 4/15 canais zerados (RSS, V2EX, Bili-search, web)
- Pitfalls: **web-Jina devolve 401** (reputation do IP do server) → precisa `JINA_API_KEY` (free) via `agent-reach configure`; X/Reddit/Facebook/Instagram/XHS/LinkedIn exigem **cookies de CONTA SECUNDÁRIA** do Rob (canais premium); npm global impossível → Exa/mcporter pendente; `um account` gh CLI ausente (sudo), usar API/web como fallback
- Legit check do próprio repo: sem token/cripto da marca (falsos Agent-Reach existem)

## last30days (skill de research, ★61k)
- `hermes skills install` BLOQUEIA (verdict dangerous, 70 findings; `--force` não passa) → via alternativa do repo: fonte em `~/tools/last30days-skill`, cópia manual em `~/.hermes/skills/research/last30days` (revisar `scripts/last30days.py` — clean: só leitura de cookies/env e subprocess yt-dlp)
- Prova: `cd ~/.hermes/skills/research/last30days && python3 scripts/last30days.py --diagnose` → fontes livres: reddit, hackernews, polymarket, youtube, github
- X precisa XAI_API_KEY **ou** cookies (server não tem browser)

## Headroom (compressão anti-token, ★71k)
- Demo em `~/headroom-test/` (venv uv + `headroom-ai` **+ extras `[proxy]`**)
- Prova 1 (library): log 2,6MB → 96,8% com fatos byte-a-byte preservados; YAML 20KB −40%; CCR reversível; ~33 ms
- **Integrado de fato em 2026-09-09: EM PRODUÇÃO nos 4 bots** (lab 8787 · default 8788 · cuidar 8789 · era4 8790) — 1 unit systemd + 1 `HEADROOM_WORKSPACE_DIR=/home/hermes/.headroom-<perfil>` por bot (stats separados), `model.base_url` → `http://127.0.0.1:<porta>/v1`, backup de rollback `config.yaml.bak-headroom` em cada home, extrato `curl 127.0.0.1:<porta>/stats`. E2E verificado: Rob mandou "oi" pro @bottesteerabot ✅ e cada oficial respondeu smoke perfeitamente. Molde original (lab):
  1. `uv pip install --python ~/headroom-test/venv/bin/python "headroom-ai[proxy]"` — sem extras o CLI reclama `No module named 'fastapi'`
  2. Unit systemd: `~/.config/systemd/user/hermes-headroom-lab.service` — ExecStart `venv/bin/headroom proxy --port 8787 --openai-api-url <BASE_URL_DO_PROVEDOR> --no-telemetry`, Restart=always
  3. No `config.yaml` do perfil, trocar **SÓ** `model.base_url: http://127.0.0.1:8787/v1` (deixar bloco `providers.*` intacto)
  4. Restart do gateway: `export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; systemctl --user restart hermes-gateway-lab`
  5. Verificação: endpoints `/livez /readyz /health /stats /stats-history` na porta; smoke headless = `hermes -p lab chat -q "ping" -Q --max-turns 2`; `/stats` conta `api_requests` e mostra compressão real por request (`best_detail` tipo `20,5k→16,1k tokens`; requests curtas ficam `prefix_frozen`, 0% é esperado nelas)
- Padrão REUTILIZÁVEL: qualquer proxy local entra entre gateway e modelo com o mesmo molde (unit systemd + base_url em 127.0.0.1:PORTA/v1 + smoke via chat -q -Q)
- ⚠ Nunca reiniciar o PRÓPRIO gateway (`hermes-gateway.service`, a única unit SEM sufixo) a partir de processo-filho/background do agente: o systemctl do filho morre no cgroup kill e derruba o turno à meia-frase — usar `systemctl --user` com `DBUS_SESSION_BUS_ADDRESS` explícito; restarts "desaparecendo" na tela do Rob = gateway reset (restart counter cai no journal)

## Remotion (vídeo em código, ★40k+ skills oficiais remotion-dev/skills)
- Projeto: `~/remotion-demo` (Node 22; Chrome Headless Shell auto-baixa no primeiro render)
- Render 1-linha: `cd ~/remotion-demo && npx remotion render src/index.ts HelloWorld out/test.mp4`
- Prova: `out/test.mp4` válido (5 s), ffprobe disponível

## Crawlee-Python / Maxun (scraping, era4)
- Demo: `~/scrape-demo` — PlaywrightCrawler → `quotes.csv` real (41 linhas, 2,4 s)
- Pitfall **crítico** aqui: chromium morre com SIGTRAP sem sandbox → passar `browser_launch_options={"args": ["--no-sandbox", "--disable-gpu"]}`; crawlee 1.10 usa APIs novas (`crawlee.crawlers`, `concurrency_settings`)
- **Maxun** (recorder no-code, AGPL): exige docker — instalar docker é decisão do Rob (sudo)
- Par recomendado: Maxun = rampa no-code/descoberta; Crawlee = produção versionável

## Distribuição por perfil (já feita — conferir antes de re-instalar)
- default: `design/` (4 do taste-skill) · `dev/full-output-enforcement` · `marketing/` (14) · `product/` (27 do phuryn/pm-skills) · `research/` (agent-reach, last30days)
- era4: 24 marketing · cuidar: 22 marketing
- gstack (Garry Tan, ★132k): NÃO é install — é blueprint de papéis p/ squads (todo aberto)