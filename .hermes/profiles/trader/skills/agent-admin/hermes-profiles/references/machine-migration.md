# Machine migration runbook (proven 2026-09-12 on the 6-profile home: default/era4/cuidar/lab/cmo/cto)

## What `hermes backup` includes (verified from hermes_cli/backup.py source + live run)
- Whole `~/.hermes` EXCEPT: the hermes-agent codebase, `__pycache__`, `.git/`, `node_modules`, `backups/`, `checkpoints/`, `*.pyc`/`*.pyo`, SQLite sidecar files (`.db-wal` / `.db-shm` / `.db-journal` — the `*.db` is snapshotted via the `sqlite3 backup()` API for a consistent copy), `gateway.pid`, `cron.pid`.
- `profiles/` IS included: every profile's full state — `config.yaml`, `.env` (**with bot tokens and API keys**), `SOUL.md`, `memories/`, `skills/`, `cron/`, `sessions/`, `state.db`. Nothing to recreate on BotFather or re-permission: the bots are literally the same tokens.
- Live numbers on this home: 980 MB home → 8561 files → 334 MB zip in ~27 s. Per-profile sizes at the time: cuidar 250M, lab 117M, era4 106M, cto 85M, cmo 65M.
- Variants: `hermes backup --quick -l <label>` = critical-state-only snapshot (config, state.db, .env, auth, cron) — fast daily backup, not enough alone for a machine move; `hermes profile export <name> -o <name>.tar.gz` + `hermes profile import` = per-profile archive when moving only one profile.
- Import is an overlay restore onto the current HERMES_HOME root (`hermes import <zip>`, `--force` to overwrite existing files without asking).

## Runbook — old machine
1. `hermes backup -o ~/hermes-mudanca.zip` (use terminal background mode for big homes; ran ~30 s here).
2. Copy the zip OFF the box: `scp hermes@<old-ip>:~/hermes-mudanca.zip .` — the zip carries every bot token; keep it out of screenshots/shared folders.
3. ⚠️ Cut-over rule (same physics as the cloned-token pitfall): **before starting gateways on the new machine**, kill them all on the old one: `export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; systemctl --user disable --now 'hermes-gateway-*.service'`. One bot token = one poller; two live pollers → 409 conflicts and messages routed to the wrong host. Headroom proxies don't conflict on tokens but disable too for a clean start.

## Runbook — new machine
1. Install the CLI: `uv tool install hermes-agent` (match the old machine's version — run `hermes --version` on both sides).
2. `hermes import ~/hermes-mudanca.zip` → profile wrapper scripts (`era4`, `cuidar`, … in `~/.local/bin/`) are recreated automatically during import; the command prints the "re-enable gateway services" list at the end.
3. `hermes profile list` — all profiles back, gateways stopped. Headroom `base_url` plumbing inside each profile's `config.yaml` came in the zip (only the proxy *service* needs reinstalling).
4. Re-enable each gateway: `printf 'y\ny\n' | hermes -p <name> gateway install` (two Y/n prompts). Default profile's unit has NO suffix: `hermes-gateway.service`.
5. Headroom: reinstall its venv once (`uv pip install --python ~/headroom-test/venv/bin/python "headroom-ai[proxy]"`), recreate the per-profile units per `references/local-proxy-headroom.md`, `curl :<port>/readyz` per port.
6. Hand-over: do the old-machine kill (step 3 above) BEFORE this point if not yet done.

## Verification checklist
- `hermes profile list` — all profiles show gateway `running`
- Headroom ports 8787/8788/8789/8790 → HTTP 200 on `/readyz`
- Message each bot on Telegram → reply arrives AND `journalctl --user -u hermes-gateway-<name>` on the new machine shows the hit; zero 409 lines in the journals
- `hermes -p <name> cron list` on each profile matches the old machine's boards (briefing-matinal `0 12 * * *` etc.)
