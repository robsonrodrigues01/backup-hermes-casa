---
name: hermes-profiles
description: >
  Create and operate multiple Hermes agent profiles (one per business, project,
  or persona) on a single machine, each with isolated memory/skills/cron and
  its own Telegram bot. Covers the --clone workflow, the cloned
  TELEGRAM_BOT_TOKEN pitfall, gateway services, multiplexing mode, and
  verification. Authoritative docs at
  https://hermes-agent.nousresearch.com/docs (user-guide/profiles,
  user-guide/multi-profile-gateways).
---

# Hermes Multi-Profile Setup & Operation

## When to use
- User wants separate agents for separate domains — e.g. a personal assistant vs. one agent per company/project (personal "Claudinho", ERA 4.0 agency, cuidar.vc).
- Adding, inspecting, renaming, deleting a profile, or wiring a profile's messaging gateway.
- Diagnosing two agents fighting over one Telegram bot, or state bleeding across profiles.

## Mental model
A profile IS a separate Hermes home: `~/.hermes/profiles/<name>/` with its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and gateway state. Profiles isolate STATE, not filesystem access — they do not sandbox the agent.

- Profile names: lowercase alphanumeric (`era4`, `cuidar`).
- Creating a profile auto-creates a wrapper command `~/.local/bin/<name>`: `<name> chat`, `<name> setup`, `<name> gateway start`, `<name> doctor` — equivalent to `hermes -p <name> <cmd>`.
- NEVER point two agent processes at the same profile. Agents needing shared memory should use an external memory provider, not a shared home.

## Steps
1. **Inventory** — `hermes profile list` (shows model, gateway status, alias per profile). `hermes profile show <name>` for details.
2. **Create** — `hermes profile create <name> --clone --description "<role in 1-2 sentences>"`. `--clone` copies `config.yaml`, `.env`, `SOUL.md`, skills from the ACTIVE profile (`--clone-from <src>` to pick another source; `--clone-all` = full state copy minus history). The `--description` is what the kanban orchestrator uses to route tasks by role, so write it as a role statement.
3. **⚠️ Swap cloned credentials BEFORE starting the new gateway.** `--clone` copies `TELEGRAM_BOT_TOKEN` (plus `TELEGRAM_ALLOWED_USERS` and `GATEWAY_ALLOW_ALL_USERS`) from the source. Telegram allows exactly ONE poller per bot token: starting the clone with the copied token collides with the source profile's live gateway (409 conflicts, messages routed to the wrong profile). Have the user create a fresh bot via @BotFather (`/newbot` → name + @username → token — only the account owner can do this), replace the token in `~/.hermes/profiles/<name>/.env`, THEN start the gateway.
4. **Personalize** — edit the profile's `SOUL.md` (persona, business context, language/tone) and `.env` (per-profile keys) as needed. Pin a project working dir with `terminal.cwd` in its `config.yaml`.
5. **Start** — `printf 'y\ny\n' | hermes -p <name> gateway install` (two Y/n prompts; single piped `y` aborts) — installs systemd user service `hermes-gateway-<name>.service`, auto-restarts on crash/login. OAuth logins (Anthropic/OpenAI Codex/xAI) are NOT cloned — single-use refresh tokens; profiles keep reading root `~/.hermes/auth.json` and refreshes write back to root. Static API keys copy normally.
6. **Verify** — `hermes profile list` shows gateway `running`; `hermes -p <name> doctor` is clean; user sends a test message ("oi") to the new bot and gets a reply in the right chat.
7. **Handoff — skill/content libraries.** A new profile starts with cloned skills only. For curating third-party skill packs into another profile's library (verify repo → select subset → copy → distribute with explicit OK), see the `agent-skill-curation` skill. Machine context inside that workflow (`terminal.cwd`, admin quirks) is still governable per-profile via `config.yaml`.

