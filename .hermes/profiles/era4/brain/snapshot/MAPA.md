# MAPA DA CASA — máquina vultr (máquina compartilhada — leia também a versão do Claudinho em ~/.hermes/MAPA.md)

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
- default: skills/design (4) · skills/dev (2) · skills/marketing (14) · skills/product (27) · skills/research (2)
- era4: profiles/era4/skills/marketing (24)
- cuidar: profiles/cuidar/skills/marketing (22)

## Repos e demos
- ~/tools/agent-reach → CLI de busca web (venv ~/.agent-reach-venv · bins em ~/.local/bin)
- ~/remotion-demo → vídeo em código (render testado) · ~/scrape-demo → scraping/CSV testado

## Credenciais (onde moram — NUNCA o valor)
- TELEGRAM_BOT_TOKEN e chaves de provedor: .env de cada perfil (os 4)
- Modelo/rota dos bots: config.yaml de cada perfil

## Contexto dos perfis
 Homes: default=~/.hermes · cuidar=~/.hermes/profiles/cuidar · era4=~/.hermes/profiles/era4 · lab=~/.hermes/profiles/lab
 SOUL.md de cada perfil traz identidade + a regra de checar PENDENTES.md antes de responder status.

## Sua pasta
- ~/.hermes/profiles/era4 · skills: marketing (24) · SOUL.md e .env locais
- SQUADS.md (~hermes/profiles/era4) → squads da agência; regra do Rob: um por vez, com soul/SOP/tools íntegros antes de existir — só registrar o que estiver funcionando
