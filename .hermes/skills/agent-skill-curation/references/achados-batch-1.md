# ACHADOS batch 1 — carrossel human__academy "skills p/ agentes"

Achados #001–#005 de um carrossel de 7 slides (sept 2026; #006/#007 ainda não
vistos — pedir quando o Rob mandar). Todos verificados via GitHub API +
shallow clone + inventário de SKILL.md antes de virar opinião.

## 6) sickn33/agentic-awesome-skills (AAS) — ★46.3k, MIT, pushed 2026-09-09
- Link do Rob em commit pinado `9d486d089` (2026-09-11, clonado em /tmp/aas).
- "Antigravity Awesome Skills": catálogo instalável de skills p/ agentes de
  código (npx antigravity-awesome-skills → ~/.agents/skills) + 42+ bundles
  `antigravity-bundle-*` por papel + CLI/MCP de descoberta.
- NÚMEROS REAIS do clone: 4.831 SKILL.md (~15k arquivos), MAS apenas ~1.520
  skills únicas — gigabulk: o restante é o mesmo conteúdo recolado nos bundles.
  Descrição da API diz "2.115+ skills" (divergência própria do repo).
- VEREDICTO DO ROB (2026-09-11): NÃO instalar (só queria a análise). Bulk
  proibiria conflito com nomes já instalados (copywriting, seo-audit,
  frontend-design...) e qualidade de 1KB-teaser a 58KB.
- Shortlist curada (se um dia ele quiser): cuidar=stripe-integration,
  pci-compliance, referral-program · era4=mcp-builder, agent-evaluation ·
  todos/oeste=unslop (4KB, anti-dialeto-de-IA) · demanda=personas PT-BR
  (elon-musk 58KB, warren-buffett, yann-lecun-tecnico, leiloeiro-ia,
  image-studio). EVITAR rich-elicitation (rodada-múltipla de perguntas =
  anti-régua do Rob). Instalar via `hermes skills install
  sickn33/agentic-awesome-skills/skills/<nome>`.

## 1) leonxlnx/taste-skill — ★85.7k, pushed 2026-08-24
- 13 skills anti-slop frontend (landing, portfolio, redesign).
- Mapping dir→frontmatter name: `taste-skill`→**asymmetric-split-hero**
  (flagship, 85KB), `soft-skill`→high-end-visual-design,
  `redesign-skill`→redesign-existing-projects, `minimalist-skill`→minimalist-ui,
  `output-skill`→full-output-enforcement.
- INSTALADO no perfil default: 4 em `skills/design/` + 1 em `skills/dev/`.
- Não instaladas: imagegen-frontend-{web,mobile}, image-to-code, brandkit,
  brutalist (industrial-brutalist-ui), gpt-taste, stitch-design-taste,
  design-taste-frontend-v1.

## 2) Owl-Listener/designer-skills — ★2.6k, pushed 2026-09-05
- 111 SKILL.md em ~9 coleções (ui-design, ux-strategy, design-ops,
  design-systems, interaction-design, prototyping-testing, visual-critique,
  design-research, designer-toolkit) + INDEX.md organizado por situação.
- PARKED: instalar coletâneas selecionadas (ui-design, ux-strategy,
  visual-critique) — candidatas: Claudemir/era4 e/ou default. Pegar via INDEX.

## 3) nexu-io/html-anything — ★8.7k, pushed 2026-08-23
- Não é pack: app completa Next/pnpm (cli/, next/, e2e/) com 81 SKILL.md
  embutidos (75 skills × 9 surfaces: magazine, deck, poster, social, proto…).
- PARKED: setup pesado; testar render antes de adotar (saída: decks, pôsteres
  e peças de social geradas de um HTML).

## 4) remotion-dev/skills (oficiais Remotion) — 12 skills
- remotion-best-practices (router), captions, create, docs, interactivity,
  maps, markup, multimedia, render, saas, studio, upgrade.
- PARKED p/ era4: skills são guias para trabalhar DENTRO de um projeto
  Remotion — sem projeto (Node + Chromium) não entregam valor. Plano: montar
  projeto-base na máquina e testar render de um vídeo exemplo antes de dar
  skills ao Claudemir.

## 5) phuryn/pm-skills — ★26.1k (Paweł Huryn), 68 SKILL.md
- ERRATA do post: comando mostrado era `claude plugin marketplace add
  phrym/pm-skills` — handle real é `phuryn`.
- 8 coleções (~counts): product-discovery 13, product-strategy 12, execution
  14, market-research 7, go-to-market 7, marketing-growth 5, data-analytics 3,
  toolkit 4, ai-shipping 2.
- INSTALADO no default (`skills/product/`, 27): opportunity-solution-tree,
  identify-assumptions-new, prioritize-features, interview-script,
  summarize-interview, lean-canvas, product-strategy, pricing-strategy,
  value-proposition, create-prd, user-stories, job-stories, pre-mortem,
  release-notes, summarize-meeting, competitor-analysis, market-sizing,
  user-personas, gtm-strategy, beachhead-segment, growth-loops,
  ideal-customer-profile, sql-queries, cohort-analysis, ab-test-analysis,
  intended-vs-implemented, shipping-artifacts.
- Subset sugerido p/ Claudete (cuidar.vc): competitor-analysis, user-personas,
  market-segments, user-segmentation, market-sizing, ideal-customer-profile,
  beachhead-segment, gtm-strategy, growth-loops, north-star-metric,
  positioning-ideas, value-proposition, customer-journey-map, pricing-strategy.
- Subset sugerido p/ Claudemir (era4): create-prd, user-stories, job-stories,
  pre-mortem, release-notes, sprint-plan, test-scenarios,
  intended-vs-implemented, shipping-artifacts (+ coletâneas de design do item 2).

## Decisões em aberto (aguardando o Rob)
1. Distribuir subsets p/ era4 e/ou cuidar (outro perfil exige OK explícito).
2. Montar projeto-base Remotion e testar render aqui antes de decidir.
3. Grupos Telegram: "Conselho" (3 bots conversando) + squads por agente
   (monitor de subagentes) — aguardando o Rob criar os grupos.
