# PENDENTES & PRAZOS — Claudinho (chefe: Rob)

> Regra de ouro: leia ESTE arquivo antes de responder "o que tá em aberto?", "o que falta?" ou "quais os prazos?".
> Manutenção: concluiu item → mova pra Feito · novo item → anote com a data · prazo → [até DD/MM].
> Por quê: memória pode falhar; este arquivo não. Atualizado em 2026-09-09.
> Régua de respostas (2026-09-09): dia-a-dia curto; análise de print/decisões detalhado. Rob cobra valor por token.

## Esperando decisão do Rob
- [ ] (Rob, 1 min): apagar a mensagem com o token `ghp_...` aqui do Telegram + ativar 2FA no GitHub
- [ ] (Rob, opcional 30s): apagar repo VAZIO_backup `backup-cuidarvc-repo` no GitHub (Settings → Danger Zone) — o repo do cuidar.vc de verdade já mora no robsoncoffy/cuidarvc
- [x] 10/09 00:59 Painel Mac (porta 9119) DESLIGADO e fora do boot — Rob não conectou o app; era o principal suspeito do martelo de 5-10min
- [x] 10/09 03:57 RESOLVIDO: Rob rodou sudo (disable+rm fantasma do sótão + daemon-reload) — porta 9119 livre, receitas apagadas. Higiene final: --replace removido do meu unit + daemon-reload + restart limpo agendado (paz-final, 45s) → ÚNICOreste: conferir amanhã que não houve morte nenhuma na noite (journal gateway) → CONFERIDO 12/09 09h Bsb: journal dos 4 gateways limpo desde 11/09 18h.
- [ ] Docker pra Maxun → monitoramento automático de sites (era4) — precisa senha de sudo; pedir no momento
- [ ] Canais premium Agent-Reach (X/Reddit/LinkedIn) → cookies de conta secundária + JINA_API_KEY (2 min no site)
- [~] PARKED pelo Rob (09/09): "esquece esse conselho por enquanto" — só retomar se ELE pedir

## Abertas (a meu critério)
- [~] 2026-09-11 Autonomia espalhada: constituição no SOUL de Claudemir e Claudete + cron briefing-matinal 9h Bsb nos 3 perfis de negócio (default/era4/cuidar). Observar 3 primeiros briefings (começa 12/09)
- [~] CÉREBRO era4 (2026-09-11): raio-X local FEITO — ~/.hermes/profiles/era4/brain/ com manual+raio-X+diário+snapshot dos arquivos de serviço+comercial. Falta a parte do Rob: criar o repo PRIVADO era4-brain + token fine-grained e me avisar aqui (o Claudemir engancha o commit diário). Instrução de 2 min enviada no recado do 11/09.
- [ ] Consolidar memória (teto em 95%) — pro curator; prioridade baixa

- [x] 2026-09-09 Skills leves instaladas + provadas: conselho-de-ia + skill-creator + agent-context-kit (cofre ok, leitura com fonte/data funcionando)
- [x] 2026-09-09 Nota: parcado gbrain (banco externo pesado); SOUL do agente-orquestrador capturado como anotação pra squads
- [~] [TODO] uv tool upgrade hermes-agent (1 commit atrás; traz plug de MCP que o cofre do kit quer usar) — BLOQUEADO 13/09 09h Bsb: tentativa no automático falhou, `__pycache__/jiter` em site-packages é dono root (Jun 16) e hermes não apaga. Precisa: `sudo rm -rf /home/hermes/.local/share/uv/tools/hermes-agent/lib/python3.12/site-packages/jiter/__pycache__` → depois `uv tool upgrade hermes-agent` (~1 min). Novo código só vale nos restarts dos gateways.

## Migração de servidor (kit pronto 2026-09-12)
- [x] Backup completo gerado: `/home/hermes/hermes-mudanca.zip` (334MB, 8561 arquivos, ~27s) — contém os 6 perfis inteiros (memórias, skills, SOUL, cron, .env com tokens dos bots). Restaura com `hermes import`
- [ ] Quando a máquina nova existir: copiar o zip pra ela → `hermes import` → religar gateways POR PERFIL → Headroom (`skill local-proxy-headroom`). Ver skill/index de migração anotado na conversa 12/09. ATENÇÃO: desligar gateways da máquina velha ANTES de ligar os da nova (1 token = 1 poller, senão colisão 409)

### Desenho squads + Conselho (proposta no papel — aguardando OK do Rob)
1. Grupo "Conselho" (os 3 bots + Rob): bots só falam quando @mencionados.
   Rob manda a ideia → cada bot dá opinião de 2-3 linhas do SEU domínio (Claudinho=casa, Claudete=cuidar, Claudemir=era4) → Claudinho consolida veredito (bots só falam quando @mencionados).
2. Squads por tarefa (duplas, sempre a cobaia primeiro):
   - Squad casa = Claudinho + Cobaia (as ideias da casa testam primeiro aqui)
   - Squad cuidar = Claudete + Cobaia
   - Squad era4 = Claudemir + Cobaia
   Cobaia = @bottesteerabot (perfil _lab_, já com Headroom testado).
3. Fluxo de skill: ACHADO (print do Rob) → Claudinho inventaria + valida repo → teste com prova real → pedir OK → distribui pro perfil certo → anota no PENDENTES.

