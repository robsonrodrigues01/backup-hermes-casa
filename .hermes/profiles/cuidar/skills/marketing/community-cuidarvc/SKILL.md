---
name: community-cuidarvc
description: Operar, ajustar e auditar o Agente 7 "Community" do cuidar.vc (DMs e comentários do Instagram @cuidarvc.br e Facebook via API Zernio). Use quando precisar mudar frequência ou comportamento do agente de atendimento, tratar leads e escalações, ou validar o que foi respondido nos chats.
category: marketing
---

# Agente 7 Community: DMs e comentários do cuidar.vc

Anatomia (soul, skills, ferramentas):
- **Soul**: prompt do job = voz da marca nos chats. Acolhedora, objetiva, honesta, nunca robótica. Muitas vezes é a primeira conversa que uma família tem com o cuidar.vc.
- **Skills**: skill `marca-cuidar-vc` anexada ao job + playbook `squad/community/playbook.md` (fonte única de verdade técnica: roteiros A–F, triagem, limites, endpoints e payloads).
- **Ferramentas**: toolsets terminal+file; curl sempre com `-H @zernio.hdr` no workdir `/home/hermes/cuidarvc/squad`; payloads em arquivo `-d @...`, nunca Bearer inline.

## Onde o job mora (e onde NÃO mora)
- Job **b1c27fe585a1**, gerenciado pelo scheduler do profile **cmo** com `profile=cuidar` (roda dentro do perfil cuidar).
- ⚠️ `hermes -p cuidar cron list` NÃO mostra este job (lista só os jobs do scheduler cuidar, agentes 1 a 6 etc.). Ele aparece em `hermes cron list` (scheduler ativo cmo, com linha "Profile: cuidar") e em `cronjob action=list`.
- Agendamento: **every 15m** (desde 12/09; antes era a cada 2h e o lead esperava horas). Deliver local: o CMO lê o relatório e leva ao briefing.

## Mudar o agendamento (pitfall do update)
- `cronjob action=update` com `schedule='15m'` vira ONE-SHOT ("once in 15m"). Para recorrente use **`schedule='every 15m'`** (padrão válido: 'every 30m', 'every 2h' etc.).
- Após qualquer update, conferir no retorno: `schedule: "every 15m"` com `repeat: forever`. Se aparecer "once in", refazer com o formato "every".

## Validar a resposta REAL no chat (nunca confiar só no relatório)
1. AccountId IG: `GET /v1/accounts` retorna o campo **`accounts`** (não é `data`; parse com `data` quebra com KeyError), usar `_id` da conta instagram.
2. Ler de volta a conversa (workdir `/home/hermes/cuidarvc/squad`):
```
curl -s -H @zernio.hdr "https://api.zernio.com/v1/inbox/conversations/{convId}/messages?accountId=$(curl -s -H @zernio.hdr https://api.zernio.com/v1/accounts | python3 -c 'import sys,json; d=json.load(sys.stdin); print([a["_id"] for a in d["accounts"] if a["platform"]=="instagram"][0])')&limit=30&sortOrder=asc"
```
3. A última mensagem `direction=outgoing` deve ser a resposta enviada. O Rob audita por print do DM: antes de reportar sucesso, ler de volta e colar o texto real pra ele.

## Rotina e segurança (resumo; detalhes no playbook)
- DMs primeiro (lead esperando não pode esperar), comentários depois. Dedupe por `community/estado.json`; PRIMEIRA RUN = só baseline.
- Roteiros A–F: família quer contratar, profissional querendo trabalhar, como funciona, cidade/região, multi-turno (nunca recomeçar apresentação nem reenviar link), elogio.
- Escala pro Rob (append em `community/escalacoes.md`): PREÇO, SALÁRIO, RECLAMAÇÃO, PROPOSTA, URGENTE, SPAM, DM_JANELA. Nunca cravar valor único de preço/salário; nunca prometer disponibilidade; nunca pedir dados sensíveis no chat (direcionar pro site); emergência = acolher + SAMU 192 + tag URGENTE.
- Limites por run: 20 respostas de comentário + 10 DMs + 50 curtidas. Likes em comentários IG desligados (403 beta Meta, flag `ig_likes_ok=false`); Facebook funciona.
- Sem travessão (—) nas respostas do agente; PT-BR acolhedor.

## Notas da API Zernio inbox (produção, 12/09)
- Cada POST de resposta exige header `Idempotency-Key: <uuid novo>`. Janela de 24h da Meta: falha de janela = não insistir, escalar tag DM_JANELA.
- Likes em comentários IG: `403 PLATFORM_BETA_RESTRICTED` (limited release da Meta) → setar `ig_likes_ok=false` no estado e não tentar mais. Facebook funciona normal.
- `GET /v1/inbox/mentions` só devolve LinkedIn; menções IG exigem webhook (fora de escopo).
- Fonte única completa de endpoints e payloads: `squad/community/playbook.md`. Se algo aqui divergir do playbook, o playbook vence.

## Manutenção desta skill
- Ela pousou fisicamente na árvore do profile `cuidar` (skills/marketing compartilhado com o cmo): `skill_manage` de patch/write_file a partir do cmo é barrado pelo guard de perfil; rota de edição = file tools com cross_profile=True ou shell no profile cuidar.
- Fusão futura prevista: consolidar na `squad-postagens-cuidarvc` quando a rota de file tools cross-profile abrir (mesmo plano da `delegar-codigo-grande`).
