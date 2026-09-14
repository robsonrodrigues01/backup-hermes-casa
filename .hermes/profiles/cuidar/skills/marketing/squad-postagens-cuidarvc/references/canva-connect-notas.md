# Canva Connect API — autofill de templates (setup em andamento, 10/09 — fase 2)

**Objetivo**: preencher (autofill) os templates de marca do Rob no Canva com texto/fotos da squad e exportar PNG — Canva integrado ao pipeline de arte.

## Credenciais
- `CANVA_CLIENT_ID` + `CANVA_CLIENT_SECRET` no `.env` do perfil (via `save_env_value`; .env é protegido contra patch/write_file direto).
- API base: `https://api.canva.com/rest/v1`.

## Fluxo OAuth PKCE S256 (validado na prática — URLs CORRETAS da OpenAPI oficial)
1. **Authorize (browser do Rob — curl NÃO passa, Cloudflare challenge)**: `https://www.canva.com/api/oauth/authorize?client_id=...&redirect_uri=...&response_type=code&scope=...&code_challenge=...&code_challenge_method=S256` — ⚠️ **SEM `/api/v1/`** (URL antiga `canva.com/api/v1/oauth/authorize` está errada).
2. **redirect_uri**: `http://127.0.0.1:3001/oauth-redirect` (padrão do starter kit do Canva — **o Rob registrou este no app dele**). Se der "não configurou o URI de redirecionamento": pedir para adicionar exatamente este no Developer Portal → sua integração → Authentication, e reabrir o link.
3. **Escopos — formato com DOIS-PONTOS duplos, sem underscore, separados por espaço**: `asset:read asset:write brandtemplate:meta:read brandtemplate:content:read design:content:read design:content:write design:meta:read folder:read profile:read`.
4. Após autorizar, o browser cai em `http://127.0.0.1:3001/oauth-redirect?code=...` → **ERR_CONNECTION_REFUSED é ESPERADO** (não há servidor local). O Rob copia a URL inteira da barra (Ctrl+L → Ctrl+C) e cola no chat.
5. **Token exchange** (curl OK aqui): `POST https://api.canva.com/rest/v1/oauth/token` form-encoded: `grant_type=authorization_code, code, code_verifier (de canva-pkce.json), redirect_uri (o mesmo do authorize), client_id, client_secret`.
6. **code expira em ~10 min** (JWT iat→exp) — trocar imediatamente ao receber. Refresh: `grant_type=refresh_token` no mesmo endpoint. Guardar tokens em arquivo com chmod restrito + `save_env_value` se for para .env.

## PKCE (geração correta — testada)
```python
import base64, secrets, hashlib, json, pathlib
verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()  # 64 chars, charset seguro
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()  # 43 chars
pathlib.Path("canva-pkce.json").write_text(json.dumps({"code_verifier": verifier, "code_challenge": challenge}))
```

## Erros já vistos e as soluções
- `400 "'code_verifier' must not be null"` ao trocar um code fake → **significa que client_id/secret são VÁLIDOS** (bom teste de sanidade das credenciais).
- Tela "não configurou o URI de redirecionamento" → redirect_uri não registrado no app; adicionar no portal (ver passo 2).
- `error=invalid_scope` ("Requested scopes are not allowed for this client") → **o app NÃO tem escopos marcados no Developer Portal**. Solução: mandar o authorize **SEM o parâmetro `scope`** (o formato do template do portal: `?code_challenge_method=s256&response_type=code&client_id=...&code_challenge=<CHALLENGE>` — `s256` minúsculo; manter `redirect_uri` que já passou na validação). O token sai com escopos vazios — o Rob marca os escopos no portal depois e reautoriza.
- `400 "Invalid code verifier"` na troca com code real → code velho (expirado >10 min) ou emitido com challenge de outro par. **Não debugar o par local** (pode estar consistente e o erro persistir): gerar PKCE NOVO + link novo e pedir para o Rob autorizar de novo.
- `400 "Invalid auth code"` (diferente do de cima) **mesmo com code fresco (58s!)** → **CAUSA RAIZ DESCOBERTA (10/09): truncamento silencioso do code JWT (~1.3k chars) ao colar/reescrever inline dentro do script heredoc**. O code incompleto nem decodifica como JWT (JSONDecodeError). **Solução definitiva: JAMAIS embutir o code em string inline — gravar em `cuidarvc/squad/canva-code.txt` via write_file (conteúdo completo) e o script LER do arquivo** (`pathlib.Path("canva-code.txt").read_text().strip()`). Validar integridade antes de trocar: decodificar o payload base64 do JWT — se parsear JSON com `scopes`, está íntegro. Com isso a troca funcionou de primeira.
- **Curiosidade técnica (não é erro)**: o campo `pckce` embutido no JWT do code NUNCA bate com o `code_challenge` enviado no authorize — e mesmo assim a troca já funcionou com o verifier do par. Não gastar tempo validando pckce do JWT.

