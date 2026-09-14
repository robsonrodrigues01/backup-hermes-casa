---
name: delegar-codigo-grande
description: Delegar geração de código GRANDE (arquivos novos de centenas/1k+ linhas, remakes, refatorações amplas) a um agente externo de código via CLI (Claude Code com Opus 5, o "CTO" do cuidar.vc). Use quando uma tarefa de código é grande demais para escrever à mão ou para o orçamento de um subagente Hermes, quando um delegate_task de código estourar iterações/truncar, ao dirigir o CLI `claude` a partir de uma sessão Hermes, ou ao verificar/entregar o resultado de um drop de código grande. Inclui as pegadinhas de PATH/HOME do CLI, a receita de briefing em arquivo, a disciplina de verificação própria (nunca confiar em autorrelato) e o método de QC de UI (DOM acima da visão auxiliar).
category: infraestrutura
---

# Delegar código grande ao agente externo (Claude Code CLI)

Contexto desta deployment: o "CTO" do cuidar.vc = Claude Code CLI rodando com Opus 5 na VM (Rob, 12/09: "peça o CTO para ajudar com o código, ele possui o opus 5 via cli"). Esta skill é nativa do profile cmo; o destino final pretendido é virar `references/cto-claude-cli.md` + pitfalls na skill `squad-postagens-cuidarvc` (profile cuidar, fonte única das skills de marketing), assim que uma sessão com acesso a file tools fizer o merge.

## Quando usar (e quando NÃO)
- **Use**: arquivo novo grande, remake completo de tela/serviço, refatoração ampla, qualquer código que precise de dezenas de leituras de arquivo + escrita de 500+ linhas.
- **Não use**: código pequeno (escreva direto), revisão pontual (subagente serve), tarefa que cabe em 1-2 write_file.
- **Por que delegate_task falha nisso (episódio 12/09)**: subagente Hermes tem orçamento de ~20 api_calls; ele queimou tudo em recon (relendo arquivos que o contexto já descrevia), nunca escreveu o arquivo, e a resposta final truncou após 3 tentativas de continuação.

## Onde está o CLI e pegadinhas de PATH/HOME
- Binário: `/home/hermes/.local/bin/claude` (instalação native; v2.1.270 na validação de 12/09).
- **NÃO está no PATH dos terminais de profile**: o HOME do terminal aponta para o sandbox do profile (`/home/hermes/.hermes/profiles/<p>/home`), então `which claude` vem vazio e `~` expande errado. Sempre caminho absoluto.
- Rodar sempre com `HOME=/home/hermes` (senão o CLI procura config/auth no sandbox do profile e não acha).
- **`--acp --stdio` NÃO existe** no CLI ("unknown option '--acp'") → `delegate_task acp_command='claude'` não serve. Use o modo print: `claude -p`.
- Smoke test barato antes de job grande (~30s, valida auth):
  `cd /tmp && HOME=/home/hermes timeout 90 /home/hermes/.local/bin/claude -p "Responda apenas: OK opus" --model opus --dangerously-skip-permissions`

## Receita validada (dashboard-novo do cuidar.vc, 12/09)

1. **Briefing completo em arquivo .md no diretório do projeto** (write_file), com:
   - objetivo e para quem é (a pergunta que a tela/entrega responde em 10 segundos);
   - spec detalhada por parte/aba/tela com TODAS as regras;
   - **regras de ouro**: o que NUNCA pode aparecer (caminho de arquivo, id interno, JSON cru, markdown cru, undefined/null/NaN, travessão —, etc.);
   - fontes de dados com paths absolutos + formato resumido de cada arquivo;
   - **Definição de Pronto como checklist executável** (compile, porta, curl com/sem token, DOM, responsividade).
   O CLI lê os arquivos de dados sozinho; não cole conteúdo de arquivo no prompt.
   Exemplo vivo: `cuidarvc/squad/dashboard/BRIEF-NOVO-DASH.md`.
2. **Rodar em background** (`terminal background=true`, `notify_on_complete=true`), com `cd` INLINE no comando (⚠️ NÃO passe `workdir=` junto com `background=true`: falha com "Invalid command: expected string, got NoneType"):
   ```
   cd <diretório-do-projeto> && HOME=/home/hermes /home/hermes/.local/bin/claude -p "Você é o CTO do cuidar.vc. Execute integralmente o briefing do arquivo BRIEF-X.md no diretório atual, do início ao checklist final. Responda com resumo curto em português." --model opus --dangerously-skip-permissions --add-dir <árvore-extra-fora-do-cwd>
   ```
   Um `--add-dir` por árvore fora do cwd (ex.: `~/.hermes/profiles/cuidar/cron/output`). Rodada típica: 10-30 min; o CLI tem loop de ferramentas próprio.
3. **Verificar TUDO você mesmo** (autorrelato do agente externo NÃO é verificado):
   - `python3 -m py_compile <arquivo>.py`;
   - processo vivo (`pgrep -af`) e porta respondendo; curl COM e SEM token (403 esperado sem token; health pode ficar aberto, raiz e api NÃO);
   - conteúdo de tela via DOM (browser_console: `textContent`, `getComputedStyle`, cssRules), nunca por leitura de screenshot;
   - screenshots por aba para o board de aprovação.
   Episódio: o CLI alegou "sem token dá 403" (era só da raiz; health ficou aberto sem eu pedir).

## Verificação de UI: DOM acima da visão auxiliar (método 12/09)

