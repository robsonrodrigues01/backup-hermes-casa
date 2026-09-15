#!/bin/bash
# Uso de tokens por modelo a partir dos logs do headroom (linhas PERF)
# uso: uso-por-modelo.sh [glob-dos-logs]
#   default: todos os logs da casa (~/.headroom*/logs/proxy.log*)
# saída: tabela modelo | tok_in | tok_out (acumulado de toda a janela dos logs)
set -euo pipefail
LOGS="${1:-$HOME/.headroom*/logs/proxy.log*}"
ls $LOGS >/dev/null 2>&1 || { echo "nenhum log encontrado: $LOGS"; exit 1; }

grep -hoE "PERF model=[^ ]+ msgs=[0-9]+ tok_before=[0-9]+ tok_after=[0-9]+ tok_saved=[0-9]+ tok_inflated=[0-9]+ tool_saved=[0-9]+ total_saved=[0-9]+ cache_read=[0-9]+ cache_write=[0-9]+ cache_hit_pct=[0-9]+ opt_ms=[0-9]+ total_ms=[0-9]+ tok_out=[0-9]+" $LOGS 2>/dev/null \
| sed -E 's/PERF model=([^ ]+).*tok_before=([0-9]+).*tok_out=([0-9]+)/\1 \2 \3/' \
| awk '{
    in_[$1]+=$2; out[$1]+=$3
  } END {
    printf "%-28s %14s %12s\n", "modelo", "tok_in", "tok_out";
    for (m in in_) printf "%-28s %12.1fM %10.1fM\n", m, in_[m]/1e6, out[m]/1e6
  }'
