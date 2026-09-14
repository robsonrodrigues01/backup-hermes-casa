# SQUADS DA ERA 4.0 — construção sob demanda (squad por squad)

> Regra do Rob (2026-09-10): NADA de organograma gigante com agentes fantasmas.
> Um squad por vez, com íntegra: cada agente precisa de identidade (soul),
> SOP/skill, toolsets e rotina definidos antes de existir.
> Validado na prática → só anota aqui o que estiver FUNCIONANDO.

## Squad Comercial 🏹 — construído em 11/09/2026 (validação de campo em andamento)

**ICP:** PMEs brasileiras, foco RM de Porto Alegre + Vale dos Sinos (RS).
**Canais:** e-mail · Instagram · WhatsApp (envio manual pelo Rob). **Cadência:** ~20 leads/caçada.
**Base de dados:** `comercial/leads.csv` + `comercial/pipeline.md` (source of truth = arquivos).

### 1. 🔍 Caçador de Leads — `skills/comercial/lead-hunting`
- **Soul:** pesquisador obsessivo; só entrega empresa ativa com dor observável e contatos publicados. Jamais inventa contato.
- **Tools:** web, navegador, terminal (arquivos). **Rotina:** cron "Caçada de leads semanal — ERA 4.0" (segunda 9:00, ~20 leads).
- **Entrega:** append em leads.csv + report de destaques pro Rob.

### 2. ✍️ Redator de Outreach — `skills/comercial/outreach-writer`
- **Soul:** copywriter direto PT-BR; sequência de 3 toques por lead, personalizada pelo sinal de dor. Zero template genérico.
- **Tools:** arquivo (rascunhos em comercial/outreach/). **Rotina:** sob demanda após cada caçada; batches quando Rob pedir.
- **Entrega:** mensagens prontas pra Rob copiar/enviar. ⚠️ Envio automático bloqueado até Rob fornecer SMTP/WhatsApp — pendência registrada em PENDENTES.md.

### 3. 📄 Arquiteto de Propostas — `skills/comercial/proposal-architect`
- **Soul:** tradutor escopo ↔ preço; discovery respondido é pré-requisito; anti-subdimensionar (buffer 25%, fora-de-escopo explícito).
- **Tools:** arquivo + terminal (docx/pdf em comercial/propostas/). **Rotina:** sob demanda (após reunião de discovery).
- **Entrega:** proposta padrão ERA 4.0 + one-pager + update no leads.csv (`status=proposta`).

**Status de validação:** smoke test aprovado 11/09 (3 leads gravados + rascunho outreach + lições de eficiência aplicadas na skill). 1ª caçada completa ~20 leads: cron seg 14/09 9:00 — se vier boa, squad marcado como FUNCIONANDO.

## Squads desejados (sem integridade ainda)
- Delivery · Conteúdo & Marketing · Ops Interna (um de cada vez, quando Rob mandar)
