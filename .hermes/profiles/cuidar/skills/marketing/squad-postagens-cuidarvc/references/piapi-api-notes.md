# Piapi API — notas verificadas (10/09)

Chave: 64 hex sem prefixo, salva em /home/hermes/cuidarvc/squad/piapi-key.txt.

## Estado verificado via teste real
- **Endpoints:** base URL `https://api.piapi.ai`. Único endpoint OpenAI-compat confirmado: `POST /v1/chat/completions`. `/v1/task/*` dão 404.
- **PITFALL:** a doc oficial (`https://piapi.ai/docs/overview`) é JS-rendered (mintlify) e NÃO expõe o header exato de autenticação. Quando for configurar o Agente 3 para um provider, extraia o endpoint de `https://piapi.ai/openapi.json` ou da doc mintlify de cada provider (ex: `/docs/flux-api/text-to-image` + `get-task`).
- **Fato do teste:** o endpoint de criação de imagem `/api/v1/task` respondeu `401 "Failed to verify api key"` com a chave crua (sem sk-) e também com sk- prefixado — ou seja, a Piapi rejeitou a chave como está em ambas as formas. **Update (10/09 à noite)**: screenshot da conta Piapi mostra DUAS chaves — a "Initial Key" (debe2e07…, a rejeitada nos testes) e uma mais nova chamada **"Bot"** (0169ef5b…, criada 15:21), provavelmente a válida — pedir ao Rob o valor completo da "Bot" e retestar `/api/v1/task`.

## Alternativa em avaliação — Krea AI (MCP)
Server MCP `krea-ai` (https://api.krea.ai/mcp) já salvo no config do Hermes (disabled) — habilitar com API key em `MCP_KREA_AI_API_KEY` no .env do perfil. Pode substituir/complementar a Piapi na geração de arte do Agente 3.

## Fluxo por provider (leitura obrigatória antes de gerar arte)
Cada provider da Piapi (flux/midjourney/kling) tem doc própria com create-task/get-task. Ler a doc específica antes de chamar o endpoint. Não re-consulte a doc a cada vez — use este arquivo + openapi.json.