## Mapa escopo → endpoint (verificado na OpenAPI oficial — usar p/ montar o `scope` do link)
- `GET /v1/designs` (listar) → `design:meta:read`
- `POST /v1/designs` (criar) → `design:content:write`
- `POST /v1/autofills` → **SÓ `design:content:write`** (não exige escopo de brandtemplate!)
- `POST /v1/asset-uploads` / `POST /v1/url-asset-uploads` → `asset:write`
- `POST /v1/exports` (exportar PNG) → `design:content:read`
- `GET /v1/brand-templates` (LISTAR) → `brandtemplate:meta:read` ⚠️ **Rob deixou este DESMARCADO no portal**
- `GET /v1/brand-templates/{id}/dataset` (slots do template) → `brandtemplate:content:read` ✓ marcado
- Consequência: **autofill funciona sem brandtemplate:meta** — só o LISTAR templates fica fora; pegar o ID do template pela URL do Canva (Rob) e ler o dataset direto.

## Endpoints (OpenAPI oficial: https://www.canva.dev/sources/connect/api/latest/api.yml — 12.9k linhas)
- **Assets: upload é JOB assíncrono** — `POST /v1/asset-uploads` (multipart) ou `POST /v1/url-asset-uploads` (por URL) → `GET /v1/asset-uploads/{jobId}` | `GET /v1/url-asset-uploads/{jobId}`. (NÃO é `POST /v1/assets`; `GET/DELETE /v1/assets/{assetId}` existe para gerenciar.)
- Autofill: `POST /v1/autofills` (brand_template_id + data layers) → `GET /v1/autofills/{jobId}`.
- Templates de marca: `GET /v1/brand-templates`, `GET /v1/brand-templates/{id}`, `GET /v1/brand-templates/{id}/dataset` (slots preenchíveis).
- Designs: `GET/POST /v1/designs`, `GET /v1/designs/{id}` (+analytics, pages, comments).
- OAuth: `/v1/oauth/token`, `/v1/oauth/introspect`, `/v1/oauth/revoke`.

## Cenário squad (pós-token)
foto z-image-turbo → `POST /v1/url-asset-uploads` → autofill no template de marca → export PNG → publicar via Zernio.

## Estado (10/09, pós-validação) — 100% OPERACIONAL: token com escopos + pipeline de publicação VALIDADO
- ✅ Reautorização concluída: code com os 8 escopos → troca com SUCESSO (via write_file, ver Erros) → tokens salvos em `cuidarvc/squad/canva-tokens.json` (access expira em 4h + refresh_token).
- ✅ Sanity check passou: `GET /v1/designs` listou 25 designs do Rob (design:meta:read OK).
- ✅ **Pipeline completo de publicação validado de ponta a ponta** (card 4 do carrossel como cobaia): foto z-image-turbo → `compose_card.py` → **`cuidarvc/squad/canva_publish.py`** (upload asset → create design → export PNG) → PNG final baixado. A arte também fica no Canva do Rob como design editável (ex: card-4 = asset `MAHU10ZQCfs`, design `DAHU1zcSv5w`).
- **Pegadinhas do pipeline (descobertas na validação)**:
  - Upload: `POST /v1/asset-uploads` com header `Asset-Upload-Metadata: {"name_base64": "<nome em base64>"}` (nome máx 50 chars) e **corpo = binário cru** (Content-Type application/octet-stream — NÃO multipart, NÃO JSON com name/content_type → senão "Invalid upload metadata header").
  - Status dos jobs em MINÚSCULO: `"success"`/`"failed"` (comparar com SUCCESS/FAILED falha silenciosamente).
  - Create design: `design_type` tem campo `type` INTERNO: `{"type": "custom", "width": 1080, "height": 1350}` (usar `"name"` → 400 "'type' must not be null").
  - Export: URL do arquivo em `job.urls[0]` (NÃO `result.export.url`).
  - BASE da API: `https://api.canva.com/rest` + paths `/v1/...` (não dobrar o /v1 → 404 endpoint_not_found).
- Renovação: `grant_type=refresh_token` no `/v1/oauth/token` (mesmo endpoint, com client_id/secret).
- Docs llms: `https://www.canva.dev/llms.txt` (índice), `https://www.canva.dev/docs/connect/llms.txt`, quickstart em `/docs/connect/quickstart.md`.
- Canva também tem MCP server oficial (docs/mcp.md) — requer waitlist de redirect URI; não é o caminho atual.
