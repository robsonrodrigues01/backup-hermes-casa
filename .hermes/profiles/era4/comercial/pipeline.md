# PIPELINE COMERCIAL — ERA 4.0

> Fonte dos leads: `leads.csv` (mesma pasta). Source of truth = arquivo, não memória.
> Quem move o card: o Rob na conversa ("lead X virou reunião"). Claudemir atualiza o arquivo.

## Estágios (leads.csv usa estes valores em `status`)
1. `novo` — recém-caçado, sem toque
2. `contatado` — toque 1 enviado (rascunho do Rob aceito e enviado)
3. `respondido` — liderança engajou
4. `reuniao` — discovery agendado/feito
5. `proposta` — proposta enviada
6. `ganho` / `perdido` / `frio` — frio = sem resposta; volta via caçada de follow-up

## Regras
- Duplicidade: checar por nome + CNPJ antes de append. Nunca recaçar quem já está no arquivo.
- Contato: só dado PUBLICADO (site, @insta, WhatsApp de capa/contato no site). Nada fabricado.
- Sem resposta após 2 follow-ups → `frio`; caçada semanal decide quem reaquece.

## Cadências vigentes (definidas pelo Rob em 11/09/2026)
- Caça: ~20 leads novos por semana (cron de segunda-feira 9:00)
- Canais de abordagem: e-mail · Instagram · WhatsApp (envio ainda manual pelo Rob)
