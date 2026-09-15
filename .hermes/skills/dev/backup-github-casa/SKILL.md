---
name: backup-github-casa
description: "Colocar a casa Hermes (home inteira — perfis dos agentes, memórias, skills, projetos, ferramentas) num repo PRIVADO no GitHub — gitignore de lixo reinstalável, auditoria de blobs >100MB ANTES do push, zip grande como Release asset, push a cada 4h. Dispara em 'quero tudo no meu GitHub', 'nunca perder', backup de desastre."
---

# Backup da casa no GitHub (disaster recovery)

Objetivo: se a máquina morrer hoje, o Rob perde NADA de valor. No git vai só
arquivo de verdade; lixo que se reinstala/baixa sozinho em minutos fica fora.

## Quando usar
- Rob pede "tudo no meu GitHub" / "nunca perder" / backup completo da casa.
- Checkpoint da casa: antes de migração de servidor, mudança grande, mês virado.
- Caso irmão: repo de CÉREBRO por perfil → ver a skill agent-second-brain.
  Um token clássico com escopo `repo` serve pros dois repos.

## Escopo (regra do Rob, 14/09 — vale pra toda rodada de backup)
- **Repo novo limpo só com a casa Hermes** (perfis, agents, subagents,
  skills, memórias, cron, PENDENTES/MAPA, configs da casa). Rob desautorizou
  o cofre-mistura: NÃO agrupar projetos de terceiros (ex.: cuidarvc, plugins
  gbrain/postiz/agent-vision) nem "mexer em nenhum outro repositório" dele.
- Terceiro instalável = fora (reinstala em 1 comando). Repos do Rob mesmo
  vazio/errado = intocados; remoção só com OK explícito dele.
- Nome canônico atual: `backup-hermes-casa`. Legado `backup-live-hermes` e
  `backup-cuidarvc-repo` ficam congelados à espera da decisão do Rob.

## Fluxo (a auditoria de blobs vem ANTES do push — ordem importa)
1. Definir a RAIZ. A raiz do git define o escopo: casa toda = `git init`
   em /home/hermes. (14/09: comecei dentro de ~/.hermes e ficou raso;
   refiz por cima na raiz certa.)
2. Escrever o .gitignore ANTES do primeiro `git add`
   (starter: templates/gitignore-casa.txt). Regra: ignorar cache, venv,
   node_modules, binário que se baixa sozinho e índice gerado
   (`index-cache/`, `.local/share/claude/`, `.local/share/uv/`).
3. Inventariar o que sobra de real (`find` com prune + contagem por pasta).
   NÃO usar `git ls-files | wc -l` como "total de arquivos": com submódulos
   ele colapsa uma árvore inteira em 1 linha (2463 vs ~24.800 reais na casa).
4. **Auditar blobs:** scripts/auditar-blobs.sh 90. O GitHub RECUSA arquivo
   >100MB no git (push quebra, hard fail). Corrigir célere:
   gitignore no caminho + `git rm -r --cached <caminho>` +
   `git commit --amend` + `git reflog expire --expire=now --all` +
   `git gc --prune=now`. Sem o gc o blob fantasma segue no histórico
   e o push quebra do mesmo jeito. Fazer isso ANTES do primeiro push
   (depois de publicado, apagar histórico exige force-push).
5. Pedir o token ao Rob (passo único de 2 min, padrão pronto na skill
   rob-comms-style item 8). No servidor, o scanner de segurança mascara
   strings tipo token/KEY= em comandos → ler o token de arquivo ou montar
   o literal dinamicamente; nunca colar o segredo direto no comando.
6. Criar repo PRIVADO `backup-hermes` e push. Confirmação: `git log
   --oneline -1`, `git ls-files | wc -l`, `git count-objects -vH`,
   `git status --porcelain | wc -l` = 0, e local=remoto:
   `[ "$(git rev-parse HEAD)" = "$(git ls-remote origin main | cut -f1)" ]`.
7. Snapshot pesado (>100MB, ex.: zip de migração de 334MB) NÃO vai no git:
   anexar como **asset de Release** (limite ~2GB por asset lá).
   Roteiro comprovado: scripts/criar-release-zip.sh (cria e faz upload
   via API; leitura do token de arquivo externo; prova: 351MB ok em 14/09).
8. Cron diário: `git add -A && git commit && push` no repo; quando não
   muda nada, termina silencioso. POLÍTICA DE SEGREDOS — flip do Rob
   (14/09, 'sobe os tokens tb'): `.env` dos perfis, `mcp-tokens/`,
   `secrets/gh-token`, `.git-credentials` e `.claude.json` SOBEM no cofre
   privado (casa auto-suficiente: clone + tokens que estão no próprio
   repo = pé de pé sem colar chave). Condição: 2FA no GitHub é o
   cadeado de todas as fechaduras. Email do GitHub 'token detectado'
   = normal, é o cofre dele — ignorar.
