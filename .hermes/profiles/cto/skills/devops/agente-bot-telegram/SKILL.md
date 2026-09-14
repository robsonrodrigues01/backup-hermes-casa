---
name: agente-bot-telegram
description: Quando o usuário pedir para colocar um agente ou subagente (CMO, suporte, vendedor, etc.) DENTRO de um bot Telegram dedicado criado no BotFather, tipicamente colando um token e dizendo "coloque o X neste bot". Cria um profile Hermes isolado (soul, skills, ferramentas) com gateway e token próprios. Usar também quando o dono quiser conversar direto com um orquestrador num canal separado da DM principal.
---

# Agente em bot Telegram dedicado (profile Hermes)

Dar a um agente um corpo Telegram próprio = criar um **profile Hermes** isolado em `~/.hermes/profiles/<nome>/` com SOUL, skills, .env com o token do bot e um gateway systemd dedicado. Segue o modelo do Rob: **soul, skills e ferramentas** (persona + playbooks anexados + toolsets mínimos). O agente conversa bidirecionalmente com o dono no bot, lê e escreve os mesmos arquivos do projeto (filesystem compartilhado entre profiles) e dispara jobs de outros profiles via CLI.

## Passos

1. **Validar o token antes de qualquer config**:
   `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"` → deve retornar `{"ok":true,...,"username":"..."}`.
2. **Criar o profile clonado** do profile do projeto (herda model, provider, .env, SOUL e skills):
   `hermes profile create <nome> --clone --description "<papel do agente em 1-2 frases>"`
3. **Trocar o bot** (o clone traz o token do bot do profile de origem):
   `hermes -p <nome> config set TELEGRAM_BOT_TOKEN <token>`
   `hermes -p <nome> config set TELEGRAM_HOME_CHANNEL <chat_id do dono>`
4. **Soul**: REESCREVER `~/.hermes/profiles/<nome>/SOUL.md` com a persona do agente (o clone traz o SOUL do profile de origem!). Modelo pronto em `templates/soul-orquestrador.md`. Sempre embutir as regras de conversa do Rob: PT-BR, JAMAIS travessões, conversa econômica, janela de sono dele, onde ler estado do projeto (paths absolutos).
5. **Skills com fonte única**: o clone copia (cp) as skills e elas divergem com o tempo; substituir por symlink:
   `rm -rf ~/.hermes/profiles/<nome>/skills/<pasta> && ln -s ~/.hermes/profiles/<origem>/skills/<pasta> ~/.hermes/profiles/<nome>/skills/<pasta>`
   Validar: `hermes -p <nome> skills list` mostra as skills esperadas.
6. **Gateway**:
   `printf 'Y\nY\n' | hermes -p <nome> gateway install`
   São DUAS confirmações (start now + enable on boot), por isso as duas linhas Y. Conferir `hermes gateway list` (✓ <nome>) e o log `~/.hermes/profiles/<nome>/logs/gateway.log` deve mostrar "Connected to Telegram (polling mode)".
7. **Testar entrega**:
   `hermes -p <nome> send --to telegram:<chat_id> "teste..."`
   Saída `sent` = entregue. Erro 403 chat not found = o dono ainda não deu **/start** no bot (bot novo não inicia conversa): pedir pra ele abrir o bot e mandar /start.
8. **Jobs/briefings pelo bot novo**: criar via cronjob tool com `profile="<nome>"` e `deliver="local"`. O prompt do job instrui o envio via `send_message` (target telegram:<chat_id>), que sai pelo token do NOVO bot porque o job roda com o .env do profile novo. Não existe `context_from` entre profiles: o prompt manda LER os últimos outputs direto de `~/.hermes/profiles/<origem>/cron/output/<job_id>/` (só o mais recente de cada, leitura seletiva) e disparar redos com `hermes -p <origem> cron run <job_id>`.
9. **Silenciar o job antigo** equivalente no profile de origem (cronjob pause) SOMENTE DEPOIS do teste de entrega passar, senão duplica briefing na DM antiga. Registrar a reversão (`hermes cron resume <id>`) no arquivo de pendências do projeto.
10. **Registrar em todos os lugares**: pendências do projeto, skill da squad afetada, memória do profile de origem (novo canal do agente + job novo + job antigo pausado).

## Identidade visual do bot (foto de perfil)

O bot novo vem sem foto (avatar padrão). Dar um rosto ao agente faz parte do ritual (Rob pediu 11/09):
`curl -X POST "https://api.telegram.org/bot<TOKEN>/setMyProfilePhoto" -F photo=@avatar.png`
(multipart, campo `photo`; PNG quadrado ~1024px). Gerar o avatar na linguagem visual da marca (PIL/Krea) antes de aplicar. Confirmar visualmente no Telegram depois.

## Pitfalls

- **"Failed to enable unit: Unit file hermes-gateway-<nome>.service does not exist" com o arquivo existindo em disco**: sessões de profile rodam com HOME redirecionado (`HERMES_HOME=~/.hermes/profiles/<origem>`), então o install escreveu o unit em `<HERMES_HOME>/home/.config/systemd/user/` enquanto o systemd --user real lê `/home/hermes/.config/systemd/user/`. Fix: `cp <HERMES_HOME>/home/.config/systemd/user/hermes-gateway-<nome>.service /home/hermes/.config/systemd/user/` + `systemctl --user daemon-reload` + `systemctl --user enable --now hermes-gateway-<nome>`.
- `hermes gateway install` sem TTY trava nas confirmações Y/n: sempre pipe `printf 'Y\nY\n'`.
- `hermes send` NÃO aceita --platform/--chat-id: sintaxe correta é `hermes -p <p> send --to telegram:<chat_id> "msg"`.
- curl getMe/getUpdates pode dar 404/409 se o gateway já estiver pollando com o token: o log do gateway é a fonte de verdade, não o curl.
- Esquecer de trocar TELEGRAM_BOT_TOKEN ou de reescrever o SOUL após o clone sobe o bot errado com a persona errada: sempre itens 3 e 4 antes de subir o gateway.
