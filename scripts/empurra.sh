#!/bin/bash
cd /home/hermes || exit 1
git remote remove origin 2>/dev/null
git remote add origin https://github.com/robsoncoffy/backup-live-hermes.git
echo "TRACKED: $(git ls-files | wc -l)"
git count-objects -vH | grep -E '^(count|size-pack)'
git gc -q --prune=now
echo "GC: $(git count-objects -vH | grep -E '^(count|size-pack)')"
git push -u origin main --progress 2>&1 | grep -vE '^(remote: Enumerating|remote: Counting|remote: Compressing)' | tail -8
echo "EXIT_PUSH=${PIPESTATUS[0]}"
