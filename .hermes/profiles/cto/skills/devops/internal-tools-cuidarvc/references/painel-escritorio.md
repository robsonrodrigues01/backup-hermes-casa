# Painel do escritório virtual (painel-escritorio.html)

Criado 14/09/2026 a pedido do Rob ("painel estilo escritório, agentes andando, cada um com sua mesinha"). HTML único autossuficiente. Mestre: /home/hermes/cuidarvc/painel-escritorio.html; servido pelo server.py em /home/hermes/painel-web/ (rota /painel, ver references/publicacao-servidor.md).

## Regra de elenco (Rob, 15/09)
SÓ quem trabalha no cuidar.vc: Rob 👑, CTO 🤖, CMO 📣, Dev 👨‍💻, QA 🕵️, DevOps 🚀, Claudete 📝, Planejador 📋, Copy ✍️, Artes 🎨, QC 🧐, Agendador 📅, Métricas 📈 (13 agentes). Claudinho (agente pessoal do Rob) não aparece; papel técnico chama-se "CTO". Rob reprovou a v1 como "muito feia": capricho visual é requisito.

## Layout v2 (15/09, reformulação)
- Office 1140x660, parede com faixa (.wallband), janela com sol e nuvens animadas, piso de madeira clara com réguas verticais, vinheta radial.
- Zonas rotuladas (.zlab): squad tech (coluna esquerda, 4 mesas: CTO/Dev/QA/DevOps em x=60, tops 140/260/380/500), marketing·ops (direita: CMO 640,130 e Claudete 640,300), squad conteúdo (mesa longa .desk.long 300,520, 520x80, 6 lugares em x=340..690 passo 70), sala do Rob (vidro topo-direita, .roboffice 292x252, mesa big 876,126).
- Plaquinhas: .plate acima das mesas normais (top:-66px) e .lp ABAIXO da mesa longa (top:calc(100%+6px), width 74px, left 5/75/145/215/285/355px) pra não cobrir os bonecos sentados.
- Cadeiras 24px atrás de cada mesinha; seat do agente = cadeira y-20.
- POIs de caminhada: recepção, café (vapor animado), quadro branco, reunião (tapete oval 330,300), impressora, planta, descanso.

## Motor JS (estável desde v1)
- Array AG: {id, n, e emoji, seat, c cor do corpo, hc cabelo, sk pele, spd, acts frases, info HTML do card}. innerHTML do boneco é template fixo + a.n/a.info autorais: seguro.
- Ciclo: senta (typing) 6-13s, ~60% de chance de andar a um POI (say nos dois trajetos, replyNear responde quem está perto), volta ao seat. Rob: 45% de sair da sala; hora BSB < 07h = dormindo (zzz).
- Plaquinha de status só atualiza com id="st-<id>" correspondente ao AG.
- Relógio BSB por segundo; badge de site: fetch no-cors cuidar.vc vira warn se cair.
- Card popup no canto ao clicar (papel, turno, "Agora:").
- Embed do CMO: section .dashsec com iframe /dash/#hoje via proxy do server.py.

## Como estender
- Novo agente: objeto em AG + mesinha com plaquinha id="st-<id>" (ou .lp na mesa longa, left = seatX-300-35px centralizado).
- Não usar .tag de nome acima da cabeça (redundante, cobre vizinho).
- Mobile: media query escala .office 0.62.
- Regravar o painel com dados de status: re-executar cronjob action=list e reler TAREFAS.md antes; nunca embutir status inventado.

