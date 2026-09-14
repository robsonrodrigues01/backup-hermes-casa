#!/bin/bash
# cria o release "Migração 12/09" e sobe o zip de 334MB como anexo
cd /tmp || exit 1
rm -f rel_mig.json upm.json
CODE=$(curl -s -o rel_mig.json -w '%{http_code}' -X POST \
  -H "Authorization: token $(cat "$HOME/secrets/gh-token")" \
  https://api.github.com/repos/robsoncoffy/backup-live-hermes/releases \
  -d '{"tag_name":"migracao-2026-09-12","name":"Migração de servidor 12/09/2026","body":"Foto completa da casa gerada em 12/09 (kit de mudança). Restaura com: hermes import","draft":false,"prerelease":false}')
echo "create: $CODE"
UP=$(python3 -c "import json;print(json.load(open('/tmp/rel_mig.json'))['upload_url'].split('{')[0])" 2>/dev/null)
echo "url: ${UP:0:60}..."
if [ -n "$UP" ]; then
  ST=$(curl -s -o upm.json -w '%{http_code}' -X POST \
    -H "Authorization: token $(cat "$HOME/secrets/gh-token")" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @/home/hermes/hermes-mudanca.zip \
    "$UP?name=hermes-mudanca.zip")
  echo "upload: $ST"
  if [ "$ST" = "201" ]; then
    python3 -c "import json;d=json.load(open('/tmp/upm.json'));print('asset ok:',d.get('name'),round(d.get('size',0)/1000000),'MB')"
  fi
fi
rm -f /tmp/rel_mig.json /tmp/upm.json
