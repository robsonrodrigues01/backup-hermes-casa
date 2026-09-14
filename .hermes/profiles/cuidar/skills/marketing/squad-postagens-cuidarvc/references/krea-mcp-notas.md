# Krea AI via MCP — playbook de geração de arte (fonte principal do Agente 3)

> Estado (10/09/2026): server `krea-ai` HABILITADO no Hermes com 34 tools (`mcp_krea_ai_generate_image`, `mcp_krea_ai_get_job`, `mcp_krea_ai_list_models`, `mcp_krea_ai_get_model_schema`, `mcp_krea_ai_show_plans` etc.). Key da API em `MCP_KREA_AI_API_KEY` no `.env` do perfil cuidar (formato `uuid:secret`, autentica como Bearer). Endpoint: `https://api.krea.ai/mcp`.

## Infra (só se algo quebrar)
- O venv do hermes-agent exige `mcp==1.26.0` EXATO — versão nova renomeia `streamablehttp_client` p/ `streamable_http_client` e quebra; versão 1.15 falta kwarg `verify`. Fix: `uv pip install --python ~/.local/share/uv/tools/hermes-agent/bin/python mcp==1.26.0`.
- `.env` e `config.yaml` do perfil são protegidos contra patch/write_file direto. P/ trocar key de MCP: `python -c "from hermes_cli.config import save_env_value; save_env_value('MCP_KREA_AI_API_KEY', '<nova key>')"` usando o python do venv do hermes (`~/.local/share/uv/tools/hermes-agent/bin/python`).
- Depois de mudar config do MCP, o gateway precisa reiniciar para a SESSÃO ATUAL ver as tools. P/ reiniciar sem matar o próprio turno: `systemd-run --user --on-active=25s --unit=<nome> systemctl --user restart hermes-gateway-cuidar.service` (timer dispara após a resposta ser entregue). Unidades do Hermes são **user-level** (`systemctl --user`), não system.

## Modelos de imagem (o que usar)
- `google/nano-banana-2` — **funciona no plano free**, ~23-30s/geração, renderiza PT acentuado corretamente. Testado e aprovado (cards nota 9/10).
- `bytedance/seedream-4` — melhor para texto/fotorealismo, mas **exige plano pago** (402 "This model requires a higher plan").
- Outros vistos: `krea/krea-2/large` (fotorrealismo expressivo), `ideogram/ideogram-3` (estética), `google/nano-banana-pro` (top, caro), `z-image` (rápido).
- Sempre conferir `get_model_schema` antes de usar um modelo novo (campos variam: alguns pedem width/height, outros aspect_ratio).

## Créditos e planos (importante p/ operação contínua)
- Plano free ≈ **1 geração** — esgota imediatamente. 402 `INSUFFICIENT_BALANCE` = créditos acabaram.
- Squad 24/7 consome ~6 cards/dia ≈ 14.000 unidades/mês → **plano Pro (US$ 35/mês, 20.000 unidades ≈ 257 gerações)** recomendado; Basic (US$ 9/mês, 5.000 ≈ 64) cobre só ~10 dias; Max (US$ 70, 40.000). Anual = 40% off. Trial de 3 dias indisponível na conta.
- Quando der 402: chamar `show_plans` como PRIMEIRO tool call do turno e avisar o Rob com os planos **traduzidos em português**.

## Template de prompt aprovado (padrão dos cards do carrossel de lançamento — nota 9/10 no QC visual)
Estrutura (ajustar foto/texto por card; manter o resto):
```
Instagram carousel card {N} of 6, vertical 4:5, premium editorial design for a Brazilian eldercare platform.
Background photograph: {FOTO — ex: caring young woman's hands gently holding the wrinkled hands of an elderly lady},
soft warm golden-hour light, cozy home atmosphere, shallow depth of field, emotional and tender.
Design: translucent deep sky blue (#0ea5e9) gradient overlay on the lower half, crisp white typography.
Large bold white sans-serif headline in Brazilian Portuguese, exactly: '{TEXTO PT — entre aspas simples!}' —
perfectly accented, correct spelling, no typos. Below it, smaller white text: '{SUBTEXTO}'.
Bottom center, small brand logo: rounded blue square containing a white heart, followed by lowercase bold
wordmark 'cuidar.vc' in blue, tiny handle '@cuidarvc.br' below. Top right corner, small semi-transparent
white text '{N}/6'. Clean, modern, trustworthy, warm, high contrast, generous margins, all text fully visible,
nothing cut off, no watermarks, no extra letters.
```
Parâmetros: width 1080, height 1350 (feed 4:5).

## Fluxo de geração (padrão comprovado)
1. `get_model_schema` (preparação, turnos anteriores quando possível) → 2. `generate_image` **async** (sem sync) → anotar `job_id` → 3. `get_job(jobId)` até `status: completed` → 4. baixar URL com curl em `artes/artes-YYYY-MM-DD/` (usar sufixo `-v2` quando for redo de rejeição do QC) → 5. `vision_analyze` para QC local (textos, acentos, cortes, logo, artefatos) antes de aprovar.

## Pegadinhas (todas já aconteceram)
- **Aspas duplas no texto PT quebram o input JSON do MCP** (erro "expected record, received string"). Usar aspas simples nos textos citados dentro do prompt.
- **sync=true estoura timeout de 120s** quando a fila demora (o job continua rodando no server — o timeout é só do cliente). Usar async + get_job.
- **402 em lote**: se vários jobs derem 402 seguidos, o MCP entra em circuit breaker ("unreachable", ~60s) — esperar e NÃO insistir com retries.
- Logo do rodapé às vezes sai com cores invertidas (quadrado branco + coração, em vez de azul + coração branco) — detalhe menor; avaliar caso a caso no QC.
- A resolução entregue pode vir 928x1152 (~4:5) mesmo pedindo 1080x1350 — aceitável p/ Instagram; não rejeitar por isso.
