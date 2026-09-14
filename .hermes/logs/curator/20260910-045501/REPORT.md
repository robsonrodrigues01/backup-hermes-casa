# Curator run — 2026-09-10T04:55:01.610378+00:00

Model: `zai-org/GLM-5.1-FP8` via `custom`  ·  Duration: 2m 6s  ·  Agent-created skills: 4 → 3 (-1)

## Auto-transitions (pure, no LLM)

- checked: 4
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **21** (by name: memory=1, patch=3, read_file=2, skill_manage=2, skill_view=5, skills_list=2, terminal=6)
- consolidated into umbrellas: **1**
- pruned (archived for staleness): **0**
- new skills this run: **0**
- state transitions (active ↔ stale ↔ archived): **0**

### Consolidated into umbrella skills (1)

_These skills were **absorbed into another skill** during this run — their content still lives, just under a different name. The original directory was moved to `~/.hermes/skills/.archive/` for safety and can be restored via `hermes curator restore <name>` if the consolidation was wrong._

- `headroom-proxy-rollout` → merged into `hermes-profiles` — Per-profile local-proxy runbook serving the same profile-infrastructure class, already citing hermes-profiles pitfalls — absorbed as a labeled SKILL.md section plus references/local-proxy-headroom.md.

## LLM final summary

Memory store is disabled in this environment — noted, carrying the quirk into the report instead.

---

# Curation pass — umbrella consolidation report (2026-09-10)

## Scan

Candidate set contained exactly **4** agent-created skills (everything else in the 55-skill registry is hub/bundled — the design/marketing/product/research packs plus `achados-toolkit-setup`, `full-output-enforcement`, `conselho-de-ia`, `criar-skill`, `agent-context-kit` — all off-limits). Cluster scan found one cluster with 2+ members:

| Cluster basis | Members | Umbrella class | Verdict |
|---|---|---|---|
| Hermes profile infrastructure (`hermes-*`, gateway/port/token family) | `hermes-profiles`, `headroom-proxy-rollout` | "Operating per-profile agent homes + background services" | **MERGE INTO EXISTING UMBRELLA** |
| ACHADOS / third-party pack ingestion | `agent-skill-curation` (singleton in scope) | Pack-verification/curation class | KEEP (already class-level, 1 reference attached) |
| Owner communication prefs | `rob-comms-style` (singleton) | "How to speak with Rob" class | KEEP (distinct class; merging into infra ops would damage discoverability) |

## Consolidation executed: `headroom-proxy-rollout` → `hermes-profiles`

The Headroom runbook is a **per-profile service sibling**, not a sibling-with-a-better-runbook: it exposes no `hermes` CLI surface, defines fixed ports (8787–8790) for the same four profiles the umbrella manages, and already deferentially cited `hermes-profiles` for restart pitfalls in its own step 5 ("veja pitfalls de drain/restart em `hermes-profiles`") — a maintainer would write this as a *section*, not a separate skill.

1. **Re-homed body verbatim** → `agent-admin/hermes-profiles/references/local-proxy-headroom.md` (2600 B; port table, unit template, hookup steps, diagnostics), with an absorption provenance header. Package integrity: source skill had zero support files and zero relative links, so wholesale re-homing was safe; reference discovery verified via `skill_view(name, file_path)`.
2. **Added labeled subsection** to the umbrella SKILL.md: *"Per-profile local proxy: Headroom (economizador de memória)"* — compressed runbook + pointer to the reference, plus pattern-generalization note (valid for any per-profile local proxy).
3. **Umbrella description updated** to advertise the new coverage (discoverability for "ligar o economizador").
4. **Archived the source package** → `~/.hermes/skills/.archive/dev/headroom-proxy-rollout/SKILL.md` with an `ARCHIVED-README.md` pointing at the absorption targets.

**Incident during archival, fully remediated:** `skill_manage(delete)` **hard-deleted** the directory rather than archiving it (no `.archive/` was created). Recovered the verbatim package from the pre-run snapshot `~/.curator_backups/2026-09-10T04-55-01Z/skills.tar.gz` and re-created the archive manually. Since deletion is forbidden by policy, future passes should use `terminal mv` into `.archive/` instead of `skill_manage(delete)`. ⚠️ This environment also has the `memory` tool disabled.

## Post-round scan & next-pass notes

- Registry: 55 skills (headroom entry gone from the active list; only live mention of the old name is the intentional provenance line inside the absorbed reference). No cron job or live SKILL.md references it — no reference migration needed.
- Second-round opportunities within scope: none viable. The two remaining keeps are already class-level; their only logical future sibling, `achados-toolkit-setup` (ACHADO tool-install sibling, natural umbrella `rob-toolkit-ops` with curation + toolkit as chapters), is **hub-installed and out of bounds** — flagging it for a pass with explicit operator authorization.
- Structural note: 1 archive total is the ceiling for a 4-skill candidate set where 2 members are already umbrellas — every candidate was checked against every other; the low count is scope, not stopping early.

## Structured summary (required)

```yaml
consolidations:
  - from: headroom-proxy-rollout
    into: hermes-profiles
    reason: Per-profile local-proxy runbook serving the same profile-infrastructure class, already citing hermes-profiles pitfalls — absorbed as a labeled SKILL.md section plus references/local-proxy-headroom.md.
prunings: []
```

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.
