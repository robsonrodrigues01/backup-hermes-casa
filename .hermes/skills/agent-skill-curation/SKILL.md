---
name: agent-skill-curation
description: >-
  Verify, inventory, selectively install and distribute third-party agent skills
  (SKILL.md-format packs shared as "ACHADOS" screenshots, GitHub links, or posts
  for Claude Code / Codex / Cursor / Gemini CLI) into a Hermes profile's library.
  Use when the user shares a skill pack to evaluate or asks to install/adapt a
  repo of agent skills, or when deciding which subset of a large collection
  fits which profile/agent.
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
   its own library, even when credentials/config are shared.

## Native installer: `hermes skills install` (verified 2026-09-11, i-have-adhd)
For a repo that ships SKILL.md-format skills, prefer the CLI over clone+copy — it quarantines, security-scans and installs in one shot:

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd --yes   # active profile
hermes -p era4 skills install <same-id> --yes                       # other profiles (era4/cuidar/lab)
hermes skills list | grep -i <name>                                 # verify: source skills.sh, enabled
```

- Identifier = `owner/repo/path/to/skill`. The repo's own `INSTALL.md` often documents the exact Hermes line — read it first, it IS the whole task (same for repo `AGENTS.md`, which maps where canonical files live).
- Output shape: `Quarantined to .hub/quarantine/...` → scan with verdict SAFE (MEDIUM notes can still end ALLOWED — e.g. a flagged code example inside SKILL.md) → `Installed: <name>` + file list. Lands at `~/.hermes/skills/<name>/` (active) or `~/.hermes/profiles/<p>/skills/<name>/`.
- One named skill per install. For multi-skill packs needing a SELECTED subset, keep the clone+inventory+copy workflow (steps 2-5).
- File-level only: no gateway restart needed; a new session indexes the skill (ongoing chats pick it up next session or after an explicit "read your SOUL.md" nudge).

## Always-on rollout across all profiles (distribution add-on)
When an installed skill should drive behavior without invoking: (1) install into every live profile as above; (2) append a behavior block to each profile's `SOUL.md` with an HTML removal-marker: `<!-- <skillname>: always-on (date, repo, "remover este bloco para voltar ao estilo padrão") -->`; (3) register it in `~/.hermes/MAPA.md` skills section; (4) verify all files with one grep across the 4 SOUL.md paths. Hub-installed skills are protected — never edit their SKILL.md; customization goes in the SOUL block/AGENT rules instead.

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

## References
- `references/achados-batch-1.md` — first ACHADOS batch on this machine
  (taste-skill, designer-skills, html-anything, remotion-dev/skills,
  phuryn/pm-skills): repo stats, what was installed where, parked items and
  open decisions waiting on the user.
- `references/install-cli-alwayson.md` — native `hermes skills install` CLI
  path (quarantine/scan output shape, per-profile fan-out, SOUL.md always-on
  block) with the full i-have-adhd worked example (2026-09-11).