- **Texto na tela = verdade no DOM.** O modelo de visão auxiliar lê ERRADO texto pequeno com letter-spacing ("ESTEIRA" → "ESTÍBA"), datas ("12/09 às 12:03" → "14/09 às 10:00") e inventa detalhes ("made in Brazil" num rodapé que diz outra coisa). Antes de patchear qualquer "defeito de texto" reportado por visão: confirme via `browser_console` (textContent do elemento, getComputedStyle, `cssRules` do stylesheet).
- **"Defeito visual" acusado pela visão**: confirme no CSS/DOM antes de mexer (o "véu branco diagonal" era só o gradiente de fundo da página, design intencional).
- **browser_click em ref obsoleta "passa" sem efeito**: se a página tem auto-refresh/re-render (ex.: 60s), o ref do snapshot envelhece; o clique reporta sucesso mas não abre nada. Re-snap ou dirija via `browser_console` (`el.click()`, ou chame a função direto, ex.: `abrir(id, el)`).
- **browser_click em ref FRESCA também falha em silêncio se o alvo está fora da área visível de container com overflow** (kanban/esteira): clique reporta sucesso e nada acontece. Diagnóstico via console: `getBoundingClientRect` do alvo vs rect do container (`scrollWidth > width` = precisa rolar). Teste o caminho humano de verdade: `container.scrollLeft = container.scrollWidth`, re-snapshot, clique, confirme o ESTADO no DOM (flag `aberto`, classe `on`, título do drawer). O delegation em si se valida com `el.click()` via console; clicar node preso fora da vista não prova interação real.
- **Fundo que desbota pra branco no fim da página** (voz do Rob 12/09: "tire o background branco, está sufocando o glassmorfismo"): `background:linear-gradient(...) fixed` no body pinta só a altura da janela; em captura/print full-page o resto do documento vira BRANCO e os painéis de vidro parecem lavados. Gradiente de página NUNCA com `fixed`. Se a visão auxiliar descrever "fundo esvaindo de azul para branco/lavanda", confira `background-attachment` nas cssRules ANTES de aceitar como design. Regra da marca: vidro sempre sobre gradiente azul profundo, nunca sobre área branca (fonte: `cuidarvc/squad/gosto-do-rob.md`).
- **Contraste**: cor de texto depende do que está REALMENTE atrás. Texto claro translúcido (ex.: 11px, ciano a 60%) sobre área CLARA = ilegível; mas o rodapé escuro `rgba(15,50,90,.6)` era PALIATIVO sobre o branco do bug do `fixed`: corrigido o fundo, o correto é texto claro `rgba(186,224,245,.75)`. Antes de "corrigir" contraste, verifique o fundo real nos pixels.
- **Captura full-page sai ~30-50px mais alta que o documento**: sobra tarja branca na base de cada screenshot; antes de montar o board, corte as linhas quase-brancas da base (receita `trim_branco` em references/dashboard-novo-12-09.md).
- **Verificar gradiente de fundo por pixels** (PIL): média RGB em faixas a 5/25/50/75/92% da altura; saudável = azul escuro dominante (B > G > R) em todas; >90% de pixels quase-brancos em faixa central = bug de fundo.
- **Consistência entre elementos**: duas afirmações na MESMA tela não podem se contradizer. Episódio: frase de estado contava só peças com hora marcada ("nada agendado nas próximas 24h") enquanto o card ao lado listava peça pautada sem horário; fix = "nada com hora marcada nas próximas 24h".
- No console, evite redeclarar `const out` (contexto persiste entre chamadas): use IIFE `(() => {...})()`.

## Entrega pro dono (show-before-swap)

Tela/ferramenta nova que SUBSTITUI algo que o Rob já usa no dia a dia: mostrar board (1 imagem única em grid com badges numerados 1-N + legenda curta numerada; nunca N imagens separadas) e esperar o OK dele ANTES de trocar. Antes de compor o board: cortar a tarja branca da base de cada screenshot full-page (`trim_branco` no reference). Feedback de gosto dele entra em `gosto-do-rob.md` NA HORA (regra da squad); aprovação vale retroativo, o pipeline não espera. Enquanto isso, a versão antiga segue no ar e a nova roda em porta de QC (ex.: atual na 8800, nova na 8801 via env `DASH_PORT`). Pipeline de conteúdo não espera aprovação; troca de ferramenta em produção sim.

## Pegadinhas do terminal (Hermes) nesta classe de tarefa
- `terminal(background=true, workdir=...)` → erro "Invalid command: expected string, got NoneType". Solução: `cd <dir> && ...` inline no comando.
- `nohup ... &` dentro de comando foreground → rejeitado ("Use terminal(background=true)"). Servidor: `background=true` com `exec python3 arquivo.py`; depois `kill <pid>` + subir de novo com o mesmo padrão quando trocar código.
- Após patch em servidor que roda em background: `py_compile` antes, matar o processo antigo (pid via `pgrep -af`), subir de novo e SÓ ENTÃO confirme com curl que o novo código está no ar.

## Estado desta deployment (ver references/dashboard-novo-12-09.md)
Episódio 12/09 FECHADO: dashboard-novo entregue pelo CTO, aprovado pelo Rob (show-before-swap funcionou: gosto corrigido antes da troca, não em produção) e NO AR na 8800 desde 19h50 BRT. Vigia, squad e briefing CMO já operam sobre a versão nova. Detalhes e fios abertos em `references/dashboard-novo-12-09.md`.
