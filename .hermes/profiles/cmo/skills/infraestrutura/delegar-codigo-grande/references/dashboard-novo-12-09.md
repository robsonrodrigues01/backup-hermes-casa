# Dashboard novo do cuidar.vc — episódio 12/09 — ENCERRADO (troca oficial concluída)

Registro do primeiro uso da receita (delegação ao CTO Opus 5). Troca oficial concluída 12/09 19h50 BRT após OK do Rob. Fios que seguem abertos no fim.

## O que existe
- **Novo**: `cuidarvc/squad/dashboard/dashboard-novo.py` (~74KB, single-file stdlib, porta via env `DASH_PORT`, default 8800). **NO AR OFICIALMENTE na 8800** (sem DASH_PORT) desde 12/09 19h50 BRT: health `{"ok":true}`, 403 sem token, 200 público com token, abas novas confirmadas no HTML servido.
- **Antigo**: `cuidarvc/squad/dashboard/dashboard.py` (v2 esteira + v3 cockpit) **PARADO**, mantido como backup. Mesma rota Caddy `/dash`, zero mudança de link pro Rob.
- Briefing-fonte da verdade da tela: `cuidarvc/squad/dashboard/BRIEF-NOVO-DASH.md` (3 abas, regras de ouro, checklist de autoteste).
- Autenticação: mesmo `dashboard-token.txt` (403 sem token na raiz e nas APIs; `/api/health` ficou aberto).
- Boards de aprovação: v1 `board-dash-novo.png`, v2 com fundo corrigido `board-dash-novo-v2.png` (4 painéis numerados: HOJE, CALENDÁRIO, RESULTADO, PREVIEW).

## Especificação que a tela cumpre (resumo do briefing do Rob)
- 3 abas: HOJE (frase de estado, PRECISA DE VOCÊ, VAI AO AR 24H, esteira 6 etapas sem etiqueta de etapa no cartão, estados honestos "aguardando copy"/"incompleta", faixa de agentes no rodapé com bolinha cinza = aguardando horário e botão "rodar agora"), CALENDÁRIO (título "Setembro de 2026", dias de outro mês sem borda, contador "setembro: X publicados, Y agendados, Z só pautados"), RESULTADO (cada número com fonte; "sem dado" quando não existe fonte; série exige 7 dias de histórico).
- Preview de peça clicável em TODAS as abas (drawer `#dr`/`#ov`/`#drc`; abre via delegation em `[data-p]`; Esc fecha e restaura scroll; imagens pesadas carregam depois da moldura).
- Zero: caminho de arquivo, id interno de conta, JSON cru, markdown cru, undefined/null/NaN, travessão (—), UTC. Tudo BRT no mesmo formato "dd/mm às HH:MM".

## Correções que o CMO fez no pós-entrega (antes de mostrar ao Rob)
- Frase de estado contradizia o card de 24h (contava só agendadas; card listava pautada sem hora) → "nada com hora marcada nas próximas 24h" quando há pautada na janela.
- Rodapé 11px ciano a 60% sobre fundo claro → 12.5px `rgba(15,50,90,.6)` (era PALIATIVO sobre o branco do bug do `fixed`; revertido a `rgba(186,224,245,.75)` na rodada 2).
- Títulos de seção (`.card h2`) 12px → 13px (letra pequena com letter-spacing fazia a visão auxiliar ler "ESTEIRA" como "ESTÍBA"; texto no DOM sempre esteve certo).

## Rodada 2 (12/09, 19h35-19h45): fundo branco sufocando o glass
- Voz do Rob ao ver o board v1: "Tire o Background Branco, pois está sofocando o Glassmorfismo."
- **Causa raiz**: `background-attachment: fixed` no gradiente do body (`background:linear-gradient(160deg,#0284c7 0%,#0369a1 34%,#0c3a6e 72%,#082b57 100%) fixed`). Com `fixed`, o gradiente pinta só a altura da janela; em captura/print full-page o resto do documento fica BRANCO. O dashboard antigo que o Rob aprova NÃO tem `fixed` (gradiente corre o documento inteiro). Fix: remover `fixed` + rodapé de volta ao tom claro.
- Feedback registrado NA HORA em `gosto-do-rob.md`: fundo é sempre o gradiente azul profundo contínuo, o vidro NUNCA fica sobre área branca (branco só em elemento pequeno intencional, tipo pílula da aba ativa).
- Verificação por pixels (PIL): média RGB nas faixas de 5/25/50/75/92% da altura → azul escuro dominante em todas (92% = (31,69,114)); na última linha (99%) a captura ainda dá branco, mas é a TARJA de captura (ver abaixo), não a página.
- **Tarja branca da captura full-page**: screenshots saem ~30-50px mais altos que o documento; a sobra além do fim do body é branca. Receita `trim_branco` usada na montagem do board (corta de baixo pra cima enquanto >85% das linhas amostradas são quase-brancas, máx 60px):
  ```python
  def trim_branco(im, limiar=235, max_trim=60):
      px = im.load(); W, H = im.size
      for corte in range(max_trim):
          y = H - 1 - corte
          claro = sum(1 for x in range(0, W, 8) if all(c > limiar for c in px[x, y]))
          if claro > (W // 8) * 0.85: continue
          return im.crop((0, 0, W, H - corte - 2))
      return im
  ```