## Histórico
- v2 (15/09): elenco corrigido pra 13 (só cuidar.vc), visual reformulado, 4 fragmentos p1/p1b/p2/p3 + cat. Rob reprovou de novo no celular: office 161% estourava a largura e cortava a coluna esquerda (origem do "muito feio" reportado).
- v3 (15/09, atual): estilo jogo 3D em CSS puro. Arquitetura: .viewport (perspective 1500px) > .world#office (rotateX 56deg via --tilt, preserve-3d) > piso, .box cuboides (btop/bsn/bss/bse/bsw, altura --h, faces com rotateX/rotateY ±90 origin edges) e .bb billboards (translateX(-50%) translateZ(--z) rotateX(calc(-1*var(--tilt))) = sempre de frente pra câmera: placas, monitores, props e bonecos .agent>.bill). Paredes: .walln origin top rotateX(90), .walle origin right rotateY(-90), vidro do Rob .glassn/.glasse translúcido. Responsivo: JS fit() escala .scenebox pra caber na largura (sem clip) + botão 🔍 ampliar vira pan horizontal (fitwrap.zoomed). QA por DOM medindo getBoundingClientRect (só .st com scrollWidth>clientWidth conta como truncado; browser_vision alucina textos pequenos, usar só pra layout geral). Placas da mesa longa viraram cartões fixos .lp 70px (plate() ignora .lp: status vivo só no balão). Ajustes que validaram: lp overlap 0, trunc [], 13 agentes, 0 erros, /painel 200 externo 32812 bytes, check-host 2/3 nós ok + Rob carregou do Brasil.
- Pitfalls v3: sinais das rotações: billboard SEMPRE rotateX(calc(-1*var(--tilt))) e translateX(-50%) ANTES do translateZ; .lp não pode passar de 70px de largura (ancoras a cada 70px); texto do cartão .lp ≤ 12 chars.
- v4 (15/09): PRIMEIRO artefato interno codado 100% pelo Opus 5 (claude -p), conforme a regra do Rob de Opus codar tudo. Estilo game isométrico realista copiado da imagem de referência enviada pelo Rob (cp da imagem pro workdir e pedir pra ler com Read): madeira, tijolo, neon CUIDAR.VC, plantas, rack. Arquivo /home/hermes/painel-web/escritorio-v4.html (59KB), copiado pra index.html pra publicar (backup backup-v3-index.html). Fluxo: prompt em prompt-v4.txt pedindo ler a imagem com Read + reusar o motor do index antigo; 2 fix passes depois (iframe src e link tela cheia de /dash-proxy/ pra /dash/#hoje, porque o server.py só roteia /dash*; neon "que" → "quem"). QA: 13 agentes, 13 plaquinhas, trunc 0, overlap 0, 0 erros JS, iframe com dados vivos no /painel, check-host 3/3 nós 200.
- Disciplina de tuning visual (15/09): usar scripts/qa-painel.js (critério de verde definido UMA vez) e PARAR no primeiro verde. Nesta session o .lp width oscilou 68↔70 por ~40 ciclos patch→navigate→console com o estado já verde, queimando contexto até a compactação. Verde que repete ao re-rodar é verde: publique. Generalização: nunca repetir ação idêntica após falha sem mudar nada na abordagem.
- v5 (15/09, em curso): Rob aprovou o v4 ("o escritório ficou bom") e pediu 4 coisas: bonecos mais realistas; clicar num agente abre conversa (modal de chat com IA local no próprio arquivo, sem chave externa); layout/disposição do painel do CMO melhorados; e fix do "rodar agora" (clique executava no server, mas sem confirmação visível: elemento de status fora da viewport, ver regra 5 em Verificação de UI no SKILL.md). Dois jobs Opus em background no workdir painel-web, sequenciados: prompt-v5.txt → escritorio-v5.html (nunca sobrescrever o index no ar) e prompt-fix-rodar.txt → dashboard-novo.py (o app do dash CMO na 8800, topologia em publicacao-servidor.md). RESULTADO: os dois publicados no mesmo dia. v5 (100KB) no ar em /painel com chat aberto por toque no boneco (modal .chat, IA local com personalidade por papel, bolhas "digitando", resposta em ~1-2s), painel do CMO em card de vidro com badge "ao vivo", 3/3 nós check-host. Fix do rodar: botão agora mostra "disparado: agente indo" / "falhou, tente de novo" (texto volta a "rodar agora" no próximo carrega(), sem timer extra). QA do chat/usou regras 7 e 8 da Verificação de UI (classe .open em vez de offsetParent; requestSubmit em vez de Event sintético).