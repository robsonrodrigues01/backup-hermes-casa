# Zernio API — quirks e endpoints (observados na operação da squad)

## Autenticação
- Chave: `sk_` + 64 hex chars = 67 chars. Enviada no header `Authorization: Bearer ***`. SDKs leem de `ZERNIO_API_KEY`.
- Um key cobre a integração inteira; rate limits escalam com contas conectadas (não com nº de keys).

## Contas
- `GET /v1/accounts` lista contas conectadas. Cada conta tem `_id` (ObjectId 24-hex) e `displayName` (ex: "cuidar.vc" p/ Instagram). Use o `_id` como filtro em analytics e follower-history.
- Campos úteis: `platform`, `isActive` (token ativo?), `enabled` (pode postar?), `followersCount`, `externalPostCount`.
- Erros: `ACCOUNT_DISCONNECTED` (token expirado → reconectar e refresh `GET /v1/accounts`), `PROFILE_OVER_LIMIT`, `ACCOUNT_NOT_ENABLED_FOR_POSTING`.

## Posts e agendamento
- `POST /v1/posts` cria e opcionalmente publica. Agendamento: `scheduledFor` (ISO 8601, lido no `timezone` enviado) OU `publishNow: true` OU `queuedFromProfile`. Sem nenhum → vira draft.
- Precedência: `isDraft` vence; `publishNow` vence `scheduledFor`. `scheduledFor` já no passado → publica síncrono (como publishNow).
- `GET /v1/posts` lista; filtra por `accountId`, `status`, `platform`, `search`.

## Idempotência (crítico p/ não duplicar)
- **Mesmo `x-request-id` (janela 5 min):** segundo request c/ mesmo ID → HTTP 200 c/ post original em `existingPost`, nada novo. Gerar UUID p/ cada post lógico; NUNCA reutilizar um ID entre vários nós de um workflow.
- **Content-hash dedup (24h):** hash `(platform, accountId, content+media)`; duplicata → HTTP 409. Repostar intencional: variar caption/media/conta. Tratar 409 e 200 como retry, não como sucesso.
- Status pós-publish: `published` (tudo certo), `partial` (1+ plataforma publicou, 1+ falhou), `failed` (nada publicou, terminal). Reportar honestamente; não fingir sucesso.

## Analytics
- `GET /v1/analytics/best-time?platform=<p>&accountId=<id>` → melhores horários por dia-da-semana/hora (UTC). ⚠️ **Pode vir `slots: []` quando a conta não tem histórico** (conta nova, ex: cuidar.vc recém-conectada). Nesse caso usar bom senso (picos 12h/20h Brasil) e reportar o vazio, não inventar slot.
- `GET /v1/analytics` → posts e engajamento (filtro accountId; de/até; max 366 dias).
- `GET /v1/analytics/instagram/follower-history?accountId=<id>&metrics=follower_count,followers_gained,followers_lost` → série diária de seguidores (max 89 dias, default 30).
- `GET /v1/analytics/content-decay` → como o engajamento acumula (posts ~78% em 24h).
- Métricas indisponíveis vêm em `unavailableMetrics` (NUNCA reportar como zero). Requer Analytics add-on; incluído em plans usage-based.

## Formato de mídia (Instagram/Facebook)
- **Hashtags**: devem ir no CORPO do conteúdo (não campo separado) p/ Instagram/Facebook.
- Instagram: 1 imagem p/ feed, até 10 p/ carrossel; Reels/Stories exigem `platformSpecificData`/`contentType`.
- Facebook: feed (texto, até 10 imagens, 1 vídeo), Story, Reel; carrossel de 2–10 cards (`carouselCards`, um por imagem em `mediaItems`, mesma ordem/comprimento).

## Upload de media
- `GET /v1/media/presigned-url` presigna URL p/ upload (imagens/vídeos/documentos) antes de usar em posts. Pré-flight: `GET /v1/validate/...`.

## Interação / manter perfil ativo
- `GET /v1/inbox/comments` + `POST /v1/inbox/comments/{postId}/{commentId}/moderation` (approve `published`, remove `rejected`, `heldForReview`) → quizzes/promos respondíveis via comentário.
- `GET /v1/inbox/conversations` (DMs) → responder seguidores; manter perfil ativo 24/7.
- Comment-to-DM automations p/ crescimento (keyword-triggered auto-DMs).

## Endpoints confirmados na operação real (via curl no proxy local / proxy)
- `GET https://api.zernio.com/v1/accounts` → 200 c/ accounts[]. Ex.: conta Instagram `cuidar.vc` (`_id` 6aa2ac82726ebfe037d39c87), isActive true, followersCount 0 (conta nova).
- `GET https://api.zernio.com/v1/analytics/best-time?platform=instagram&accountId=6aa2ac82726ebfe037d39c87` → 200 `{"slots":[]}` (sem histórico ainda).