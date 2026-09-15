# Native CLI install + always-on rollout (worked example: i-have-adhd, 2026-09-11)

Pattern for any SKILL.md-format repo pack being installed/distributed on this machine.

## 1. Locate the skill + read the repo's own instructions
- Repo `AGENTS.md` maps where canonical files live (`skills/<name>/SKILL.md` = source of truth).
- Repo `INSTALL.md` usually has a per-platform section — often an exact `hermes skills install` line. Verify repo is real first (GitHub API: stars/description/pushed_at), per SKILL.md step 1.

## 2. Install (active profile) — output shape seen in real run
```text
$ hermes skills install ayghri/i-have-adhd/skills/i-have-adhd --yes
Fetching: ayghri/i-have-adhd/skills/i-have-adhd
Quarantined to .hub/quarantine/i-have-adhd
Running security scan...
Scan: i-have-adhd (skills-sh/ayghri/i-have-adhd/skills/i-have-adhd/community)
Verdict: SAFE
  MEDIUM   supply_chain   SKILL.md:38   "Good: "Run `npm install jsonwebtoken`..."
Decision: ALLOWED — Allowed (community source, safe verdict)
Installed: i-have-adhd
Files: SKILL.md, agents/gemini.toml, agents/openai.yaml
```
- `--yes` skips the confirmation prompt (needed outside TUI/idempotent re-runs).
- A MEDIUM note inside the scan does NOT block → verdict ALLOWED installs. Inspect flagged lines before deciding to `--force` anything; never force on verdicts other than ALLOWED-with-notes.
- Flags: `--category <dir>` (organizational subdir), `--name <name>` (override when SKILL.md lacks frontmatter name).

## 3. Fan out to the other profiles
```bash
for p in era4 cuidar lab; do
  hermes -p $p skills install ayghri/i-have-adhd/skills/i-have-adhd --yes
  ls ~/.hermes/profiles/$p/skills/i-have-adhd/SKILL.md        # physical check
  hermes -p $p skills list | grep -i adhd                     # status check (enabled)
done
```

## 4. Always-on (optional) — SOUL.md block per profile
Read each SOUL.md first (some end without trailing newline, some carry the SERVICO-PENDENTES-MAPA footer — anchor the patch there), then append:

```markdown
<!-- i-have-adhd: estilo de resposta always-on (instalado 2026-09-11, repo ayghri/i-have-adhd · skill skills/i-have-adhd). Para voltar ao estilo padrão, remova este bloco. -->
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists to 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

- Add one PT-BR one-line summary after the block if the profile's persona is PT-BR (helps PT-only reasoning stick).
- Verify all 4 at once: `grep -c "i-have-adhd: estilo" ~/.hermes/SOUL.md ~/.hermes/profiles/{era4,cuidar,lab}/SOUL.md` → expect `:1` each.
- Update `~/.hermes/MAPA.md` skills section (status: always-on/off, date, how to disable). Then update the skill's own SKILL.md step count via `hermes skills update` when upstream changes (hub-installed = protected: never hand-edit its SKILL.md).
- lab first: risky/broad rollouts go through lab (plain `hermes skills install ...` in lab persists; if odd, `hermes -p lab skills uninstall i-have-adhd`).

## 5. When NOT to use the CLI path
- Selective subset of a big pack → clone + inventory + copy per SKILL.md steps 2-5 (CLI installs only the one named skill).
- Full app repos (skill embedded in a codebase) → park, per SKILL.md pitfalls.
