---
name: internal-tools-cuidarvc
description: Construir, estender e verificar artefatos internos do cuidar.vc que ficam FORA do repo (painéis HTML autossuficientes, relatórios, ferramentas do CTO entregues via Telegram). Inclui o painel-escritorio.html, a receita de gravar arquivos grandes em partes para não truncar a resposta, verificação de UI no browser stack do Hermes e entrega via MEDIA. Usar quando o Rob pedir painéis, visualizações ou ferramentas internas, ou quando um write_file grande puder estourar o limite de output.
---

# Artefatos internos cuidar.vc (fora do repo)

## Regra de fronteira
- Diretiva do Rob (15/09): o Claude Code+Opus 5 é o coder de TUDO, inclusive artefatos internos (painéis, relatórios, ferramentas). Artefatos internos continuam FORA do repo (/home/hermes/cuidarvc/, /home/hermes/painel-web/), nunca commitados. Fluxo: CTO monta o prompt objetivo, roda `claude -p "<tarefa>" --model opus --dangerously-skip-permissions` com workdir no diretório do artefato, depois revisa no browser, testa e publica. Ajuste pequeno também é código: passa pelo claude -p. Escrever fragmentos com write_file é só fallback para claude indisponível.

## Receita: Opus refaz/constrói artefato interno (15/09)
1. Se houver imagem de referência: cp pro workdir e citar o caminho no prompt (CLI do Claude não tem flag --image; o Read dele enxerga).
2. write_file do prompt em arquivo (prompt-vN.txt): estilo alvo descrito por inteiro, elenco exato, funcionalidades obrigatórias, regras (PT-BR, zero travessão, zero dependência externa, zero erro de console, 390px sem corte) e critério de pronto.
3. REGRA DE SEGURANÇA: mandar o Opus escrever em arquivo NOVO (ex: escritorio-v4.html), NUNCA sobrescrever o index.html que está no ar (o server.py serve ele direto; arquivo pela metade = painel fora do ar).
4. Rodar claude -p em background com timeout 1800 (tarefa grande passa do cap de 600s do terminal foreground); ver receita na skill claude-code-headless.
5. QA no browser ANTES de publicar: file:// no arquivo novo, assertions por DOM via browser_console, browser_vision só pra layout geral.
6. Publicar: cp do arquivo novo por cima do index.html (a rota /painel no Caddy já aponta pra ele) e validar externo (curl + check-host.net).

## Arquivo grande sem truncar a resposta
- write_file gigante numa resposta só estoura o limite de output (2 truncamentos reais em 14/09).
- Receita validada: fragmentos de até ~8KB e UM write_file por turno com prosa mínima (uma linha curta). 15/09: truncou 4x seguidas quando o turno carregava write grande + texto; com 4 fragmentos menores (5-8KB) e prosa de uma linha passou liso.
- Dois padrões de junção, via terminal: (a) fragmentos autônomos que só encadeiam o HTML: `cat p1 p1b p2 p3 > final.html`, sem strip; (b) fragmento anterior já fechou o `</head>`: `head -n -1 p1.html > final.html` antes do cat. CSS pode atravessar dois blocos `<style>` no mesmo head (válido, testado).
- Ajustes depois via patch direto no final.

