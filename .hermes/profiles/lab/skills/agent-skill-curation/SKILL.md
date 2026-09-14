---
name: agent-skill-curation
description: >-
  Verify, inventory, selectively install and distribute third-party agent skills
  (SKILL.md-format packs shared as "ACHADOS" screenshots, GitHub links, or posts
  for Claude Code / Codex / Cursor / Gemini CLI) into a Hermes profile's library.
  Also covers operating and re-verifying the agent-tools already installed from
  prior packs on this machine (paths, pitfalls, proof commands — Agent-Reach,
  last30days, Headroom, Remotion, Crawlee, Maxun/gstack) and reusing their pilots.
  Use when the user shares a skill pack to evaluate or asks to install/adapt a
  repo of agent skills, when deciding which subset of a large collection fits
  which profile/agent, or when one of the verified tools is missing/broken or a
  pilot it ran (video render, scraping CSV) needs to be reused/rerun.
---

# Curating third-party agent skills into Hermes profiles

## When to use
- The user drops screenshots/posts/links advertising "agent skills" built for
  other agent tooling (Rob's recurring "ACHADOS" pattern from the human__academy
  Instagram carousel — send slides, then waits for a verdict).
- The user asks "dá pra instalar isso?", "testa essa skill", "adapta pra mim".
- Any bulk-inventory or selective install of SKILL.md-format packs.

Note: these ecosystems use the SAME SKILL.md frontmatter format as Hermes, so
the work is file-level, not tool-level.

## Steps
1. **Verify before trusting — promotional names have typos.** Check
   `https://api.github.com/repos/{owner}/{repo}` (description, stars,
   pushed_at). On 404, search `/search/repositories?q=<keywords>` (real case:
   post showed `phrym/pm-skills`, real repo is `phuryn/pm-skills`). Report the
   errata to the user — it builds trust.
2. **Clone + inventory + install in ONE script.** Run
   `git clone --quiet --depth 1 <url> /tmp/<name>` via terminal(), then in the
   SAME execute_code script: `Path.rglob('SKILL.md')` and print
   `relpath | frontmatter name: | description[:100] | size KB`. Do the copy
   step in that same run (see Pitfalls).
3. **Identify the real skill name.** The frontmatter `name:` is what Hermes
   registers — a repo dir `taste-skill` can contain a skill named
   `asymmetric-split-hero`. Copy the whole skill dir (references/assets
   included) and name the target dir after the frontmatter `name:`.
4. **Select a subset, never bulk.** Mega packs flood the skill listing
   (a 273-skill pack shipped ~111 SKILL.md). Choose per business/agent
   relevance. Installing into the ACTIVE profile needs no permission;
   installing into OTHER profiles requires explicit user confirmation.
5. **Install into the active profile:** copy selected dirs to
   `~/.hermes/skills/<category>/<frontmatter-name>/`. Category is a free-form
   organizational subdir (seen: agent-admin/, design/, dev/, product/).
6. **Verify:** count `*/SKILL.md` under the target category dir and spot-read
   one SKILL.md. Report a compact list.
7. **Distribute to other profiles** (only after explicit OK): same copy logic
   into `~/.hermes/profiles/<profile>/skills/<category>/...`. Each profile has
   its own library, even when credentials/config are shared. The target profile
   must exist and be reachable first — for creating/operating profiles (clone,
   cloned-token pitfall, gateway install, API_SERVER_* strip), see the
   `hermes-profiles` skill.

## Pitfalls
- **/tmp is NOT durable across calls.** In one session `/tmp/rmtn` survived to
  the next execute_code call; in another `/tmp/pmk` vanished between two
  consecutive scripts. Treat any clone from a previous script as GONE —
  re-clone and use it in the same script.
- **Promotional install commands are not our commands.** `npx skills add ...`
  and `claude plugin marketplace add ...` target other tooling — skip them
  and copy files instead; flag command typos found in the post.
- **Some "skills" repos are full apps** (e.g. a Next/pnpm workspace with
  embedded SKILL.md) — installing guidance-only skills without the app
  delivers no value; park those until an environment exists.
- **Router skills**: a pack may ship one router (e.g. `remotion-best-practices`)
  that tells an agent which sibling skill to load — install the router too
  when installing the siblings.

## Operating the verified toolkit (machine state)
Prior batches seeded actual agent-tools on this machine — that's part of the
same ACHADOS pipeline (evaluate → install subset → operate). When Rob reports a
verified tool missing/broken, or asks to reuse a pilot (video render, scraping
CSV, token compression), don't re-research from scratch:
`references/verified-tools.md` holds the machine-state runbook — durable paths
(`~/tools/agent-reach`, `~/.agent-reach-venv`, `~/remotion-demo`,
`~/scrape-demo`, `~/headroom-test`), per-tool pitfalls (Agent-Reach web-Jina 401
→ `JINA_API_KEY`; container chromium dies with SIGTRAP unless launched with
`--no-sandbox --disable-gpu`), one-line proof
commands per tool, plus explicit pending decisions (Maxun needs docker = sudo
decision; Headroom gateway proxying = invasive, separate decision). Machine
profile distribution state is there too (era4/cuidar carry the marketing
subsets — check before re-installing).

## References
- `references/achados-batch-1.md` — first ACHADOS batch on this machine
  (taste-skill, designer-skills, html-anything, remotion-dev/skills,
  phuryn/pm-skills): repo stats, what was installed where, parked items and
  open decisions waiting on the user.
- `references/verified-tools.md` — machine-state runbook for the agent-tools
  installed by these batches (durable paths, pitfalls, proof commands);
  absorbed from `dev/achados-toolkit-setup` on 2026-09-10.