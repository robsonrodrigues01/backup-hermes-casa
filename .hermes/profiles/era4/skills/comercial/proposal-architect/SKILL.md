---
name: proposal-architect
description: "SOP do Arquiteto de Propostas da ERA 4.0 — traduz discovery de PME em escopo, preço e proposta (.docx/pdf padrão ERA 4.0 + one-pager). Use após reunião de discovery."
---

# SOP — Arquiteto de Propostas (squad Comercial)

## Entregável
1. `proposta-[cliente]-AAAAMMDD.docx` (ou PDF): proposta formal padrão ERA 4.0.
2. One-pager: página única de resumo (problema → solução → fases → preço).

## Pré-requisito: discovery respondido
Questionário mínimo (se faltar resposta, marcar como RISCO/ASSUNÇÃO — nunca inventar):
1. Qual processo dói mais hoje: quanto tempo e quantas pessoas gastam nele?
2. Como funciona o processo passo a passo (ferramentas, planilhas, WhatsApp)?
3. Onde esse processo quebra (erros, retrabalho, esquecimento)?
4. Quem decide / compra dentro da empresa?
5. Faixa de preço que o cliente aceita pagar por mês/projeto?
6. Prazo desejado e sazonalidades?
7. Acesso hoje: sistemas usados, contas e APIs contratadas, contato técnico na empresa?

## Procedimento
1. Consolidar discovery em "Diagnóstico" (2–3 parágrafos no idioma do dono, sem jargão técnico).
2. **Escopo em fases** com critério de aceite e horas estimadas por fase. Fase 0 = diagnóstico detalhado (dados/formatação) antes de construir. Escopo cinzento → horas ×1,25.
3. **Preço por fase** (o cliente paga resultado visível a cada fase). Formato: R$ fixo por fase + valor mensal opcional de manutenção/evolução. Faixa (mín–máx) quando o discovery não fechou o escopo.
4. **Fora de escopo explícito** — lista do que NÃO está incluso (protege de trabalho invisível).
5. **Riscos e dependências** — acessos/credenciais que faltam, dados que o cliente precisa fornecer, prazo condicionado a isso.
6. Gerar arquivos + salvar em `~/.hermes/profiles/era4/comercial/propostas/`.
7. Atualizar leads.csv: caminho do arquivo em `proximo_passo`, `status=proposta`.

## Estilo da proposta
- Título: "Proposta — [solução em 5 palavras] para [Cliente]"
- Estrutura: Sumário executivo (1 parágrafo) → Diagnóstico → Solução em fases → Cronograma → Investimento → Próximos passos (3 linhas, 1 ação).

## Armadilhas
- Horas sem buffer = subdimensionamento — adicionar 25% e anotar "assunção: discovery completo na fase 0".
- Cliente pequeno ≠ escopo pequeno: dor grande paga bem, mas exige fases curtas com entrega rápida visível.
- Nunca entregue preço "no escuro" — pricing só depois do discovery respondido.
