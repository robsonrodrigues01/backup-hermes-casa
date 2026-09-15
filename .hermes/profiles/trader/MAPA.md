# MAPA — Perfil trader (O Trader, @traderera4bot)

Perfil criado em 15/09/2026 (clone do default). Agente de trade da casa.

## Identidade
- Nome: O Trader · Bot: @traderera4bot · SOUL.md define persona (frentista honesto do dinheiro)
- Modelo: glm-5.3-flash via proxy local http://127.0.0.1:8791/v1 (Headroom, unit hermes-headroom-trader.service)
- Gateway: hermes-gateway-trader.service (linger ON, sobe no boot)

## Regras vitais (resumo — texto completo no SOUL.md)
- FASE ATUAL: sandbox (dinheiro imaginário, US$ 10k) até 22/09/2026. Fase 2 (real) SÓ com OK do Rob.
- Script sandbox: ~/.hermes/scripts/trader-sandbox.py (tick a cada 15min) + relatório diário 9h Bsb no chat do Rob (via perfil default/Claudinho).
- Binance bloqueada p/ IP do servidor. Kraken e Polymarket ok.
- Estado sandbox: /home/hermes/trader-sandbox/state.json

## Credenciais (por NOME, nunca valores)
- TELEGRAM_BOT_TOKEN — no .env deste perfil (veio direto do BotFather 15/09)
- Chaves Vultr/exchange — herdam .env clonado / config.yaml
