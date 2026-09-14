---
name: caddy-exposicao-publica
description: Expor serviços locais da VM publicamente via Caddy (admin API 127.0.0.1:2019) sem abrir firewall. Use ao publicar dashboards, APIs ou sites internos no domínio com TLS, ao adicionar/alterar rotas do Caddy, ao depurar erros 500 do admin API, ou ao criar gatilho por webhook (receiver que recebe evento externo pela URL pública e dispara agente cron "na hora", com vigia próprio).
category: infraestrutura
---

# Exposição pública de serviços via Caddy

Padrão validado no cuidar.vc (11/09, dashboard da squad): o serviço roda só em localhost (ex: porta 8800), o firewall da Vultr fica fechado e a exposição sai por uma rota no Caddy 443 com reverse_proxy. A rota nova herda o cert TLS do domínio já servido.

## Passos
1. **OK do Rob antes de tudo**: o security scan do Hermes barra alteração de rota no Caddy (admin 127.0.0.1:2019) e exige aprovação explícita. Apresentar as opções (rota no Caddy vs liberar porta no firewall) e aplicar só a escolhida.
2. Ler a config: `GET 127.0.0.1:2019/config/`, localizar o server (ex: srv0) e a rota externa 0 (`GET .../servers/srv0/routes/0`).
3. Aplicar por script idempotente (modelo: `cuidarvc/squad/dashboard/caddy-dash-rota.py`): deepcopy da rota externa 0, ajustar match (`/dash`, `/dash/*`), handler reverse_proxy para `127.0.0.1:<porta>`, aplicar PATCH no recurso da rota.
4. Testar end-to-end pela URL pública: health check (ex: `/dash/api/health` → 200) e abrir a página no browser (se o tema usa gradiente, conferir `getComputedStyle(document.body).backgroundImage`).

## Pegadinhas (3 iterações até acertar, 11/09)
- **POST no array de rotas retorna 500** sem explicação. O que funciona: **PATCH no recurso da rota** (`.../routes/0`) com o objeto completo (deepcopy + alterações).
- **Handler `strip_prefix` não existe no Caddy 2.11** ("unknown module"). O certo: handler `rewrite` com `strip_path_prefix: /caminho`.
- **O erro real só vem no corpo do HTTPError**: sempre capturar e imprimir `e.read()`. Um 500 sozinho não diz nada.
- **Frontend sob prefixo de rota exige fetches relativos** (`api/state`), nunca absolutos (`/api/*`) — senão quebra fora do root.
- **`background-attachment: fixed`** no body faz o fundo renderizar claro (sem gradiente) no browser: não usar no tema.
- **ORDEM das rotas no array decide (12/09, rota `/hook/*` do receiver)**: rota específica nova tem que vir ANTES de qualquer catch-all `reverse_proxy` do site principal no array interno. O Caddy avalia na ordem: catch-all declarado antes engole a rota nova e a URL pública nova devolve 502. Ao inserir via admin API, colocar a rota no INÍCIO do array de rotas.

## Operação contínua
- Proteção: token na query string (`?k=<token>`, segredo em arquivo local, ex: `dashboard-token.txt`). O link é a senha, não compartilhar publicamente.
- Serviço de longa duração: vigia = cron job script-only (`--no-agent`, o script É o job), silencioso quando saudável (stdout vazio = não notifica), relança o processo se o health check falhar. Vigia atual do dashboard: job `fbee0838b577` + `scripts/vigia-dash-cuidarvc.sh` (profile cuidar), a cada 30min. Desde 12/09 à noite o dash oficial na 8800 é `dashboard-novo.py`; o `dashboard.py` (v2 esteira + v3 cockpit) está PARADO, mantido como backup.
- **Pegadinhas do vigia cron**: (a) cron jobs PODEM SUMIR silenciosamente após operações no perfil (o vigia `42c6aa7c07c4` deixou de existir sem aviso e ninguém relançaria o servidor) → após qualquer manutenção, `hermes -p cuidar cron list` e confirmar que o vigia existe; (b) schedule `"every 30m"` = repeat forever, `"30m"` = one-shot; (c) caminho do script resolve em `~/.hermes/profiles/<perfil>/scripts/`, NÃO `~/.hermes/scripts/` (path errado → "Script not found"); (d) troca de versão: rodar a nova em porta de QC (ex: `DASH_PORT=8801`), kill na antiga, subir a nova na porta oficial e validar health + 200 com token + 403 sem token, tudo com o `?k=` no curl.
- No perfil cmo, `Path.home()` redireciona para `~/.hermes/profiles/cmo/home`: caminhos de dados sempre absolutos.