## Feito recente
- [x] 14/09 **Cofre GitHub ao vivo** (`robsoncoffy/backup-live-hermes`, privado): 16.318 arquivos = casa toda conteúdo real (6 perfis, skills, projetos, ferramentas) + Release `migracao-2026-09-12` com zip 351MB anexado. Cron `backup-cofre-github-diario` (17h Bsb): push git diário; dia 1 de cada mês cria Release com zip COMPLETO (inclui diários state.db). README no repo tem o passo-a-passo de restauração. Obs: o repo do cuidar.vc de verdade (robsoncoffy/cuidarvc) jámtarlá é backup do cuidarvc/repo (local tá 14 commits atrás, nada perdido).
### Kit de ativação (pré-montado — dispara com SIM do Rob)
1. Rob cria grupo "Conselho" no Telegram e adiciona: @claudinhovc_bot, @claudetezinhabot, @Claudemirera4bot, @bottesteerabot.
2. Claudinho grava regra do Conselho no SOUL dos 3 perfil-bons: opinar 2-3 linhas do SEU ramo, só quando @mencionado; Claudinho consolida veredito.
3. Teste ordem: cobaia primeiro (lab) → grupo real. Fluxo dos prints entra no mesmo lote.
4. Atualizar MAPA.md (seção squads) + anotar data no mural.
- [x] 2026-09-09 Headroom (compressor) ligado nos 4 bots, verificado
- [x] 2026-09-09 marketingskills nos 3 perfis; last30days + agent-reach instalados
- [x] 2026-09-09 PENDENTES.md + MAPA.md criados (ideias do print Amora, aprovadas pelo Rob)

## Feito (14/09) — cofre GitHub refeito igual Rob pediu
Repo NOVO único: robsoncoffy/backup-hermes-casa (privado) — só casa Hermes (perfis c/ agents+subagents, skills, memórias, cron, PENDENTES/MAPA), 7384 arq, 260MB.
Fora por regra do Rob: logs de conversa (state.db -> zip mensal no Release), plugins de terceiros (gbrain/postiz/agent-vision -> reinstaláveis), binários. TOKENS AGORA SOBEM (pedido do Rob 14/09): .env ×6, mcp-tokens, gh-token, .git-credentials, .claude.json — 2FA no GitHub é o cadeado do cofre.
Envio a cada 4h (6x/dia Bsb, script backup-github.sh) + zip completo dia 1.
 Pendente p/ Rob decidir: aposentar backup-live-hermes (repo antigo cheio de terceiros) e apagar backup-cuidarvc-repo (vazio, criado por engano)?

## Plano economia Vultr (iniciado 15/09)
Passo 1 FEITO+PROVADO: cmo e cto -> glm-5.3-flash (config.yaml dos 2, rota 8789 testada ok proven).
Próximos (Rob aprovou plano? aguardando OK p/ seguir):
- Passo 2: lab -> glm-5.3-flash (cobaia), depois era4 e Claudinho (glm-5.1 moribundo, 404 recorrente, sumiu da lista Vultr)
- Passo 3: cuidar fica no glm-5.3 completo (fala com cliente — mantém qualidade)
Meta: conta ~US$2700 -> ~US$400/mês.

## Plano economia Vultr (iniciado 15/09)
Passo 1 FEITO+PROVADO: cmo e cto -> glm-5.3-flash (configs trocadas; rota 8789 testada ok).
Próximos:
- Passo 2: lab -> glm-5.3-flash (cobaia), depois era4 e Claudinho (glm-5.1 moribundo, 404 recorrente, sumiu da lista Vultr)
- Passo 3: cuidar fica no glm-5.3 completo (fala com cliente — mantém qualidade)
Meta: conta ~US$2700 -> ~US$400/mês.

## Plano economia Vultr (15/09)
Passo 1 FEITO e PROVADO: cmo e cto trocados p/ glm-5.3-flash (configs; rota 8789 testada ok).
Passo 2 FEITO e PROVADO: lab, era4 e Claudinho -> glm-5.3-flash (rotas 8787/8790/8788 testadas ok).
Passo 3: cuidar fica no glm-5.3 completo (fala com cliente).
Meta: conta ~US$2700 → ~US$400/mês.

## Projeto AGENTE TRADER (15/09, pedido do Rob)
Objetivo: agente que opera Polymarket+# prosecutors e gera caixa p/ pagar servidor+LLM (~US$400/mês pós-migração).
Feasibilidade PROVADA: servidor alcança CLOB Polymarket (200) e Kraken (200); Binance bloqueado (IP datacenter US).
Arquitetura: bot determinístico (código, estratégias + freios de risco) + Claudinho como supervisor (pesquisa/decisões agendadas, não roda trade a trade) — leitura: economiza tokens e evita decisão impulsiva de LLM.
Fases: 1) PAPEL (simulado, 7 dias, nada real) 2) real com carteira pequena + freios (perda-dia-máx, sem alavancagem, sem saque nas chaves) 3) escalar certinho se bater meta.
15/09 Rob aprovou: FASE 1 SANDBOX no ar. Bot de papel virtual US$10k (BTC/Kraken; Polymarket entra depois). Cron tick 15min (silencioso) + relatório diário 9h Bsb neste chat. Regras no código: 20%/op, lucro +1.5%, corte -2%, freio se perder $150 no dia. Meta sandbox: 7 dias úteis de dados até 22/09 — depois apresento resultado e fase 2 (dinheiro real, carteira separada) SÓ com novo OK do Rob.
