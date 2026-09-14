# Zernio API — notas verificadas (10/09)

Autenticação: `Authorization: Bearer *** chave em /home/hermes/cuidarvc/squad/zernio-key.txt.

## Endpoints confirmados via teste real
- **Contas:** `GET /api.zernio.com/v1/accounts` → 200 com conta cuidar.vc ativa (campo `_id`; displayName identifica; a lista pode vir vazia/0 itens quando a conta não tem dados — trata erro de extração).
- **Upload de mídia (Agente 5: fluxo completo):**
  1. `POST /v1/media/presign` com body `{"platform":"instagram","accountId":"<id>","mediaType":"image","extension":"jpg","filename":"<nome>.jpg","contentType":"image/jpeg"}` → 200 com `uploadUrl` (S3/R2), `publicUrl`, `key`, `expiresIn:3600`.
  2. `PUT` no `uploadUrl` (S3/R2) — **verificado 11/09**: SEM `Authorization` (Bearer no PUT faz o R2 pedir AWS4-HMAC) e SEM headers extras (`x-amz-*` dão SignatureDoesNotMatch); APENAS o mesmo `Content-Type` do presign (ex.: image/png).
  3. Agendar/postar: `POST https://api.zernio.com/v1/posts` com `content` (hashtags inline no corpo), `mediaItems: [{"url": publicUrl, "type": "image"}]`, `scheduledFor` local sem Z (ex.: `"2026-09-11T07:00:00"`) + `timezone: "America/Sao_Paulo"`, `platforms: [{"platform":"instagram","accountId":"<id>"}]` → 201, post.status `scheduled`. Script completo verificado 11/09: `squad/zernio_agendar.py`.
  - Erros comuns no presign (400): faltou `filename`; faltou `contentType` (aceita image/jpeg|png|webp|gif|video/mp4|pdf|audio/* etc).
- **Melhor horário:** `GET /v1/analytics/best-time?platform=instagram&accountId=<id>` → `slots:[]` (vazio) quando conta nova (0 seguidores). Agente 5 usa bom senso (12h e 20h no Brasil) até acumular histórico; REPORTE o vazio.
- **Status de posts (verificado 12/09):** listagem `GET /v1/posts` → 200, a lista vem na chave **`posts`** (NÃO `items`); cada item traz `_id`, `status` (`scheduled`/`published`/`partial`/`failed`), `scheduledFor` e `platforms[]` com status por rede (ex.: instagram `published` + facebook `published`). ⚠️ O GET individual `GET /v1/posts/<id>` retorna `status: null` e `platforms: []`: não serve p/ checagem, usar SEMPRE a listagem. Remoção manual no Instagram NÃO reflete na API (o post segue listado como `published`). Rotina de fechamento do CMO (18h): script pronto `squad/cmo_fechamento_check.py` (lista todos os posts com status por plataforma).

## PITFALL — paths reais
Os paths de API reais estão em `https://zernio.com/openapi.json` (483 paths). Listar posts NÃO é `/v1/media/list-posts` (dá endpoint_not_found). Reais: `/v1/media/presign` e `/v1/media/upload-direct`. Não re-consulte a doc a cada vez — use este arquivo.

## Idempotência e retries
- Zernio deduplica (platform, accountId, content+media) em 24h (409); retries com mesmo x-request-id retornam 200. Sempre variar caption/media para repost; gerar UUID por post lógico.

## Receita segura: curl com header de auth (verificada 10/09)
Nunca montar `-H "Authorization: Bearer $KEY"` inline em scripts — aspas aninhadas quebram o bash de forma silenciosa (unexpected EOF) e geram loops de reescrita. Padrão que funciona:
1. `write_file` cria o arquivo de header com o valor COMPLETO (ex: `squad/zernio.hdr` — formato: `Authorization: Bearer sk_...`).
2. curl com `-H @zernio.hdr` e payloads em arquivo com `-d @payload.json`.

O header pronto já existe em `/home/hermes/cuidarvc/squad/zernio.hdr`. Aplica-se a qualquer API com Bearer (Zernio, Piapi, Krea).