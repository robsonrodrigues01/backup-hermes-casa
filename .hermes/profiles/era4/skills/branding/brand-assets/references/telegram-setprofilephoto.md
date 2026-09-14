# Foto de perfil do bot via Telegram Bot API — receita validada

Fonte oficial: core.telegram.org/bots/api#setmyprofilephoto (também existe `removeMyProfilePhoto`, sem parâmetros).

## Descoberta central
O campo `photo` do método é do tipo **InputProfilePhoto** (objeto JSON-serializado), **não** um InputFile solto:

- `InputProfilePhotoStatic`: `{"type":"static","photo":"attach://<file_attach_name>"}` — o anexo viaja no mesmo multipart/form-data, numa parte nomeada `<file_attach_name>`; formato **.JPG**; fotos de perfil "can't be reused" → sempre upload novo, nunca file_id de foto anterior.
- `InputProfilePhotoAnimated` existe (type "animated", campo `animation`, MPEG4) — ainda não testado.

## Receita validada (python requests)

```python
import os, requests, json
token = os.environ["TELEGRAM_BOT_TOKEN"]  # carregado via shell: set -a; . ~/.hermes/profiles/era4/.env; set +a
data = {"photo": json.dumps({"type": "static", "photo": "attach://img"})}
files = {"img": ("pfp.jpg", open("/tmp/era4_pfp/pfp.jpg", "rb").read(), "image/jpeg")}
r = requests.post(f"https://api.telegram.org/bot{token}/setMyProfilePhoto", data=data, files=files, timeout=60)
# HTTP 200 {"ok":true,"result":true}
```

## Tabela erro→causa (debugging real de 2026-09-09)

| Resposta | Causa |
|---|---|
| `400 "photo isn't specified"` | campo `photo` recebendo o binário em multipart direto (curl `-F "photo=@arquivo"` e requests `files={"photo": ...}`) — o método não parseia InputFile solto |
| `400 "can't parse photo JSON object"` | campo `photo` presente (ex.: form-urlencoded com file_id) mas não é o objeto JSON `{"type":"static",...}` |
| `200 {"ok":true,"result":true}` | aplicado; novo avatar aparece na lista de chats do usuário em segundos |

JPG é o formato documentado para foto estática — converter sempre, mesmo que PNG pareça ser aceito pelo `sendPhoto` (que aceita, mas é outro método).

## Passos recomendados
1. Validar token: `curl -s "$URL/getMe"` (URL montada no shell a partir do token em .env) → `ok:true` confirma bot e permissões.
2. Converter PNG→JPG: `Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92)`.
3. POST conforme receita acima.
4. Diagnóstico de multipart em dúvida: `sendPhoto` com os mesmos bytes para o chat do usuário (multipart clássico funciona lá) — resultando `200`, o problema está no método específico, não no upload.
5. Consultar a doc quando um campo está "esquisito": `curl -sS https://core.telegram.org/bots/api -o /tmp/botsapi.html` e grepar o trecho via python (strip de tags) — evita adivinhar assinatura.

## Segurança do token
- Carregar no shell: `set -a && . ~/.hermes/profiles/era4/.env && set +a`; python lê via `os.environ["TELEGRAM_BOT_TOKEN"]`.
- Nunca: `cat` do .env, regex/eco do token no output, heredoc python contendo o valor do token (o security scan pode bloquear padrão de upload de credenciais).