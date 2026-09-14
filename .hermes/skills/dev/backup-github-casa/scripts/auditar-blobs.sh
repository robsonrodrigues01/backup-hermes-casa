#!/usr/bin/env bash
# auditar-blobs.sh — lista blobs do histórico git acima de um limiar em MB
#   e os arquivos atuais igualmente grandes (fora .git).
# Motivação (14/09): o GitHub RECUSA arquivo >100MB no git (push hard fail)
#   — rodar ANTES do primeiro push. Usa --batch-all-objects, então enxerga
#   até blob fantasma de histórico amendado; após `git reflog expire +
#   gc --prune=now` eles somem daqui também (e o push passa a passar).
# Uso: ./auditar-blobs.sh [limiar_em_MB]   (default 90)
set -euo pipefail

MB=${1:-90}
BYTES=$(( MB * 1000000 ))

echo "== blobs maiores que ${MB}MB no histórico git =="
if git rev-parse --git-dir >/dev/null 2>&1; then
  git cat-file --batch-all-objects --batch-check='%(objectsize) %(objectname)' \
    | awk -v b="$BYTES" '$1 > b {print $1, $2}' \
    | while read -r size hash; do
        nome=$(git rev-list --objects --all 2>/dev/null \
               | grep "^${hash}" | head -1 | cut -d' ' -f2 || true)
        printf '%4d MB  %s\n' $(( size / 1000000 )) "${nome:-(só objeto solto)}"
      done
else
  echo "não é um repo git (rode na raiz que vai pro GitHub)"
fi

echo
echo "== arquivos ATUAIS maiores que ${MB}MB (fora .git) =="
find . -path "$PWD/.git" -prune -o -type f -size +"${MB}"M -print -exec ls -lh {} \; \
  2>/dev/null | awk '{print $5, $NF}' | sort -rh | head -20

echo
echo "fluxo se aparecer blob >100MB: gitignore no caminho +"
echo "  git rm -r --cached <caminho> && git commit --amend &&"
echo "  git reflog expire --expire=now --all && git gc --prune=now"
