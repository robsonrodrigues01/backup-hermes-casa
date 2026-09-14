---
name: internal-tools-cuidarvc
description: Construir, estender e verificar artefatos internos do cuidar.vc que ficam FORA do repo (painéis HTML autossuficientes, relatórios, ferramentas do CTO entregues via Telegram). Inclui o painel-escritorio.html, a receita de gravar arquivos grandes em partes para não truncar a resposta, verificação de UI no browser stack do Hermes e entrega via MEDIA. Usar quando o Rob pedir painéis, visualizações ou ferramentas internas, ou quando um write_file grande puder estourar o limite de output.
---

# Artefatos internos cuidar.vc (fora do repo)

## Regra de fronteira
- A diretriz do Rob "Claude Code é o único coder" vale para arquivos do REPO (/home/hermes/cuidarvc/repo). Artefatos internos (painéis, relatórios, ferramentas do CTO) vivem em /home/hermes/cuidarvc/ FORA do repo, nunca commitados, e o CTO escreve direto com write_file/patch, sem claude -p.

## Arquivo grande sem truncar a resposta
- write_file gigante numa resposta só estoura o limite de output (2 truncamentos reais em 14/09).
- Receita validada: dividir em partes de até ~8KB. part1.html com HTML+CSS terminando em `</body></html>`, part2.html com `<script>` + `</body></html>`. Juntar via terminal: `head -n -2 part1.html > final.html && cat part2.html >> final.html`. Ajustes depois via patch direto no final.

## Verificação de UI no browser stack
1. browser_navigate aceita file:///. 
2. Assertions via browser_console com expression: NUNCA retornar string com emoji na expression (erro 'utf-8 codec can't encode surrogate'); usar textContent.length, ids, classes (count de .agent, .walk/.work, texto de plaquinha, relógio), contagem de erros.
3. browser_vision SÓ para layout/sobreposição. O headless não tem fonte de emoji colorida: emojis viram tofu e o modelo de visão descreve errado (chamou agentes de "badges com letras"). Não julgar renderização de emoji por screenshot.
4. Entregar só com zero erros de JS e movimento confirmado por DOM.

## Publicação no servidor (painel no ar)
- Publicar sempre como rota no Caddy da 443 (domínio do VPS) fazendo proxy pro server.py stdlib em porta alta. IP:porta alta direto NÃO funciona de fora: firewall externo só libera 22/80/443 (14/09: o Rob pegou ERR_CONNECTION_TIMED_OUT no :8643 que eu tinha "testado").
- Prova de acesso externo: check-host.net na URL pública (200 de vários países). browser_navigate/curl do Hermes rodam LOCAL: sucesso local não vale como teste externo.
- Rota no Caddy SEM sudo: POST /load na admin API 127.0.0.1:2019 (vale até o Caddy reiniciar; backup /tmp/caddy-backup.json antes). Morre no reboot: restart manual.
- Embed de app interno que bloqueia iframe (x-frame-options DENY) e usa chave na URL: proxy no próprio server.py, omitir o header, injetar a chave no HTML no servidor. Detalhes em references/publicacao-servidor.md.
- Caddyfile em /etc/caddy é enganoso; a config efetiva está na API admin http://127.0.0.1:2019/config/.

## Entrega
- HTML autossuficiente (zero dependências externas): entregar com MEDIA:/caminho na mensagem, o Rob abre no navegador do celular/PC. Se o Rob quiser link online, publicar no servidor (ver seção acima).
- Dados de status embutidos devem ser re-verificados na hora (cronjob action=list, TAREFAS.md) antes de gerar; nunca embutir status inventado.

## Pitfalls
- Patch em innerHTML por replace: conferir que nenhum token vizinho foi perdido junto (14/09: remover a tag de nome levou o emoji do agente embora).
- Plaquinha de status só atualiza se tiver id="st-<id>" correspondente ao agente no array JS.
- Estilo do Rob vale aqui também: PT-BR, zero travessões, mensagens curtas.

## Referências
- Painel do escritório (estrutura, como estender, dados embutidos): references/painel-escritorio.md
- Publicação no servidor + embed do dash do CMO (topologia, proxy, chave): references/publicacao-servidor.md
