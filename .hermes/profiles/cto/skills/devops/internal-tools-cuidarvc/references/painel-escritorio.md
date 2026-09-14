# Painel do escritório virtual (painel-escritorio.html)

Criado 14/09/2026 a pedido do Rob ("painel estilo escritório, agentes andando, cada um com sua mesinha"). Arquivo: /home/hermes/cuidarvc/painel-escritorio.html, HTML único autossuficiente, ~12KB.

## Estrutura
- Header: título, badge de site ao vivo (fetch no-cors para https://cuidar.vc, vira warn se sem resposta), relógio America/Sao_Paulo tickando por segundo.
- Barra de quadro: contagens reais de TAREFAS.md no momento da geração (backlog, em progresso, revisão, pronto) + "Coder: Claude Opus 5".
- .office: piso com grade CSS, POIs (recepção, café, quadro branco, impressora, planta, reunião, descanso) e a sala do chefe no canto superior direito (faixa hachurada + vidro).
- 10 agentes no array AG: {id, n nome, e emoji, seat [x,y] fixo da mesinha, acts frases de status, info HTML do cartão}. CTO 🤖, Dev 👨‍💻, QA 🕵️, DevOps 🚀, CMO 📣, Claudete 📝, Planejador 📋, Artes 🎨, Agendador 📅, Rob 👑.
- Mesa = div .desk com monitor emoji e plaquinha (.plate) com nome em <b> e status em .st com id="st-<id>".
- Ciclo JS por agente: trabalha 6-13s (frase de acts vai pro balãozinho .bub e pra plaquinha), 62% de chance de levantar, ir a um POI (transition left/top + classe .walk com bounce), esperar 2-5s, voltar ao seat. Rob: 50% de chance de sair da sala e, se hora BSB < 07h, fica "😴 dormindo".
- Clique no agente abre card fixo no canto (papel, turno, último resultado real, "Agora: <atividade>").

## Dados reais embutidos (14/09)
- Turnos: Dev 09h00 BSB (12h UTC), QA 15h00 (18h UTC), DevOps 17h00 (20h UTC), status CTO 07h15. Últimos turnos 14/09: todos ok.
- Backlog vazio na geração. Se emendar o painel, re-executar cronjob action=list e reler TAREFAS.md antes.

## Como estender
- Novo agente: objeto novo em AG + div .desk com plaquinha id="st-<id>". Seat y = topo da mesa - 22px para o boneco "sentar" na borda. Plaquinha em top:-66px fica acima do boneco sem cobrir.
- Não usar .tag de nome acima da cabeça: redundante com a plaquinha e cobre o vizinho (removido 14/09).
- Mobile: media query escala .office 0.62.

## Verificação real executada em 14/09
- browser_console: 10 agentes, 3 em .walk, 7 em .work, relógio "19:56 BSB", plaquinha Rob "tomando café", 0 erros.
- browser_vision (2ª rodada, após correções): "plaquinhas acima das mesas, não cobrem os agentes; sala do chefe legível".
- Entregue via MEDIA: na DM. Rob pediu link online e o painel foi publicado no mesmo dia: http://66.42.78.129:8643/ com o dash de postagens do CMO embutido como seção "📣 Posts do CMO" (iframe /dash/#hoje via proxy). Detalhes do servidor e do embed: references/publicacao-servidor.md.
