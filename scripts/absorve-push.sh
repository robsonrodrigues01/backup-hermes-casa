#!/bin/bash
# absorve clones + empacota + empurra pro cofre do GitHub (one-shot)
cd /home/hermes || exit 1
STASH="$HOME/nested-git-stash"; mkdir -p "$STASH"
N=0
for p in .hermes/plugins/agent-vision-toolkit .hermes/plugins/gbrain .hermes/plugins/postiz-app headroom-test/headroom tools/agent-reach tools/last30days-skill tools/scan-okjpg/agent-context-kit tools/scan-okjpg/agente-orquestrador tools/scan-okjpg/gbrain tools/scan-okjpg/skill-creator tools/scan-okjpg/skills; do
  if [ -e "$p/.git" ]; then mv "$p/.git" "$STASH/$(echo "$p" | tr '/' '_')"; fi
  git rm -q --cached --ignore-unmatch "$p" 2>/dev/null
  git add -- "$p" 2>/dev/null
  N=$((N+1))
done
echo "absorvidos: $N"
git add -A
git commit -q -m "conteudo real das libs/projetos no cofre + README + regras de segredos"
echo "commit: $(git log --oneline -1)"
git config http.postBuffer 524288000
git gc -q --prune=now 2>/dev/null
echo "PACK: $(git count-objects -vH | grep size-pack)"
git push -u origin main 2>&1 | grep -vE '^(remote:|Objects|Delta|Total)' | tail -6
echo "EXIT_PUSH=${PIPESTATUS[0]}"