## Verificação de UI no browser stack
1. browser_navigate aceita file:///. 
2. Assertions via browser_console com expression: NUNCA retornar string com emoji na expression (erro 'utf-8 codec can't encode surrogate'); usar textContent.length, ids, classes (count de .agent, .walk/.work, texto de plaquinha, relógio), contagem de erros.
3. browser_vision SÓ para layout/sobreposição. O headless não tem fonte de emoji colorida: emojis viram tofu e o modelo de visão descreve errado (chamou agentes de "badges com letras"). Não julgar renderização de emoji por screenshot.
4. Entregar só com zero erros de JS e movimento confirmado por DOM.
5. Painel-escritório: QA com a sonda canônica scripts/qa-painel.js (colar como expression no browser_console). O verde do script é FINAL: publicar e encerrar. Nunca retunar um estado que já passou e nunca repetir a mesma ação idêntica após resultado ruim (15/09: .lp width oscilou 68↔70 por ~40 iterações com o estado já verde, queimando contexto até a compactação; mesmo padrão num loop de memory replace).

## Publicação no servidor (painel no ar)
- Publicar sempre como rota no Caddy da 443 (domínio do VPS) fazendo proxy pro server.py stdlib em porta alta. IP:porta alta direto NÃO funciona de fora: firewall externo só libera 22/80/443 (14/09: o Rob pegou ERR_CONNECTION_TIMED_OUT no :8643 que eu tinha "testado").
- Prova de acesso externo: check-host.net na URL pública (200 de vários países). browser_navigate/curl do Hermes rodam LOCAL: sucesso local não vale como teste externo.
- Rota no Caddy SEM sudo: POST /load na admin API 127.0.0.1:2019 (vale até o Caddy reiniciar; backup /tmp/caddy-backup.json antes). Morre no reboot: restart manual.
- Embed de app interno que bloqueia iframe (x-frame-options DENY) e usa chave na URL: proxy no próprio server.py, omitir o header, injetar a chave no HTML no servidor. Detalhes em references/publicacao-servidor.md.
- Caddyfile em /etc/caddy é enganoso; a config efetiva está na API admin http://127.0.0.1:2019/config/.

## Painel-escritório: regra de elenco (15/09, pedido do Rob)
- Mostrar SÓ quem trabalha no cuidar.vc: Rob, CTO, CMO, Dev, QA, DevOps, Claudete, Planejador, Copy, Artes, QC, Agendador, Métricas.
- Agente pessoal do Rob (Claudinho) NÃO é pessoa do escritório; o papel técnico aparece só como "CTO".
- Rob reprovou a v1 de "muito feia": capricho visual (paleta quente, zonas rotuladas, sombras, plaquinhas legíveis, mesa longa da squad de conteúdo) é requisito, não detalhe opcional.

## Entrega
- HTML autossuficiente (zero dependências externas): entregar com MEDIA:/caminho na mensagem, o Rob abre no navegador do celular/PC. Se o Rob quiser link online, publicar no servidor (ver seção acima).
- Dados de status embutidos devem ser re-verificados na hora (cronjob action=list, TAREFAS.md) antes de gerar; nunca embutir status inventado.

## Pitfalls
- Patch em innerHTML por replace: conferir que nenhum token vizinho foi perdido junto (14/09: remover a tag de nome levou o emoji do agente embora).
- Plaquinha de status só atualiza se tiver id="st-<id>" correspondente ao agente no array JS.
- Estilo do Rob vale aqui também: PT-BR, zero travessões, mensagens curtas.
- Comando de junção/publicação NUNCA encadeia rm: o guard de consentimento do terminal pode travar o comando inteiro por timeout sem resposta (15/09: join+cp+rm bloqueado e o fluxo parou esperando o Rob). Junção/publicação em comando inofensivo; limpeza de fragmentos depois, separada (ou nunca: fragmentos sobrando são inofensivos).
- A skill dev-cuidarvc (playbook da squad) NÃO pertence ao profile cto: é symlink de /home/hermes/.hermes/profiles/cuidar/skills/devops/dev-cuidarvc. skill_manage se recusa ("skill not found in active profile"); patch via ferramenta de arquivo exige cross_profile=True. Editar ali é legítimo quando o Rob dá regra da squad (ex: "Opus coder de tudo", 15/09, já gravada no playbook).

## Referências
- Painel do escritório (estrutura, como estender, dados embutidos): references/painel-escritorio.md
- Publicação no servidor + embed do dash do CMO (topologia, proxy, chave): references/publicacao-servidor.md
