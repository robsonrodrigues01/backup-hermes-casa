---
name: piloto-sandbox
description: "Como levantar um PILOTO de risco da casa como sandbox (dinheiro/conta/público de papel, zero perda real possível): runner determinístico com carteira virtual, regras de segurança DURAS embutidas no código (não em config), cron de tick silencioso + um relatório diário no chat do Rob, prazo de prova definido no boot, e trava de fase — só sai da fase 1 com OK novo e explícito dele. Dispara em 'vamos de sandbox', 'bot de papel', 'fase 1', 'testa antes de gastar', piloto de trading/agente/automação."
---

# Piloto sandbox (ideia de risco, provada sem risco)

Objetivo: toda ideia que pode gastar dinheiro real, tocar produção ou falar em
nome da casa em público entra primeiro como PILOTO SANDBOX — provado por dias,
com números na mesa, ANTES de qualquer decisão cara.

Caso de origem: AGENTE TRADER (15/09, Rob: "por enquanto vamos de sandbox").
Detalhe do caso (regras, scripts, cron ids, fontes de dados c/ data):
references/trader-sandbox-fase1.md

## As 7 regras da casa para um piloto sandbox

1. **Zero recurso real.** Sem conta, chave ou credencial real — nem "só pra
   testar". Sandbox lê dados PÚBLICOS (preço, feed) e opera sobre carteira
   virtual (ex.: US$ 10k fictícios) guardada em arquivo de estado local.
2. **Regras de risco EMBUTIDAS no código, não em config.** Limites (fracao
   por operação, alvo de lucro, stop, freio diário) como constantes do
   script. Config editável = piloto que "só uma vez" vai pro limite errado.
3. **Tick silencioso, relatório falante.** Tick de cron só roda e cala
   (no_agent / script determinístico — LLM a cada 15min é caro à toa).
   UM relatório por dia no chat do Rob, com números (posição, P&L,
   operações, freios que travaram).
4. **Estado do piloto em arquivo junto do runner** (estado.json na mesma
   pasta, `~/.hermes/scripts/`). Sobrevive a restart; sobe junto no cofre
   (repo backup-hermes-casa) porque o script fica no path versionado.
5. **Prazo definido no boot.** Datas de início e da apresentação (ex.:
   15→22/09, 7 dias úteis) anotadas no PENDENTES.md e no relatório. Sem
   prazo de prova, sandbox vira moradia eterna.
6. **Trava de fase é do Rob.** Subir de fase (dinheiro real, produção,
   público) nunca é decisão do agente — é uma pergunta nova, com o
   resultado do piloto na mesa, e responde só com OK explícito dele.
   Liga com a constituição: gastar dinheiro = zona "só com o Rob".
7. **Registrar e versionar.** PENDENTES.md recebe a entrada da fase; commit
   + push no cofre leva scripts e estado ANTES da data da prova, pra não
   perder o histórico do piloto se a máquina morrer no meio dela.

## Pitfalls

- **Auto-escalar por silêncio:** nenhum cron do piloto deve "avançar fase"
  se algo der muito bem. A porta entre fase 1 e fase 2 é conversa com Rob.
- **Tick com LLM** drena o headroom (regime de custo: ver skill
  gerencia-custos-llm). Tick = script; LLM só no relatório diário.
- **Runner em path não versionado** (ex.: /tmp): estado e código somem.
  Runner SEMPRE em `~/.hermes/scripts/` e referenciado por nome RELATIVO
  na ferramenta de cron (mesma exigência da skill backup-github-casa).
- **Sandbox que precisa de fonte bloqueada:** testar a fonte (endpoint
  público) no boot do piloto e registrar resultado + data no reference;
  não assumir que a fonte de ontem ainda responde.
- **Relatório sem números** ("tá rodando") não decide fase: sempre trazer
  P&L do período, nº de operações, freios ativados e custo do piloto.

## Passo-a-passo (copiando do caso trader)

1. Confirmar o gate: Rob falou explicitamente "sandbox" (anotar data).
2. Escrever runner em `~/.hermes/scripts/<nome>.py` partindo de
   templates/sandbox-runner.py: constantes de risco no topo, funções
   `ler_mercado()`, `decidir()`, `executar()`, `carregar()`.
3. Testar 2 ticks + gerar 1 relatório À MÃO antes de agendar nada
   (prova real antes do cron — nunca agendar coisa não testada).
4. Criar 2 crons: tick `*/15 * * * *` no_agent (script cala se nada
   anormal) + relatório diário às `0 12 * * *` UTC (= 9h Bsb, fuso do
   Rob) com prompt próprio que lê o estado e manda o resumo no chat.
5. PENDENTES.md: entrada "FASE 1 SANDBOX no ar" com prazo e regras.
6. Commit + push no cofre (repo `backup-hermes-casa`).

## Referências
- references/trader-sandbox-fase1.md — caso AGENTE TRADER completo
- templates/sandbox-runner.py — esqueleto do runner de papel

## Caso irmão
- Decisão de estratégia antes de criar o piloto → skill conselho-de-ia.
- Cron scripts em ~/.hermes/scripts/ e push automático → backup-github-casa.