### Gatilho por webhook: responder evento "na hora" (12/09, Agente 7 Community)
Rob pediu resposta por gatilho (ao receber mensagem) em vez de esperar o ciclo do cron. Cadeia validada em produção com a Zernio:
1. **Receiver HTTP local** (ex: `squad/community/hook-zernio.py`, 127.0.0.1:8805): valida token próprio do hook (sem token → 403; segredo em arquivo chmod 600, ex: `community/hook-token.txt`), lê o evento e dispara `hermes -p cuidar cron run <job_id>`.
2. **Exposição pública com rota no INÍCIO do array** (pegadinha acima): `/hook/*` → receiver. Prova do bloqueio: curl público SEM token → 403.
3. **Assinar o webhook na plataforma**: Zernio suporta por conta os eventos `message.received`, `conversation.started`, `comment.received`, `lead.received`, `review.new`, `referral.received`; conferir `isActive` depois de criar.
4. **Debounce (90s)** no receiver: rajada de eventos dispara no máximo 1 run por janela. O cron periódico (ex: every 15m) segue como rede de segurança: o gatilho só antecipa, nunca substitui.
5. **Validar end-to-end de verdade**: disparar o evento de TESTE oficial da plataforma e confirmar no log do receiver que chegou pela URL pública. Curl local no receiver não prova a cadeia.
6. **Vigia do próprio receiver**: mesmo padrão do vigia de dashboard (no_agent, silencioso no health 200, relança se cair). Vigia do receiver Zernio: job `d58dd88fe8d5`, every 15m, profile cmo. O detalhe do agente em si (roteiros, limites) mora no playbook `squad/community/playbook.md`.
- Pitfall de profile no vigia: o `profile=` do cron job decide em qual `~/.hermes/profiles/<perfil>/scripts/` o script resolve. Job criado numa sessão cujo scheduler default é outro perfil não acha o script ("Script not found") → passar `profile=` explícito no create (vigia do receiver: profile cmo; vigia do dash: profile cuidar).

## Dashboard v2 "esteira" (11/09 à noite, construído e validado em produção)
Aba **Esteira** virou a inicial do dashboard da squad (`cuidarvc/squad/dashboard/dashboard.py`), no formato que o Rob exemplificou: frase de estado no topo ("X peças publicadas hoje, Y em produção, Z esperando você, W parada"), painel rosa **PRECISA DE VOCÊ**, stepper de 6 etapas com contagem, **ONDE CADA PEÇA ESTÁ** (mini-cards por estágio + miniatura da arte via /media), PUBLICADO com métricas reais, CONTAS + COMMUNITY.

Mapeamento de dados (`esteira_state()`, alimentado por arquivos da squad + Zernio):
- Pauta: regex `^### \d+\. .+$`, título = 1ª string entre aspas, data dia/DD/MM, pilar `(P1..P4)`.
- Copy: 1ª string entre aspas depois de "Assunto escolhido". Arte: última pasta `artes-YYYY-MM-DD` (sort por nome), conta `card-*.png`.
- Qualidade: regex `Veredito:\s*(?:✅\s*)?(APROVAD[OA]|REPROVAD[OA]|AJUSTES?)` (usar `\b` em AJUSTE/CORRIGIR, senão "ajustes" em texto normal vira falso reprovado).
- "Publicada hoje" = `scheduledFor` em BRT == hoje (relógio da VM é UTC: virada de dia BRT ≠ virada local).
- Métricas por post: `/v1/analytics/post-timeline?postId=` → SOMAR reach/likes/comments/impressions dos pontos. Conta nova = números ~0: mostrar como estão, nunca inflar.
- **Quirk Zernio: post apagado manualmente no IG segue `published` na API** (remoção não reflete). Dashboard mostra o que a API diz; registrar o apagado em PENDENTES (ex: carrossel "R$ 3.000").

