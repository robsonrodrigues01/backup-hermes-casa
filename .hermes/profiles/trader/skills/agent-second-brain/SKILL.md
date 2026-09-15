---
name: agent-second-brain
description: >-
  Give a Hermes agent profile a durable "second brain": a plain-markdown
  brain/ folder inside the profile home (operating manual + raio-X inventory
  + daily diary + snapshots of service files + domain operation dirs +
  dropbox inbox), optionally mirrored to a PRIVATE GitHub repo via a scoped
  fine-grained token and a nightly auto-commit cron. Trigger: "estou com
  medo de perder o que progredi", "vamos usar o github? ou obsidian?",
  "cérebro do <empresa>", wiring the nightly commit, or deciding where a
  new fact/decision/file lives.
---

# Second Brain for an Agent Profile

## When to use
- User fears losing an agent profile's accumulated progress ("não quero perder o que já progredi", "podemos usar o github pra isso? ou obsidian?").
- Wiring/extending the nightly brain commit; operationalizing a bridge-zero inventory; filing a new decision/fact.

## Mental model
- The brain is a folder of plain `.md` inside the profile home: `~/.hermes/profiles/<name>/brain/`. Markdown-first pays out three times: GitHub history = infinite memory OFF the machine; Obsidian can later open the exact same folder as a visual view (window, not migration); the agent feeds it by itself.
- Distinct from full-state backup (`hermes profile export` / `hermes backup` = GBs, sessions/history): the brain is CURATED knowledge, deliberately small and readable.
- Bridge zero: write the raio-X inventory FIRST — the value is locking in what already exists, not perfection.

## Skeleton (starter files: templates/cerebro-skeleton.md)
- `00-CEREBRO.md` — operating manual: core rule "nada importante morre fora daqui"; end-of-day diary block is mandatory; decisions → `decisoes/`; client/project/process files by domain.
- `00-RAIO-X.md` — dated inventory of what exists at bridge zero (agent status, gateway, strong memories, ongoing operations, comms channels).
- `diario.md` — one dated block per day, newest on top.
- `snapshot/` — copies of the profile's service files (PENDENTES.md, MAPA.md, SOUL.md, SQUADS.md, memories/MEMORY.md).
- `<domain>/` — operation areas with their raw files (e.g. `comercial/` with leads.csv, pipeline.md, outreach/).
- `dropbox/` — bucket for loose files awaiting filing.

## Rollout
1. `mkdir -p .../brain/{snapshot,dropbox,<domains>}`; copy service files into `snapshot/`.
2. Write `00-RAIO-X.md`, `00-CEREBRO.md`, first `diario.md` block. The local part is the profile's own home → acting without waiting for an explicit OK matches the autonomy constitution; the GitHub step crosses a boundary and does NOT.
3. Hand-off recipe for the owner (his account; ~2 min): (a) create the repo set to **Private**; (b) fine-grained token scoped to **only that repo**, permission **Contents: Read and write**; (c) owner sends the token in chat.
4. Connect: init/clone, add remote using the token ONLY via file I/O — the security scanner masks token-shaped literals inside scripts (see hermes-profiles pitfalls); validate by URL/length, never echo. First push = the raio-X.
5. Nightly commit cron on the profile (e.g. 00h Bsb = `0 3 * * *`; cron runs in UTC — see hermes-profiles): self-contained prompt that `git add/commit/push` with a date message; **empty stdout = silent** delivery (nothing changed → nobody gets pinged); when it pushed, report the link to the latest commit. Cron may make 1 small question max per tick.
6. Verify: manual git push → confirm on GitHub web; register the repo in the profile's PENDENTES/MAPA.

## Pitfalls
- NEVER store credential VALUES in brain files (everything gets committed); record where credentials live BY NAME only, mapa-style.
- Repo stays PRIVATE; token scoped to that single repo; if the token ever lands in a screenshot/chat, owner revokes it immediately.
- clarify() for the repo decision can time out silently → build the local brain anyway, leave GitHub as the owner's 2-click hand-off, register the pending piece in PENDENTES.md.
- The AGENT curates brain content; never ask the owner to hand-write files — his only job is the two GitHub clicks and sending the token.
- Before rebuilding differently, check the live instantiation: `~/.hermes/profiles/era4/brain/` (era4-brain, 2026-09-11).

## References
- `templates/cerebro-skeleton.md` — starter content for `00-CEREBRO.md`, `00-RAIO-X.md`, a `diario.md` block.
- hermes-profiles skill — cron scheduler (UTC), scanner/token pitfalls, autonomy constitution, service-files convention.
