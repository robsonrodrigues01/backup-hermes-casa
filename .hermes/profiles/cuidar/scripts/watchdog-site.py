"""Watchdog do site cuidar.vc (cron no_agent, a cada 15 min).

Comportamento:
- Site OK -> silencio absoluto (stdout vazio = nada enviado ao Rob).
- Fora do ar -> alerta UMA vez (apos 2 falhas seguidas) e fica silencioso enquanto continuar fora.
- Volta a responder -> mensagem unica de recuperacao.

Overrides para teste: WATCHDOG_URL, WATCHDOG_STATE.
"""
import json
import os
import sys
import urllib.request

URL = os.environ.get("WATCHDOG_URL", "https://cuidar.vc")
STATE_FILE = os.environ.get(
    "WATCHDOG_STATE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "watchdog-site-state.json"),
)
TIMEOUT = 15


def check_ok():
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "cuidarvc-watchdog/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"up": True, "fails": 0}


def save_state(st):
    with open(STATE_FILE, "w") as f:
        json.dump(st, f)


ok = check_ok()
st = load_state()

if ok:
    if not st.get("up", True):
        save_state({"up": True, "fails": 0})
        print("SITE DE VOLTA: " + URL + " respondeu OK novamente. Watchdog normalizado.")
    else:
        save_state({"up": True, "fails": 0})
    sys.exit(0)

# Site fora do ar
if st.get("up", True):
    fails = st.get("fails", 0) + 1
    if fails >= 2:
        save_state({"up": False, "fails": 0})
        print("SITE FORA DO AR: " + URL + " falhou em 2 checagens seguidas (~30 min). Verificar hospedagem (Lovable) urgente.")
    else:
        save_state({"up": True, "fails": fails})
    sys.exit(0)

# Continua fora e ja alertou: silencio
sys.exit(0)