- **Clique real validado (falso bug)**: clicar o card "Cuidando de quem cuida" na coluna PUBLICADA não abria o drawer. Não era bug de código: a coluna fica FORA da vista horizontal da esteira (container 1146px de largura vs scrollWidth 1442px em desktop 1280px; card em x=1288-1498). browser_click em elemento fora da vista = no-op silencioso. Caminho humano comprovado: `esteira.scrollLeft = esteira.scrollWidth` → re-snapshot → clique → drawer `on`, `aberto=true`, título "Cuidando de quem cuida". `fechar()` restaurou o scrollLeft salvo (Esc volta ao mesmo lugar, spec ok). Em mobile cada coluna ocupa 78vw (swipe natural). O delegation `[data-p]` se valida rápido com `el.click()` via console.
- Board v2 reenviado 19h45; PENDENTES.md atualizado com a rodada.

## Rodada 3 (12/09, 19h47-19h50): OK do Rob e troca oficial
- Rob: "ok" às 19h47 BRT. Troca executada na hora.
- **Swap**: `pgrep -af` + kill do antigo → subir `dashboard-novo.py` SEM DASH_PORT (default 8800). Validação: health `{"ok":true}` local, 200 público com token, 403 sem token, abas novas no HTML servido (curl SEMPRE com `?k=<token>`).
- **Vigia**: o antigo `42c6aa7c07c4` tinha SUMIDO do cron (não existia mais; ninguém relançaria o servidor se caísse). REFEITO como job `fbee0838b577` (schedule `"every 30m"` = repeat forever; script-only `--no-agent`; `scripts/vigia-dash-cuidarvc.sh` no profile cuidar): silencioso quando saudável (stdout vazio = não notifica), relança `dashboard-novo.py` se cair. Primeira execução real validou: detectou servidor saudável e não falou nada.
- **Squad ligada ao painel**: skill `squad-postagens-cuidarvc` passo 5 (Agendador) agora lê `squad/aprovacoes/aprovacoes-AAAA-MM-DD.md` do dia: peça BARRADO não agenda nem publica, APROVADO segue fluxo, RESOLVIDO é bookkeeping; pipeline nunca trava esperando o dono. Botões do painel gravam exatamente ali (endpoint `/api/decisao` → `decisoes.jsonl` + `aprovacoes-AAAA-MM-DD.md`); se a peça já foi publicada, nenhum dos dois botões aparece.
- **Briefing CMO**: job `8c20e6866ceb` atualizado via CLI (`hermes -p cuidar cron update`) para ler as decisões do painel no início de cada run e não repreguntar item já respondido na tela.
- **Show-before-swap validado como padrão**: mostrar o board antes de trocar funcionou; o Rob pediu 1 correção de gosto (fundo branco) ANTES da troca, não em produção. Reaplicar em toda troca de ferramenta que ele já usa.

## Fios que seguem abertos
- Community: botão "rodar agora" desativado no novo (job `b1c27fe585a1` existe no cron do profile cuidar; mapear se quiser o botão ativo). Faixa de agentes usa o job ativo do CMO `8c20e6866ceb`.
- Horários do cron no servidor são UTC; o novo converte para BRT na exibição (não "corrigir" para UTC de volta).
- RESULTADO: "cliques na bio" e "cadastros UTM" seguem "sem dado" até existir fonte; seguidores = followersCount real da conta via Zernio.

## Fusão pretendida
Quando uma sessão com acesso a file tools tocar `squad-postagens-cuidarvc` (profile cuidar): portar esta skill inteira para lá (`references/cto-claude-cli.md` + pitfalls no corpo) e apagar/absorver esta skill nativa do cmo, para manter a fonte única das skills operacionais do projeto. Até lá, esta skill nativa é a rota.
