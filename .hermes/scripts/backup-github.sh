#!/bin/bash
# backup diario casa Hermes -> GitHub cofre privado
# silencio quando nada mudou | avisa quando envia | erro se falhar
cd /home/hermes || { echo "ERRO: casa sumiu"; exit 1; }
git add -A
MUDOU=$(git status --porcelain | wc -l)
if [ "$MUDOU" -eq 0 ] && [ "$(date +%d)" != "01" ]; then
  exit 0
fi

if [ "$MUDOU" -gt 0 ]; then
  git commit -q -m "backup diario: $(date '+%d/%m %Hh') - $MUDOU arquivos" || { echo "ERRO: commit falhou"; exit 1; }
  TENT=0
  while [ $TENT -lt 3 ]; do
    if git push -q origin main 2>/dev/null; then
      echo "backup enviado: $MUDOU arquivos mudaram"
      break
    fi
    TENT=$((TENT+1)); sleep 30
    [ $TENT -eq 3 ] && { echo "ERRO: push falhou apos 3 tentativas"; exit 1; }
  done
fi

# No dia 1 de cada mes: zip completo (inclui os diarios state.db) -> Release
if [ "$(date +%d)" = "01" ]; then
  TAG="cofre-$(date +%Y-%m)"
  ZIP="/tmp/cofre-completo-$(date +%Y%m).zip"
  cd /home/hermes || exit 1
  zip -qr "$ZIP" .hermes 2>/dev/null
  TOK=$(cat "$HOME/secrets/gh-token")
  RH="Authorization: token $TOK"
  cd /tmp && rm -f rel_new.json
  CREAT=$(curl -s -o rel_new.json -w '%{http_code}' -X POST -H "$RH" https://api.github.com/repos/robsoncoffy/backup-live-hermes/releases \
    -d "{\"tag_name\":\"$TAG\",\"name\":\"Cofre completo $TAG\",\"body\":\"Zip casa inteira incluindo historicos (state.db). Gerado dia 1 - substitui o anterior como foto completa.\"}")
  if [ "$CREAT" = "422" ]; then
    rel_new.json=""
    curl -s -H "$RH" -o rel_tag.json "https://api.github.com/repos/robsoncoffy/backup-live-hermes/releases/tags/$TAG"
    mv rel_tag.json rel_new.json
  fi
  UPLOAD=$(python3 -c "import json;print(json.load(open('/tmp/rel_new.json'))['upload_url'].split('{')[0])" 2>/dev/null)
  if [ -n "$UPLOAD" ]; then
    UPSTAT=$(curl -s -o up.json -w '%{http_code}' -X POST -H "$RH" -H "Content-Type: application/octet-stream" \
      --data-binary @"$ZIP" "$UPLOAD?name=cofre-completo-$(date +%Y%m).zip")
    if [ "$UPSTAT" = "201" ]; then
      echo "cofre mensal ($TAG): zip completo enviado ($(du -h "$ZIP" | cut -f1))"
    else
      echo "ERRO: upload do zip mensal falhou (http $UPSTAT)"
    fi
  else
    echo "ERRO: release mensal nao criou upload url"
  fi
  rm -f /tmp/rel_new.json /tmp/up.json "$ZIP" rel_tag.json /tmp/rel_tag.json
fi
