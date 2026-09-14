---
name: claude-code-headless
description: "Operar o Claude Code CLI em servidor headless (Hermes). Instalar, logar sem browser (paste-code via PTY), rodar claude -p, fixar modelo padrão (settings.json) e evitar pitfalls do sanitizador. Usar ao plugar, usar ou consertar o Claude Code em qualquer projeto do servidor."
---

# Claude Code em servidor headless (Hermes)

## Quando usar
- Instalar, autenticar ou rodar o Claude Code CLI numa máquina sem browser e sem terminal interativo (o caso do Hermes).
- Diagnosticar erros de auth (login caído, token expirado) e fluxos OAuth de CLIs parecidos (padrão paste-code).

## Instalação
- `npm install -g @anthropic-ai/claude-code` falha com EACCES neste servidor. Não insistir.
- Instalador nativo que funciona: `curl -fsSL https://claude.ai/install.sh | bash` (vai pedir aprovação do pipe; binário cai em `~/.local/bin/claude`).
- Todo uso precisa de `export PATH="$HOME/.local/bin:$PATH"`.
- Credenciais vivem em `$HOME/.claude`. Conferir `echo $HOME` antes de operar: no profile cto o HOME do terminal hoje é `/home/hermes`.

## Login headless (procedimento comprovado em 12/09/2026)
1. `terminal` com `background=true` e `pty=true` rodando `claude auth login --claudeai` (assinatura Claude; `--console` é API paga por uso).
2. O CLI imprime `https://claude.com/cai/oauth/authorize?...` e espera em "Paste code here if prompted >".
3. Mandar a URL pro usuário no chat. Ele abre no dispositivo dele, autoriza e recebe um código no formato `CODIGO#STATE`.
4. `process(action=submit)` com o código colado por inteiro. O PTY do claude ACEITA submit (diferente do gh auth login, que travava).
5. Verificar com `claude auth status`: precisa mostrar `"loggedIn": true`. Credenciais ficam em disco, o token nunca passa pelo contexto do agente.
- Fluxo que dependa de abrir browser na própria máquina não existe aqui: paste-code é o caminho.

## PITFALLS
1. **`claude setup-token` é armadilha no Hermes.** Ele imprime o token de 1 ano no stdout do PTY, o sanitizador do Hermes mascara com asterisks no log/poll e o setup-token NÃO grava nada em disco. Resultado: token perdido e o usuário precisa autorizar de novo. Regra geral: fluxo de credencial que imprime segredo no output não serve neste ambiente, prefira fluxo que grava em disco.
2. Se precisar do token como env var (`CLAUDE_CODE_OAUTH_TOKEN`), faça o OAuth manual com PKCE próprio num script que grava direto no .env sem printar (padrão da skill mcp-oauth). Dados do client e transcrição da sessão em `references/login-claude-code.md`.
3. O sanitizador do Hermes também mascara segredos literais em comandos e write_file: nunca escrever valor literal, extrair de disco ou DB via script.
4. **Subcomando desconhecido vira prompt (v2.1.270, verificado 12/09).** `claude model list` e `claude config set -g model X` NÃO existem como subcomandos: o CLI engole o texto como se fosse prompt e gasta uma chamada respondendo algo conversacional (ex: "olá, estou pronto..."). Sinal de que era prompt: resposta em linguagem natural sobre o tema. Antes de usar subcomando duvidoso, rodar `claude <sub> --help`; erro de opção desconhecida confirma que não existe.

## Modelo (definir e verificar)
- `--model` aceita alias (`opus`, `sonnet`) ou nome completo (`claude-opus-5`); vale só para aquele comando.
- Padrão global (jobs cron, squad): escrever `~/.claude/settings.json` com `{"model": "opus"}`. O arquivo pode não existir, criar na mão. `claude config set` não serve (vira prompt, ver PITFALLS 4).
- Verificar de verdade, sem acreditar em doc: `claude -p "Responda em UMA linha: qual o nome exato (id) do modelo que está respondendo agora?"` com e sem `--model`. O modelo responde o id (testado 12/09: com `--model opus` e com settings.json default, ambos responderam `claude-opus-5`).

## Uso no dia a dia (squad tech)
- Rodar headless dentro do repo: `cd <repo> && timeout 900 claude -p "<tarefa objetiva, com contexto e critério de pronto>" --model opus --dangerously-skip-permissions`.
- Modelo padrão da squad: Opus 5 (diretriz do Rob 12/09), fixado no settings.json + flag `--model opus` na linha por segurança.
- Sem `--dangerously-skip-permissions` o modo -p bloqueia edição de arquivo e comandos: em job autônomo é obrigatório. Nunca rodar sem timeout.
- Convenções do projeto: o CLAUDE.md na raiz do repo é a fonte autoritativa (git pull antes, git push depois, edge function só publica via agente Lovable, build é `npm run build` com tsc -b). Ler antes de delegar qualquer tarefa.
- O `.env` versionado no repo do cuidar.vc é proposital (só as 3 variáveis públicas VITE_*): não remover nem "corrigir".
- Detalhes da sessão de setup e fallbacks: `references/login-claude-code.md`.
