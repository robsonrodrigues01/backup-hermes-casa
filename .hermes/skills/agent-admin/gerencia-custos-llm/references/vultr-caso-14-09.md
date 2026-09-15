# Vultr — preços, uso medido e plano aprovado (sessão 14/09/2026)

⚠️ Tabela com data — NÃO reusar como verdade eterna; re-buscar preços
(`GET /v1/models` + página de preços da Vultr) antes de qualquer estimativa.

## Preços conforme a imagem do Rob (fluxo $/1M tokens, na data)
| modelo | entrada | saída |
|---|---|---|
| GLM-5.3 | 0,75 | 3,00 |
| GLM-5.3-flash | 0,10 | 0,35 |
| DeepSeek V4 Flash | 0,10 | 0,25 |
| glm-5.1 | N/D — já fora da lista de modelos da Vultr |

## Uso medido (logs, janela de 3–4 dias de casa)
- glm-5.3 (cuidar+cmo+cto): 352,3M in / 6,9M out ≈ **US$ 285** na janela
- zai-org/GLM-5.1-FP8 (default+era4+lab): 43,9M in / 1,2M out
- deepseek-v4-flash-0731: 19,9M in / 0,2M out
- Projecão sem mudança: ≈ **US$ 2.700/mês**

## Plano aprovado pelo Rob ("sim" no fechamento da sessão)
1. **Passo 1** — cmo e cto → `glm-5.3-flash` (trabalho interno de squad)
2. Migrar os dependentes do glm-5.1 moribundo: **lab primeiro** (cobaia),
   depois era4, depois default/Claudinho
3. **cuidar mantém GLM-5.3 completo** — frente pra cliente (famílias),
   qualidade acima de economia
- Alvo: ≈ US$ 400/mês (~85% de economia)

## Estado no fechamento da sessão
- Nada migrado ainda; cmo/cto ainda em glm-5.3.
- Teste do flash ("diga ok" direto + via proxy do lab) ficou PENDENTE:
  o comando carregava a key interpolada e foi retido pelo portão de
  segurança a espera do OK do Rob. Caminho registrado na SKILL.md:
  gravar teste em .sh que lê a key de config.yaml na hora de rodar.
- Para o próximo turno desta pauta: rodar o teste, depois trocar
  `model.default` em cmo/cto e re-verificar PERF dos logs.
