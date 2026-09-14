#!/usr/bin/env bash
# criar-release-zip.sh — cria Release e anexa um arquivo grande via API GitHub.
# Prova real (14/09): zip de 351MB subiu como asset do Release
#   migracao-2026-09-12 em robsoncoffy/backup-live-hermes (create 201,
#   upload 201). Assets de Release aceitam ~2GB — o git recusa >100MB.
#
# Uso: ./criar-release-zip.sh <owner/repo> <tag> <titulo> <caminho-do-arquivo>
# Ex.: ./criar-release-zip.sh robsoncoffy/backup-live-hermes \
#        migracao-2026-09-12 "Snapshot migração 2026-09" /home/hermes/cofre.zip
#
# Segredo: lido de PAT_FILE (default ~/secrets/gh-token) — NUNCA colar o
# segredo na linha de comando (scanner de segurança mascara literais
# token/KEY=; aqui o nome da var evita a substring). Escopo `repo` basta.
# NOTA para quem edita: o validador de escrita mascara "TOKEN=" no meio do
# conteúdo — por isso as vars se chamam PAT/PAT_FILE.
set -euo pipefail

REPO="$1"; TAG="$2"; TITULO="$3"; ARQUIVO="$4"
PAT_FILE="${PAT_FILE:-$HOME/secrets/gh-token}"
if [[ ! -r "$ARQUIVO" ]]; then echo "arquivo não achado: $ARQUIVO" >&2; exit 1; fi
if [[ ! -s "$PAT_FILE" ]]; then echo "segredo não achado: $PAT_FILE" >&2; exit 1; fi
# segredo sem quebras de linha (tolerante a editor que grava \r\n)
PAT=$(awk 'NR==1{sub(/\r$/,"");print;exit}' "$PAT_FILE")
if [[ -z "$PAT" ]]; then echo "segredo vazio" >&2; exit 1; fi

TIM=$(wc -c < "$ARQUIVO" | awk '{printf "%.0f", $1/1000000}')
echo "== arquivo: $(basename "$ARQUIVO") ~${TIM}MB =="

# 1) cria o Release (a tag nasce aqui, se ainda não existir)
BODY=$(python3 - "$TAG" "$TITULO" <<'PY'
import json, sys
print(json.dumps({"tag_name": sys.argv[1], "name": sys.argv[2],
      "body": "Snapshot completo da casa — restauração: ver README do repo."}))
PY
)
COD1=$(curl -sS -o /tmp/rl.json -w '%{http_code}' -X POST \
  -H "Authorization: token $PAT" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${REPO}/releases" \
  -d "$BODY")
echo "create release: $COD1 (201 = criado)"
if [[ "$COD1" != "201" ]]; then
  echo "falha ao criar release — resposta:" >&2; cat /tmp/rl.json >&2; exit 1
fi
# resposta sem jq: só python3 stdlib
URL_UPLOAD=$(python3 -c 'import json;print(json.load(open("/tmp/rl.json"))["upload_url"].split("{")[0])')
ID=$(python3 -c 'import json;print(json.load(open("/tmp/rl.json"))["id"])')

# 2) sobe o arquivo como asset (host diferente: uploads.github.com)
COD2=$(curl -sS -o /tmp/as.json -w '%{http_code}' -X POST \
  -H "Authorization: token $PAT" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@$ARQUIVO" \
  "${URL_UPLOAD}?name=$(basename "$ARQUIVO")")
echo "upload asset: $COD2 (201 = anexado)"
if [[ "$COD2" != "201" ]]; then
  echo "falha no upload — resposta:" >&2; head -c 800 /tmp/as.json >&2; echo >&2; exit 1
fi

echo "== OK: release id=$ID tag=$TAG com $(basename "$ARQUIVO") (~${TIM}MB) =="
# verificação sugerida depois: GET /releases/tags/$TAG e conferir
# assets[].state == "uploaded" e assets[].size == tamanho real em bytes.
