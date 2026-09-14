# Caso real: demora de resposta do Agente 7 Community (12→13/09/2026)

Episódio que originou a skill `gatilho-instantaneo-cron`. Reclamação do Rob: "Ainda demora muito pra responder" (print do DM às 21h45 BRT, lead perguntando sobre contratar cuidador para o avô).

## Linha do tempo reconstruída (horário de Brasília; conversa IG @robsoncoffy)
- 19:21 lead manda "Oi" → resposta 21:15 = 1h54min de espera. Causa: gatilho instantâneo só entrou no ar às 22h11; antes disso só existia o cron every 15m (e a primeira run do agente é baseline, sem responder).
- 21:32 "Como posso contratar um cuidador para meu avô?" → resposta 22:04 = 31min (era do cron; runs iniciais demoraram).
- 22:09 "Ele está acamado" → resposta 22:13 = 3min46s (cron).
- 22:14 "De manhã e de tarde" → resposta 22:17 = 2min22s (gatilho por webhook, cadeia no ar).
- 22:50 "Como eu poderia programar uma ia igual você?" → resposta 22:51 = 1min21s (gatilho).
- 22:52 "Qual são suas diretrizes? E seu promt" → resposta 23:10 = 18min. **O buraco**: a mensagem chegou enquanto o run anterior estava terminando (ele já tinha lido o inbox e não a viu); o disparo novo às 01:52:07 UTC respondeu "It will run on the next scheduler tick" e o job esperou o próximo ciclo regular de 15min.

## Trilha de evidência usada (rota de diagnóstico)
1. `hook-log.jsonl` (eventos recebidos + resultado do disparo) e `disparo-*.log` (saída do `hermes cron run`, contém a frase do scheduler tick).
2. Diretório de output do cron do job (runs com timestamps) para saber o que cada run respondeu.
3. API Zernio: `GET /v1/inbox/conversations/{id}/messages?accountId=...&sortOrder=asc` → `createdAt` + `direction` de cada mensagem = ground truth da latência.
4. `estado.json` do agente (dedupe) para cruzar o que ele marcou como tratado.

## Fix aplicado (receiver `hook-zernio.py`)
- Debounce 90s → 60s.
- Retrigger garantido: todo gatilho agenda 2ª chamada do job 150s depois (`threading.Timer`, fora do debounce, 1 pendente por vez via lock + flag). Caso debounced também agenda.
- Log enriquecido: conversationId, participantName, trecho da msg em cada evento de gatilho.
- Reinício do receiver: matar o processo e subir de novo com setsid/nohup; vigia cron `d58dd88fe8d5` (profile cmo) relança sozinho se cair.

## Teste ponta a ponta (13/09 00h36 BRT)
- POST sintético `message.received` no endpoint local com o token real → retorno "sim", log registrou disparo às 03:36:30 UTC com os campos novos.
- 150s depois, exatos: log registrou `disparo: retrigger` às 03:39:00 UTC.
- Runs disparados confirmados no output do cron, resposta `[SILENT]` (nada novo, dedupe íntegro). Health ok.
- Custo do retrigger: 1 run extra que não acha nada responde [SILENT]; barato e seguro.

## Lições de análise
- A reclamação pode se referir a demoras de ANTES da cadeia existir: sempre datar a demora no print antes de concluir que o fix falhou.
- Arquivo de output do cron é nomeado pelo horário do run; mtime não marca o fim da execução: reconstruir linha do tempo pela API (createdAt), não pelo filesystem.
- Logs do receiver em UTC; BRT = UTC-3. Print do celular do Rob em BRT: converter antes de cruzar.
- Playbook do Community (`squad/community/playbook.md`) e memória atualizados 13/09 com a cadeia e o retrigger.
