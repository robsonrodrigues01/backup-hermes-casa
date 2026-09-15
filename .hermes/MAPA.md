# MAPA DA CASA — máquina vultr (Claudinho mantém)

> Leia quando alguém perguntar "onde está X?" / "onde ficam as coisas?" — não chute.

## Quem é quem (4 agentes Hermes nesta máquina)
- default: ~/.hermes → Claudinho, assistente pessoal do Rob · Telegram @claudinhovc_bot · api_server porta 8642
- cuidar: ~/.hermes/profiles/cuidar → Claudete, @claudetezinhabot (serviço hermes-gateway-cuidar)
- era4: ~/.hermes/profiles/era4 → Claudemir, @Claudemirera4bot (serviço hermes-gateway-era4)
- lab: ~/.hermes/profiles/lab → cobaia de testes, @bottesteerabot

## Compressores de memória (Headroom, 1 por bot)
- Portas: lab 8787 · default 8788 · cuidar 8789 · era4 8790 · serviços: hermes-headroom-*
- Extrato: curl http://127.0.0.1:<porta>/stats (e /stats-history)
- Plano B: copies config.yaml.bak-headroom nos homes de cada perfil (voltar base_url e reiniciar)
- Código/venv: ~/headroom-test (CLI: ~/headroom-test/venv/bin/headroom)

## Skills (por perfil)
- default: skills/design (4) · skills/dev (2) · skills/marketing (14) · skills/product (27) · skills/research (2) · skills/i-have-adhd
- era4: profiles/era4/skills/marketing (24) · profiles/era4/skills/i-have-adhd
- cuidar: profiles/cuidar/skills/marketing (22) · profiles/cuidar/skills/i-have-adhd
- lab: profiles/lab/skills/i-have-adhd
- i-have-adhd (2026-09-11, todos os 4): estilo de resposta TDAH-friendly, do repo ayghri/i-have-adhd — skill instalada + bloco always-on pendurado no SOUL.md de cada perfil (marcação `<!-- i-have-adhd -->`; remover o bloco para desligar). Também funciona por invocação ("/i-have-adhd" ou "use a skill").

## Repos e demos
- ~/tools/agent-reach → CLI de busca web (venv ~/.agent-reach-venv · bins em ~/.local/bin)
- ~/remotion-demo → vídeo em código (render testado) · ~/scrape-demo → scraping/CSV testado

## Credenciais (onde moram — NUNCA o valor)
- TELEGRAM_BOT_TOKEN e chaves de provedor: .env de cada perfil (os 4)
- Painel Desktop (app do Mac): HERMES_DASHBOARD_BASIC_AUTH_* no .env default; cópia em ~/.hermes/dashboard-credenciais.txt (chmod 600)
- Modelo/rota dos bots: config.yaml de cada perfil

## Painel Desktop (app do Mac)
- Serviço: hermes-dashboard.service (user) → `hermes dashboard --host 0.0.0.0 --port 9119 --no-open` (com login; NUNCA usar --insecure)
- Endereço pro app do Mac: http://66.42.78.129:9119 → opção "Remote gateway"
- Antes era processo volto (--insecure, sem senha) — substituído por serviço com fechadura em 2026-09-09

## Contexto dos perfis
 Homes: default=~/.hermes · cuidar=~/.hermes/profiles/cuidar · era4=~/.hermes/profiles/era4 · lab=~/.hermes/profiles/lab
 SOUL.md de cada perfil traz identidade + a regra de checar PENDENTES.md antes de responder status.
- trader = agente Trader, bot @traderera4bot (no ar 15/09/2026, hermes-gateway-trader.service), headroom 8791
