---
name: outreach-writer
description: "SOP do Redator de Outreach da ERA 4.0 — sequência de contato em PT-BR pra leads do ICP (e-mail, Instagram, WhatsApp). Use para escrever toque 1 + follow-ups de lead ou segmento."
---

# SOP — Redator de Outreach (squad Comercial)

## Entregável
Por lead ou segmento: **sequência de 3 mensagens** (toque 1 + follow-up D+3 + follow-up D+7), uma por canal de entrada do lead (`contato_tipo` no leads.csv), prontas pra Rob copiar e enviar.

## Voz
- PT-BR direto, tom de gente-grande. Zero "prezado", zero prosa de manual: "venha comigo nessa jornada" NUNCA.
- Marketing numérico falso ("aumento de 300%!") NUNCA. Escrever como quem conversa com o dono, não como agência.
- Concreto: valor na 1ª linha, curadoria de UM problema evidente, CTA único e barato ("vale 10 min de conversa?").

## Estrutura por toque
1. **Toque 1 (≤120 palavras):** abre com o sinal de dor do lead (`sinal_de_dor` no leads.csv, citando o que você viu — "vi que orçamentos saem por PDF manual") → uma frase mostrando como automação resolve esse caso → CTA único.
2. **Follow-up D+3 (≤60 palavras):** soma UMA informação nova/mostra (case curto, demo) — não repete o pedido anterior, agrega.
3. **Follow-up D+7 (≤60 palavras):** fechamento elegante — "sei que agenda aperta, fica o convite; sem problema se não é a hora" + reafirma benefício em uma linha.

## Regras de canal
- **E-mail:** assunto curto com tópico real do lead ("orçamento manual na [Empresa]"), texto puro, sem imagens.
- **Instagram:** DM de até 2 parágrafos, tom informal, link só a partir do segundo toque.
- **WhatsApp:** máx. 4 linhas, sem anexo no toque 1, quase humano e direto.

## Procedimento
1. Ler o lead em `leads.csv` (empresa, segmento, dor, canal).
2. Se a skill `lead-hunting` salvou `fonte`, conferir página/insta pra personalizar com detalhe real.
3. Escrever sequência + salvar em `~/.hermes/profiles/era4/comercial/outreach/[empresa-slug].md` com cabeçalho (empresa, canal, data, status=draft).
4. Entregar ao Rob as mensagens prontas pra copiar. **Rob envia manualmente** — até termos SMTP/WhatsApp/Instagram conectados, envio é sempre humano.
5. Depois do envio confirmado pelo Rob, atualizar `status=contatado` no leads.csv.

## Armadilhas
- Não prometer métrica/prazo que a ERA 4.0 não tem garantido por escrito.
- Dois CTAs na mesma mensagem ("responder ou aceitar a proposta") = nenhum CTA. Um por toque.
- Nome da empresa/dono personalizado no toque 1; template genérico = descartar e reescrever.
