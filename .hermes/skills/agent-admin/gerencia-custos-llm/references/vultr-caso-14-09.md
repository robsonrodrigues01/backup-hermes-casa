# Vultr — preços, uso medido e plano aprovado (sessões 14/09–15/09/2026)

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
- Projeção sem mudança: ≈ **US$ 2.700/mês**

## Plano aprovado pelo Rob
1. **Passo 1 (FEITO e provado, noite 14/09→15/09)** — cmo e cto →
   `glm-5.3-flash`: `model.default` trocado por sed (1 linha em cada
   config.yaml — `grep -rn <modelo> <perfil>/` só achou `config.yaml:3`),
   teste na ROTA REAL deles (proxy 8789 + Bearer da key do config do cmo)
   respondeu `ok` no modelo novo; commit no cofre
   ("passo 1 economia: cmo+cto no glm-5.3-flash").
2. Migrar os dependentes do glm-5.1 moribundo: **lab primeiro** (cobaia),
   depois era4, depois default/Claudinho — aguardando OK do Rob p/ seguir.
   glm-5.1 = 404 recorrente (149×) e ausente do `GET /v1/models`.
3. **cuidar mantém GLM-5.3 completo** — frente pra cliente (famílias),
   qualidade acima de economia.
- Alvo: ≈ US$ 400/mês (~85% de economia).
- Estimativa pós-passo-1 apenas: ~US$ 900–1.200/mês (cmo/cto = maior fatia).

## Armadilhas reveladas pelo teste (14/09–15/09)
- Comando com key interpolada foi RETIDO pelo portão de segurança e ficou
  aguardando OK do Rob ("PODE" liberou). Caminho que passou: gravar o teste
  em arquivo (write_file) ou python heredoc lendo a key de config.yaml na
  hora de rodar — segredo nunca na linha de comando.
- Primeiro teste usou `max_tokens: 10` → flash respondeu `content: null`
  porque é modelo de reasoning (pensou no campo `reasoning` até estourar).
- Proxy 8789 sem header `Authorization: Bearer <key do config do perfil>`
  responde 401 — o teste fiel carrega a key do PRÓPRIO perfil alvo.

## Estado no fechamento (15/09)
- Passo 1 concluído; PASSO 2 PENDENTE de OK do Rob.
- Ao mudar de modelo: re-verificar PERF nos logs por alguns dias
  (tok_before/tok_out por modelo) para confirmar a economia real.