** Quando criar o cron com a ferramenta de agendamento: o script precisa
   estar dentro de `~/.hermes/scripts/` e referenciado RELATIVO a ela
   (ex.: `backup-github.sh`); (erro literal: "Script path must be relative"); no_agent=True
   para backup silencioso; erro de push precisa subir como retorno de saída
   para não falhar em silêncio.

## Pitfalls
- **Gitlink de submódulo (mode 160000):** qualquer pasta com `.git` dentro
  vira 1 linha no git e o CLONE não traz os arquivos dela. Decidir por
  clone: manter (snapshot fica no zip/Release) ou remover o `.git`
  interno antes do add. A lista dos 12 encontrados + peso de cada:
  references/submodulos-observados.md.
- `git status --porcelain | wc -l` antes do commit conta linhas de STAGED
  ("A") — não é "resíduo não commitado" (zero válido só depois do commit).
- Revisar o .gitignore depois de escrevê-lo (houve linha embaralhada na
  gravação e reequilíbrio de filtros: nada de ignorar projeto demais).
- **Arquivo que CRESCE (state.db SQLite dos perfis) não é "abaixo do teto"
  nunca:** passou da auditoria 92MB e, no PUSH, o REMOTE recusou a 113MB
  ("remote: error: File ... exceeds GitHub's file size limit") — a
  auditoria só olha um instante. Regra durável: `state.db`, `*.db-wal`,
  `*.db-shm` FORA do git sempre (gitignore); banco vive no zip do Release.
- **Escopo `repo` do token NÃO deleta repo via API** (403; precisaria
  `delete_repo`). Repo vazio sobrando → limpeza manual pelo Rob:
  Settings → Danger Zone; não gastar turno nisso.
- **.gitignore editado após `git add` não solta nada — nem com
  `git rm -r --cached .`**: reindexação confiável = `rm -f .git/index &&
  git add -A`, conferindo `git ls-files | grep -c <padrão>` = 0. Prova
  14/09: index-cache e binários dos perfis só saíram com o index zerado
  (7394→7384 arq, 645→260MB).
- **Push grande (~260MB) morre com HTTP 408 / "unexpected disconnect"**:
  antes do 1º push, `git config http.postBuffer 524288000` (+
  `http.lowSpeedLimit 0`, `http.lowSpeedTime 999999`); o retry no mesmo
  comando sobe. Depois trocar o remote p/ URL sem token e deixar o auth no
  credential.helper `store` — o push diário do cron autentica sozinho.
- **Scan de token dá falso positivo em binário** (ELF com `ghp_...` por
  coincidência — caso `tirith`, 38MB×5 perfis): usar `grep -lI` (pula
  binário) + `file <arq>` pra confirmar antes de apagar; binário
  reinstalável = fora do git (`profiles/*/bin/`).
- **Trocou o repo-alvo?** Atualizar TODAS as URLs dentro de
  `~/.hermes/scripts/backup-github.sh` (release mensal também aponta pro
  repo novo). O cron (no_agent) chama o script por nome, então só o
  conteúdo do .sh muda — não recriar o job.
- **PENDENTES.md é quadro compartilhado entre agentes** — um irmão pode
  tê-lo editado no meio da sessão (a ferramenta de edição alerta "modified
  by sibling subagent"); ler sempre antes de editar pra não sobrescrever
  a nota do irmão.

## Referências
- templates/gitignore-casa.txt — starter do .gitignore da casa
- scripts/auditar-blobs.sh — auditoria de blobs (limiar MB como $1)
- references/submodulos-observados.md — 12 gitlinks + decisão

## Exemplo real (14/09, cofre definitivo)
/home/hermes → repo privado `robsoncoffy/backup-hermes-casa`, branch `main`:
7.384 arquivos rastreados (~260MB), escopo casa-only conforme a regra acima
(sem cuidarvc, plugins de terceiros, binários `tirith`, index-cache, logs
.headroom). Segredos DENTRO (flip do Rob 14/09): scan `grep -lI` = 23 arqs de
segredos espelhados (.env ×6, mcp-tokens, gh-token, .git-credentials,
.claude.json). 1º push
408 → postBuffer 500MB → subiu; 2 pushes de teste ok com remote limpo.
state.db/logs fora do git (zip mensal no Release do repo novo). Cron no_agent 0 */4 * * *
chama `backup-github.sh` (6x/dia Bsb: 1h/5h/9h/13h/17h/21h, mudou de
17h diário em 14/09); README do repo traz o passo-a-passo de
restauração. Legado `backup-live-hermes` (16.318 arq, cofre-mistura) ficou
congelado — histórico do caso anterior, CVE de escopo resolvida pelo Rob.