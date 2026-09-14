#!/bin/bash
# Câmera de vigilância: fotografa processos hermes novos e a genealogia deles
LOG=/home/hermes/tools/ghost-camera.log
echo "cam start $(date -u +%FT%TZ)" > "$LOG"
BASE=$(ps -eo pid=,args= | grep -E "hermes (_c|cla)?" | grep -E "gateway|dashboard" | grep -v grep | awk '{print $1}' | sort)
for i in $(seq 1 900); do
  NOW=$(ps -eo pid=,ppid=,args= | grep -E "gateway run|dashboard" | grep -v grep | grep -v "watch-ghost")
  NEWP=$(comm -13 <(echo "$BASE" | sort) <(echo "$NOW" | awk '{print $1}' | sort))
  if [ -n "$NEWP" ]; then
    {
      echo "=== NOVO PROCESSO $(date -u +%FT%.3Z) ==="
      echo "$NOW" | grep -E "^ *($(echo $NEWP | tr ' ' '|')) "
      for p in $NEWP; do
        PP=$(ps -o ppid= -p $p 2>/dev/null | tr -d ' ')
        echo "-- pid $p pai=$PP证件: $(cat /proc/$p/cgroup 2>/dev/null | tail -1)"
        C=$p
        for k in 1 2 3 4 5 6; do
          [ -z "$C" ] && break
          ps -o pid=,ppid=,args= -p "$C" 2>/dev/null | head -1
          C=$(ps -o ppid= -p "$C" 2>/dev/null | tr -d ' ')
          [ "$C" = "1" ] || [ "$C" = "0" ] && break
        done
      done
    } >> "$LOG"
    BASE=$(echo "$NOW" | awk '{print $1}' | sort)
  fi
  sleep 1
done
echo "cam fim $(date -u +%FT%TZ)" >> "$LOG"