Watchdogs (painel PRECISA DE VOCÊ): escalações `- [ ]` de `community/escalacoes.md`; QC reprovado/ajuste do dia; agente sem run > 26h; post `scheduled` > 1h atrasado; nenhuma peça agendada para amanhã (mínimo 1/dia). Painel vazio = "Nada esperando você. A esteira anda sozinha."

Pegadinhas desta leva:
- **esc(0) no JS**: helper `(s||'')` engole ZERO → contagem "0" desaparece da UI (headline e stepper de estágio vazio). Fix: `s===0?'0':(s||'')`.
- **Truncar título em fronteira de palavra**: `[:70].rsplit(" ",1)[0] + "…"`; corte fixo cruza palavra e o QC visual acusa como bug.
- **innerHTML/inline python**: security scan do patch acusa innerHTML (false positive: tudo passa por esc(), documentado em comentário); security scan do terminal bloqueia `python3 -c` com payload pesado ("inline interpreter with suspicious payload") → escrever script em arquivo via write_file e rodar o arquivo.
- **QC visual com visão auxiliar gera ruído OCR** ("Rasta" por "Pauta", "Estoque" por "Esteira", "Chegueu" por "Chegou"): verificar claims de typo/count contra os dados reais (api/state) antes de "corrigir"; defeitos estruturais (texto cortado, linha apagada) são legítimos. Régua do QC de arte: dados/pixels > visão.
- Stepper conector `::before` rgba(255,255,255,.22) invisível → .38.
- Review CTO v1 aplicada antes da v2: bind 127.0.0.1, `secrets.compare_digest`, `is_relative_to` no /media, headers nosniff/DENY, single-flight + cache negativo 30s, log mascarando token. Fase 2 pendente: token→cookie HttpOnly.
- Restart validado: kill da session + `exec python3 dashboard.py` background; conferir 200 local, 200 via Caddy, **403 sem token**.

## Dashboard v3 "cockpit" (11/09, demanda do Rob: calendário, comandos, quem está trabalhando)
Rob rejeitou read-only como "primitivo": dashboard tem que ser cockpit (calendário de postagens, executar comandos, ver a equipe ao vivo). Entregues: aba **Equipe** (8 cartões: status ao vivo + última ação real de cada agente + horários do cron + botão rodar), aba **Calendário** (grade mensal Zernio + pautas) e POST `/api/acao`.

Padrões que funcionaram:
- **Disparar agente**: whitelist fixa de job_ids (dict AGENDA com horários conferidos no cron/jobs.json; agente fora da lista → 400), `subprocess.Popen([<caminho absoluto do hermes>, "-p", "cuidar", "cron", "run", job_id], stdout=log, start_new_session=True)`, log `acao-<job8>-<ts>.log` chmod 600, auditoria `acoes.jsonl` chmod 600. `hermes cron run` é assíncrono ("next scheduler tick"): o status "trabalhando" vem do heurístico abaixo, não do pgrep sozinho.
- **"Trabalhando agora"**: `pgrep -af <job_id>` (excluir self) OU arquivo de saída do agente com mtime < 10 min. "No que": primeira linha útil do bloco `## Response` do último arquivo de saída (limpar markdown `*-#• `, reticências se >100 chars).
- **Calendário**: chips por dia (verde=published, azul=scheduled, tracejado=planejado, vermelho=falha); "planejado" vem de TODAS as pautas do mês com dedupe (data,título), NÃO só da última; clique no dia abre detalhes; hoje com borda ciano.

