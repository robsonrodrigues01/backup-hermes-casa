---
name: gerencia-custos-llm
description: "Auditar gasto de tokens da casa multi-agente (logs do headroom), mostrar onde o dinheiro vai por modelo/bot, propor migração pra modelos mais baratos (ex.: glm-5.3 → glm-5.3-flash na Vultr) e executar em ordem segura. Dispara em 'quanto tá custando', 'tá muito caro', 'economizar', 'trocar de modelo', ou sinal de modelo sendo aposentado pelo provedor."
---

# Gerência de custos de LLM da casa (frota multi-agente)

Casa com 4+ bots pagando tokens por utilização (Vultr). Este é o fluxo para
auditar, propor economia e migrar sem quebrar agentes.

## Mapa do gasto
- Cada perfil/bot fala com o provedor através de um proxy headroom próprio:
  logs em `~/.headroom*/logs/proxy.log*` (rotacionam em .1, .2, ...).
- O modelo de cada perfil fica em `~/.hermes/profiles/<p>/config.yaml` →
  `model.default` (e `base_url` apontando pro proxy na porta do perfil;
  ex.: lab=8787, cmo/cto=8789).
- Lista de modelos vivos do provedor: `GET /v1/models` com a key que já
  está em config.yaml (não perguntar token ao Rob — já existe no arquivo).

## Medir antes de opinar
1. `scripts/uso-por-modelo.sh` (desta skill) agrega tok_in/tok_out por modelo
   a partir das linhas PERF dos logs.
2. Traduzir em dinheiro com a tabela vigente (recarregar do provedor —
   preços mudam; ver references/vultr-caso-14-09.md como formato, não como
   verdade eterna).
3. Número do mês atual vs número pós-migração: é essa comparação que o Rob
   decide — simples, sem jargão, UMA pergunta por vez (estilo rob-comms-style).

## Sinais de aposentadoria de modelo (migrar ANTES de morrer)
- 404 recorrente no log do proxy para o modelo (ex.: 149 numa janela).
- Modelo sumiu do `GET /v1/models` mas perfis ainda apontam pra ele.
- Caso 14/09: glm-5.1 deu 404 149× e já não estava na lista com 3 perfis
  dependentes (default/Claudinho, era4, lab) → migrar por ordem de risco.

## Ordem segura de migração
1. **lab** primeiro (perfil-cobaia, convenção da casa).
2. Agentes internos (cmo, cto, squads de marketing) — aguentam modelos
   "flash" porque o trabalho é interno.
3. Frente pra cliente POR ÚLTIMO e só mantendo qualidade (cuidar fala com
   famílias — merece modelo completo; avaliar antes de flash).
- Nunca migrar tudo de uma vez; validar cada degrau com teste real.

## Pitfalls
- **Comando com material de chave (mesmo via variável/substituição) pode
  ser retido pelo portão de segurança e fica aguardando OK do Rob** —
  o timeout vira bloqueio e silêncio NÃO é consentimento. Caminho melhor:
  gravar o teste num arquivo `.sh` que lê a key de config.yaml NA HORA de
  rodar (nada sensível na linha de comando), e pedir "pode?" ao Rob antes.
- Prometer economia com tabela antiga = vender sonho; sempre re-buscar preços.
- Trocar `model.default` não cobre tudo: dar `grep -ri <modelo-velho>`
  no perfil (squads, cron prompt, config de subagentes) — tem referência
  espalhada e cada ponta solta continua pagando pelo caro.
- Fallback silencioso: se o provedor retorna 404 e há fallback na Vicuña
  config, o barulho só aparece no log — conferir PERF por modelo depois
  da troca, não só "parece funcionar".

## Referências
- scripts/uso-por-modelo.sh — agregação de uso por modelo (logs headroom)
- references/vultr-caso-14-09.md — tabela de preços da época, uso medido e plano aprovado
