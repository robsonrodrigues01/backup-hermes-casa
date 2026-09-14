# DESIGN.md / VoltAgent awesome-design-md — notas condensadas

(Verificadas em sessão de 2026-09. Para re-utilizar em trabalho de UI de
clientes; não é documento oficial.)

## Conceito: DESIGN.md

- Formato introduzido pelo **Google Stitch**: documento markdown puro no root
  do projeto que agentes de IA leem para gerar UI consistente. Paralelo do
  AGENTS.md — "AGENTS.md define como construir; DESIGN.md define como fica".
- Nada de Figma export/JSON/schema. Markdown é o formato que LLMs lêem melhor.

## O repo

- `github.com/VoltAgent/awesome-design-md` — ⭐115k (top 150 GitHub), 13k forks,
  MIT, 74 marcas em `design-md/<marca>/` (10 categorias + Retro Web: Dell 1996,
  Nintendo 2001).
- Cada pasta: `DESIGN.md` + `preview.html` + `preview-dark.html`.

## Formato das 9 seções (padrão a replicar em DESIGN.md próprio)

1. Visual Theme & Atmosphere
2. Color Palette & Roles (nome semântico + hex + função)
3. Typography Rules (família + tabela hierárquica completa)
4. Component Stylings (botões, cards, inputs, nav — com estados hover/pressed)
5. Layout Principles (escala de spacing, grid, filosofia de whitespace)
6. Depth & Elevation (sistema de sombra, hierarquia de superfícies)
7. Do's and Don'ts (guardrails e anti-padrões)
8. Responsive Behavior (breakpoints, touch targets ≥44px, colapso)
9. Agent Prompt Guide (referência rápida de cor + prompts prontos)

Alguns arquivos incluem "Known Gaps" documentando o que NÃO foi extraído.

## Como usar

- Copiar o `DESIGN.md` da marca/build próprio para o root do projeto e pedir
  ao agente: "build me a page that looks like this" (ou referenciar componente
  a componente por token, ex.: `{colors.primary}`).
- Lint após editar: `npx @google/design.md lint DESIGN.md`.

## Prova de qualidade (amostra linear.app — 21.910 chars)

- 23 tokens de cor semânticos, 13 níveis tipográficos com letter-spacing por
  nível, 21 componentes com estados, breakpoints 1440/1280/1024/768/480.
- Exemplo de tokens reais: canvas `#010102`, primary `#5e6ad2`, surface ladder
  `#0f1011`→`#191a1b`, hairline `#23252a`.

## Uso na ERA 4.0 + caveat

- Use o formato das 9 seções como TEMPLATE para criar um `DESIGN.md` próprio
  por cliente antes de gerar UI — padroniza handoff design→código.
- CAVEAT: tokens são CSS público, mas replicar a identidade visual integral de
  marca famosa é zona cinzenta legal. Derive tokens/estrutura, não a face.
