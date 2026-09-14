#!/usr/bin/env python3
"""Camera forense 20Hz: fotografa todo pid NOVO cuja cmd envolve gateway/dashboard/systemctl,
registrando ppid + cmd do PAI imediatamente (antes do pai morrer)."""
import os, time, signal

LOG = "/home/hermes/tools/forense.log"
PATTERNS = ("gateway run", "dashboard --host", "systemctl")
dead_marker_pid = 0

def runcmd(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return f.read().replace(b"\0", b" ").decode(errors="replace").strip()
    except Exception:
        return f"<zumbi {pid}>"

seen = {}
with open(LOG, "a", buffering=1) as out:
    out.write(f"cam-start {time.strftime('%FT%TZ', time.gmtime())}\n")
    deadline = time.time() + 1080  # 18 min de runtime
    while time.time() < deadline:
        try:
            pids = os.listdir("/proc")
        except Exception:
            continue
        for p in pids:
            if not p.isdigit() or p in seen:
                continue
            seen[p] = 1
            cmd = runcmd(p)
            if not cmd:
                continue
            if any(k in cmd for k in PATTERNS):
                try:
                    with open(f"/proc/{p}/stat") as f:
                        ppid = int(f.read().split(") ", 1)[1].split()[1])
                except Exception:
                    ppid = -1
                pcmd = runcmd(ppid) if ppid > 0 else ""
                out.write(f"NEW {time.strftime('%FT%T', time.gmtime())}.{int(time.time()*100)%1000:03d} pid={p} ppid={ppid}\n")
                out.write(f"    pid-cmd: {cmd[:200]}\n")
                out.write(f"    pai-cmd: {pcmd[:200]}\n")
        time.sleep(0.05)
    out.write("cam-fim\n")
