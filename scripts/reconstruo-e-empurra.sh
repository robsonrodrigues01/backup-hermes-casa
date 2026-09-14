#!/bin/bash
cd /home/hermes || exit 1
kill 365857 2>/dev/null
rm -rf .git
git init -q -b main
git config user.name 'Rob (backup automatico)'
git config user.email 'rob-backup@era4.local'
git config http.postBuffer 524288000
git add -A
echo "TRACKED: $(git ls-files | wc -l)"
git commit -q -m "backup inicial: casa Hermes completa (perfis + projetos + ferramentas)"
git remote add origin https://github.com/robsoncoffy/backup-live-hermes.git
git gc -q --prune=now
echo "PACK: $(git count-objects -vH | grep size-pack)"
git push -u origin main --progress 2>&1 | grep -vE '^remote: (Enumerating|Counting|Compressing)' | tail -8
echo "EXIT_PUSH=${PIPESTATUS[0]}"
