# Curator run — 2026-09-10T05:31:33.190039+00:00

Model: `zai-org/GLM-5.1-FP8` via `custom`  ·  Duration: 3m 51s  ·  Agent-created skills: 2 → 2 (+0)

## Auto-transitions (pure, no LLM)

- checked: 2
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **38** (by name: cronjob=1, memory=1, read_file=1, session_search=2, skill_manage=7, skill_view=5, skills_list=1, terminal=20)
- consolidated into umbrellas: **0**
- pruned (archived for staleness): **0**
- new skills this run: **0**
- state transitions (active ↔ stale ↔ archived): **0**

## LLM final summary

# Consolidation pass — umbrella-building report (lab profile, 2026-09-10)

## Scope determination ran first, not assumed

The brief anticipated 10–25 prefix clusters across a large agent-created pool. The actual landscape required a provenance audit before any merge decision:

| Provenance | Count | Evidence |
|---|---|---|
| Agent-created (candidate pool) | **2** | `.usage.json` `created_by: agent` → `agent-skill-curation`, `hermes-profiles` |
| Third-party pack content (local) | 49 | Bulk-copied Sep 9 14:47–15:38 from verified repos (`references/achados-batch-1.md`: taste-skill/leonxlnx 5, phuryn/pm-skills 27, marketing pack 14, research tools 2) |
| Bundled built-ins | **0** | `hermes skills list`: "0 hub-installed, 0 builtin" |
| Hub-installed | **0** | `.hub/lock.json` `installed: {}` |

So PRUNE-BUILTINS mode has no targets in this profile, and the third-party clusters (`design/`×4, `dev/full-output-enforcement`, `marketing/`×14, `product/`×26, `research/`×2) are outside the candidate filter *and* outside the bundled-only PRUNE-BUILTINS authorization. Documented, not touched (rationale below).

## Cluster 1 — ACHADOS third-party intake: MERGE+DEMOTE (the real consolidation)

`achados-toolkit-setup` surfaced as a **literal rule-#4 hit**: a session-artifact-named skill (`*-toolkit-setup`) holding machine-state content (durable `~/tools/*` paths, per-tool pitfalls like the Agent-Reach web-Jina 401 and the SIGTRAP chromium trap, proof commands, per-profile distribution state). The upstream pack provenance is absent — it was agent-authored output of the ACHADOS flow, which the auto-filter missed because it was bulk-copied, not created via `skill_manage` (confirmed: authorship by content, no upstream repo).

Consolidated into the already-existing umbrella `agent-skill-curation`:
- **Demote** → `references/verified-tools.md`, verbatim body (diff-verified against the pre-run backup: only frontmatter→provenance-comment differs) — correct support-dir choice: condensed knowledge bank, not a copy-and-modify template.
- **Patch umbrella SKILL.md**: description now carries the absorbed triggers ("verified tool missing/broken", "reuse a pilot — video render, scraping CSV"); new labeled section **"Operating the verified toolkit (machine state)"** with corrected facts (my first patch had two transcription slips — `~/.agent-reach-venv`, SIGTRAP pitfall — caught and fixed in-place); References list updated with provenance note.
- **Archive** the original with `absorbed_into='agent-skill-curation'`.
- ✅ Verified: `linked_files` = 2 healthy references; listing dropped 51→50 local; no dangling relative links from active instructions.

## Cluster 2 — platform administration pair: KEEP, cross-linked

`hermes-profiles` (profile topology, gateways, credential-swap pitfalls; 2 references) and `agent-skill-curation` (content pipeline: verify→subset→install→distribute; 2 references) are **each already the class-level umbrella of its own class**. The maintainer test says a mega-`hermes-admin` umbrella containing both would *worsen* discoverability — precise trigger-rich descriptions collapsed into one, two large bodies with zero shared mechanics. Negligible count win, real discoverability loss.

Instead I added the missing consolidation artifact a maintainer would write: **bidirectional hand-off links** — `hermes-profiles` step 7 (new) hands off to `agent-skill-curation` for library distribution; `agent-skill-curation` step 7 hands back for profile creation/gateway bootstrapping. Frontmatter of both verified intact after patching.

## Second pass

Remaining agent-created pool = exactly the two umbrellas above. No further absorption improves discoverability. The only other archive on disk (`/home/hermes/.hermes/skills/.archive/dev/headroom-proxy-rollout → hermes-profiles`) belongs to the **default profile's** separate curator pass (04:55) and was left untouched.

## Recoverability

The original `achados-toolkit-setup` package is preserved in the auto pre-run backup (`.curator_backups/2026-09-10T05-31-33Z/skills.tar.gz`, verified present) *and* its full content is live in the umbrella. Zero cron dependencies existed to migrate.

Two environment quirks, carried into this report since the memory store is disabled here: (1) the `.usage.json`-based candidate filter misses bulk-copied agent-authored skills — verify by content before classifying; (2) `skill_manage delete` records `absorbed_into` for tooling but physical `.archive` materialization is not guaranteed per-profile — always diff against the pre-run tar.

## Structured summary (required)

```yaml
consolidations:
  - from: achados-toolkit-setup
    into: agent-skill-curation
    reason: Session-artifact machine-state runbook (verified-toolkit paths/pitfalls/proofs) demoted to the ACHADOS umbrella as references/verified-tools.md with its triggers folded into the umbrella description.
prunings: []
```

Decision left alone, intentionally not listed above: the 49 third-party pack skills — out of the agent-created candidate pool by provenance-filter design; rewriting them would break upstream provenance, the packs' internal cross-reference graph (`see copywriting`, `see social`), their evals/references packages, and the pending era4/cuidar distribution subsets that are waiting on exactly these files.

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.