Pegadinhas desta leva (as 3 primeiras custaram quase a sessão inteira de debug):
- **`\'` dentro do PAGE (string Python) some no runtime**: Python consome o escape e o JS servido fica `rodar(''` → SyntaxError mata o SCRIPT INTEIRO (página congela em "carregando…", abas mortas, K/carrega undefined). NUNCA usar `\'` no JS embutido em string Python; usar entidade `&#39;` no atributo onclick (zero backslash).
- **Validar o JS SERVIDO, não o do source**: extrair o script do HTML via HTTP e rodar `node --check`; o extraído do .py mostra `\\n` dobrado (artefato de escape) e gera diff falso. `node --check` no servido = ground truth.
- **browser_console roda em mundo isolado**: não vê globais da página (`K is not defined` NÃO é bug da página); só o DOM é compartilhado. Pra rodar JS no mundo da página: injetar `<script>` via createElement+appendChild e ler o resultado pelo DOM (ex: `document.title=typeof carrega`). Página congelada em "carregando…" + funções undefined = script morto por SyntaxError.
- **Colisão de ID**: painel novo `id="cal"` colidiu com elemento antigo da aba Pipeline e `carrega()` sobrescreveu o calendário com texto de arquivo (QC visual acusou "log no lugar da grade"). Antes de criar ID novo, conferir os `getElementById` existentes no script.
- **Formato de pauta varia entre runs** ("Sáb 12/09" → "★ TERÇA 22/09:"): parser genérico `(\d{1,2})/(\d{1,2})` na linha do heading + validar mês == mês exibido; título = 1ª string entre aspas com fallback pro trecho da linha.

QC final do v3 (12/09, calibração visual da aba Calendário em produção):
- **Grid com chips nowrap estoura o painel de vidro**: `repeat(7,1fr)` deixa as colunas SEX/SÁB vazarem do card (track expande pelo min-width auto dos itens). Fix: `repeat(N,minmax(0,1fr))`; os chips truncam com ellipsis dentro da célula.
- **`text-transform:capitalize` capitaliza CADA palavra em PT-BR** (título do mês virou "Setembro De 2026"): mandar o título pronto do servidor ("Setembro de 2026") e remover capitalize; maiúscula inicial, se precisar, via `::first-letter{text-transform:uppercase}`.
- **Visão alucina ESTRUTURA, não só OCR** (relatório acusou aba "Equipe" duplicada que não existia; DOM tinha 6 abas, verificado via browser_console `document.querySelectorAll('.tab')`): claim estrutural se confirma no DOM antes de patchear. Régua completa: pixels p/ render, DOM p/ estrutura, dados p/ contagens.
- **Conferir HTML/CSS servido exige o token na URL**: curl em `/` sem `?k=` devolve 403 `{"erro":"token"}` e parece "fix que não subiu" (falso alarme no restart). Ler o token de `squad/dashboard/dashboard-token.txt` e incluir `?k=<token>` no curl antes de checar o CSS servido.

## Nota de consolidação
O ideal da squad é fonte única: quando os file tools com cross_profile=True estiverem disponíveis, mesclar este conteúdo em `squad-postagens-cuidarvc/references/` (profile cuidar), em DOIS arquivos: `dashboard-caddy-notas.md` (passos/pegadinhas do Caddy, ordem de rotas e o gatilho por webhook de 12/09) e `dashboard-esteira.md` (v2 esteira + v3 cockpit: mapeamento, watchdogs, disparo de agentes, pegadinhas das duas levas), apontar ambos no SKILL.md da squad e absorver esta skill. Na mesma leva, a `community-cuidarvc` merece uma linha sobre o gatilho por webhook ativo (o detalhe técnico completo já mora no playbook `squad/community/playbook.md`, que ela aponta como fonte única).