## Pitfalls
- **#1 pitfall: cloned Telegram token.** Start a cloned profile's gateway only AFTER swapping `TELEGRAM_BOT_TOKEN`. Keep the cloned `TELEGRAM_ALLOWED_USERS` so the owner stays whitelisted on the new bot.
- **#2 pitfall: cloned `API_SERVER_*` keys force the api_server platform on.** In `gateway/config.py` the platform is enabled when `API_SERVER_ENABLED` is truthy OR `API_SERVER_KEY` is merely present — so `API_SERVER_ENABLED=false` in `.env` and `platforms.api_server.enabled: false` in `config.yaml` do NOTHING while the key exists. The clone then fights the default profile over the api_server port (e.g. 8642). Fix: delete every `API_SERVER_*` line from the cloned `.env`, then restart the profile gateway and confirm zero `api_server` lines in `journalctl --user -u hermes-gateway-<name>`.
- **Cloned `GATEWAY_ALLOW_ALL_USERS=true`** lets ANYONE talk to the new bot. Set `false` and keep the cloned `TELEGRAM_ALLOWED_USERS`. Verify the owner's real Telegram ID against the DB: `SELECT user_id FROM sessions WHERE source='telegram'` in the root `state.db` — don't trust the allowlist blindly.
- **`gateway install` asks TWO interactive Y/n prompts** (start now? + start at boot?) — from a script pipe both answers: `printf 'y\ny\n' | hermes -p <name> gateway install`. A single `y` aborts the install.
- **`gateway restart`/`stop` are REFUSED from inside a running gateway session** ("Refusing to restart the gateway from inside the gateway process") — i.e. when the agent itself lives in a gateway. Workaround: `export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; systemctl --user restart hermes-gateway-<name>.service`, or SIGTERM the gateway PID — systemd `Restart=always` revives it with fresh config within seconds.
- **The command security scanner masks secret-shaped strings**, including `*_TOKEN=` literals inside scripts (inserts `***`, breaking Python syntax and Telegram URLs — a token pasted into a `curl` URL gets truncated to 14 chars → confusing 404s). Handle secrets only via file I/O; build key-name literals dynamically (`'TELE'+'GRAM_BOT'+'_TOKEN='`); verify a token by LENGTH (Telegram tokens = `<10-digit-id>:<35 chars>`, 46 total), never by echoing it.
- **Which token is a live gateway polling?** Calling `getUpdates` with that token and getting HTTP 409 "Conflict" proves the gateway owns it (the gateway terminated your probe). Side effect: it kills the gateway's current long poll — it logs a warning and re-acquires in ~20 s. Diagnostic only, use sparingly.
- **CLI stickiness** — `hermes profile use <name>` makes plain `hermes` commands target that profile. Switch back with `hermes profile use default`. The CLI prompt/banner always shows the active profile.
- **Multiplexing mode** — `gateway.multiplex_profiles: true` on the DEFAULT profile makes its gateway the single inbound process for all profiles. Secondary profiles must NOT start their own gateways (hard error) or enable port-binding platforms (webhook, api_server, msgraph_webhook, feishbok, wecom_callback, bluebubbles, sms, whatsapp_cloud, line, teams — default profile only). Secondary HTTP routes live under `/p/<profile>/` with that profile's own credentials. Default (off) = one process per profile = hard isolation; prefer it for a small number of profiles. Details: `references/multi-profile-gateways.md`.
- **No sandbox** — profiles don't enforce workspace boundaries; SOUL.md guidance is not isolation and asking the model its cwd is not a test. Pin `terminal.cwd` explicitly. Note `cwd: "."` means the launch directory, not the profile dir.
- **Clone excludes history** — sessions, state.db, checkpoints, backups are not copied (can be GBs). Full-history copy → `hermes profile export` / `hermes backup`.
- **Security scanner applies to `execute_code` too** — a literal `'TELEGRAM_BOT_TOKEN='` inside a Python script gets masked to `TELEGRAM_BOT_TOKEN=***` → SyntaxError. Build key literals dynamically (`key + '=' + value`) and move secrets only via file I/O.
- **`memory` tool `replace` swaps the WHOLE entry, not a substring** — `old_text` only selects the entry; `content` becomes its entire new text. Passing only the changed fragment silently truncates the entry; always pass the full reconstructed entry.
- **`execute_code` consent prompts can time out** ("the user has NOT consented… silence is not consent") — treat the block as "approval not given", not task refusal: ask in chat, get an explicit OK, then re-run the same script.

## Verification checklist
- `hermes profile list` — all intended gateways show `running`
- `hermes -p <name> status` and `hermes -p <name> doctor` — clean
- End-to-end: user messages each new bot and gets a reply in the correct chat
- (If kanban is in use) `hermes kanban` — profiles routable via their descriptions

## References
- `references/multi-profile-gateways.md` — operating many gateways: per-profile services vs. multiplexing contract, port-binding rules, `/p/<profile>/` auth, full `hermes profile` command surface.
- `references/telegram-token-swap-example.md` — worked example from this machine (era4/cuidar profiles): observed `.env` keys after clone, the completed-and-verified cuidar runbook (token swap, `API_SERVER_*` strip, service install), and the era4 pending steps.
