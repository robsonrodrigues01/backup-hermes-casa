# Multi-Profile Gateways — Operating Notes

Condensed from https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways
and /docs/user-guide/profiles (Docusaurus site; pages exist under /docs/).

## One process per profile (default; preferred for few profiles)
- Every profile runs its own gateway with its own bot token:
  `<name> gateway install && <name> gateway start`
- Linux service: systemd user unit `hermes-gateway-<name>.service`; macOS: LaunchAgent
  `ai.hermes.gateway-<name>.plist`. Auto-restart on crash, starts on login.
- Hard isolation: separate memory footprints, independent crash domains, restart one
  without touching the others.

## Multiplexing mode (opt-in, off by default)
Enable on the DEFAULT profile — it owns the multiplexer:

    hermes config set gateway.multiplex_profiles true
    hermes gateway restart

Contract while the flag is on (everything reverts when it is off):

- The default gateway enumerates every profile and serves each profile's enabled
  platforms under that profile's OWN credentials. Credentials are never shared.
- Secondary profiles must NOT run `hermes gateway start` — it is a hard error while
  the multiplexer runs. `--force` exists but is not recommended.
- Port-binding platforms may be enabled ONLY on the default profile:
  webhook, api_server, msgraph_webhook, feishu, wecom_callback, bluebubbles, sms,
  whatsapp_cloud, line, teams. A secondary profile enabling one is a config error:
  that profile is skipped entirely (warning names the profile + platforms).
- HTTP routing: default profile = `POST /webhooks/<route>`; secondary profile =
  `POST /p/<profile>/webhooks/<route>`. Unknown/unconfigured profile in prefix → 404.
- Auth follows the profile named in the URL: `/p/<name>/...` uses that profile's
  keys (e.g. API_SERVER_KEY from `~/.hermes/profiles/<name>/.env`); the default
  listener key is rejected there. Webhook routes targeting a profile must declare
  `profile: <name>` beside the route secret in the DEFAULT profile's config.yaml;
  that secret is then only valid at that profile's prefix.
- When to prefer: containers/VPS where N processes/ports/PIDs are a burden; many
  low-traffic profiles; single thing to monitor. Otherwise keep per-profile processes.

## `hermes profile` command surface
`list, use, create, delete, describe, show, alias, rename, export, import, install, update, info`

- `hermes profile use <name>` — sticky CLI default (like kubectl config use-context);
  `hermes profile use default` to switch back.
- `hermes profile describe <name>` — read/set the kanban routing description.
- `hermes profile create <name> [--clone] [--clone-all] [--clone-from <src>]
  [--description "..."] [--no-alias] [--no-skills]` — `--no-skills` opts out of
  `hermes update` bundled-skill sync.
- `hermes profile install <git-url-or-dir>` / `update` — profile distributions
  (versioned profile packages; user data preserved on update).
- Clone excludes per-profile history: sessions, state.db, backups/, state-snapshots/,
  checkpoints/ (can reach tens of GB). Full-history copy → `hermes profile export`
  or `hermes backup`.
- OAuth logins (Anthropic Claude Pro/Max, OpenAI Codex, xAI) use single-use refresh
  tokens: clones DROP those rows; profiles read login from root `~/.hermes/auth.json`
  and any profile's refresh writes back to root so all profiles stay signed in.
  Separate per-profile OAuth login: `hermes -p <name> auth add <provider>`.

## Related features
- `hermes kanban` — multi-profile collaboration board (tasks, links, comments);
  the orchestrator decomposes and routes tasks using each profile's description.
- Profiles vs workspaces vs sandboxes: profile = state directory; workspace =
  `terminal.cwd` where commands start; sandbox = filesystem limits. A profile does
  NOT sandbox. Pin `terminal.cwd` per profile for a predictable working directory.
