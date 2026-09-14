# Análise ad-hoc de perfil concorrente (Radar, modo CMO)

Receita validada em 14/09/2026 com @clicarecuidadores, @famyleapp, @luziane.cuidandodeidosos e no LOTE DUPLO @cuidadoresdovalesjc + @gscuidadoresdeidosos (Rob mandou 2 links numa mensagem só). Fluxo distinto da varredura diária das 10h: o CMO lê os dados direto via Apify MCP na própria sessão e entrega a leitura na hora.

## Quando usar
- O Rob manda link de perfil no chat e pede análise.
- Também serve como primeiro passo quando ele indica perfil novo pro Radar: a análise ad-hoc já verifica o handle E rende a decisão de ativação.

## Coleta via Apify MCP (apify/instagram-scraper)
Duas runs do actor, ambas com `directUrls: ["https://www.instagram.com/<handle>/"]`:
1. Posts: `resultsType: "posts"`, `resultsLimit: 30`. Runtime ~40s.
2. Detalhes: `resultsType: "details"`, `resultsLimit: 1`. Runtime ~10s. Seguidores e total de posts SÓ vêm aqui.

Ler resultados com `mcp_apify_get_dataset_items` (clean=true). Campos úteis dos posts: `caption`, `likesCount`, `commentsCount`, `timestamp`, `type`. Do details: `username`, `followersCount`, `postsCount`, `biography`.
LOTE (2+ perfis numa mensagem): despachar todas as runs de actor num único bloco paralelo (4 chamadas), depois poll dos runs + datasets de details juntos, posts por último com `fields=` estreito. Validado 14/09, economiza minutos.
Custo: 2 runs cabem folgado no crédito grátis (rotação de ~8 perfis/dia).

## Estrutura da entrega (validada 14/09, zero retrabalho do Rob)
1. **Quem é**: nome, praça, seguidores, total de posts, proposta da bio. Classificar por MODELO, não só nicho: plataforma de intermediação (verificação, pagamento centralizado, curadoria = concorrente DIRETO) vs. franquia vs. app vs. autônomo. Só o mesmo modelo compete no nosso quadrado; os demais são só referência de conteúdo.
2. **Saúde do perfil**: cadência (posts/semana, meses vagos), baseline de engajamento (likes e comentários típicos), consistência visual.
3. **O ouro**: o post destaque em MÚLTIPLO da média (Clicare: 66 likes vs. baseline 5-9 = ~7x). Múltiplo alto = formato validado pelo mercado, prioridade máxima de destilação. Dissecar o porquê: gancho, formato, promessa, estrutura do texto.
4. **Mais coisas que valem**: 3-5 táticas transferíveis (depoimentos textuais em série, checklist de contratação, séries marteladas no mesmo tema, CTA de conversa nos comentários).
5. **Fraqueza explorável**: gaps (ex.: 1 reel em 1,5 ano, cadência irregular, visual sem identidade) = nosso espaço.
6. **Decisão**: ativar no Radar ou não + inspiração imediata mapeada em pilar (1-5) + layout oficial, sem copiar texto.

## Padrões confirmados no caso Clicare (14/09)
- Comparativo "extremos + meio do caminho" (autônomo vs. home care vs. intermediação) COM FAIXA de preço e nota de fonte/data no rodapé foi o único post que viralizou do concorrente (7x a média). Valida na prática a regra do Rob: preço aberto converge se for faixa com contexto. Pauta pronta pro Planejador: pilar 1, layout 8 ou 6, faixas nossas + nota de fonte.
- Depoimentos textuais em série (primeira pessoa, história curta, nome no fim) são prova social barata e replicável; não dependem de print de avaliação.
- Ativação no perfis.json é padrão de baixo risco (monitoramento é só leitura): ativar handle verificado, avisar o Rob que sai com uma palavra, registrar em PENDENTES.

## Caso Famyle (14/09): diagnóstico de perfil morto
@famyleapp, marketplace de domésticas/babás por vaga/match, 9.763 seguidores, 357 posts. Os 30 posts do scrape iam de jan a 29/04 e o feed parou: ~5 meses de silêncio. Decisão: `pausado` no perfis.json, NÃO ativo.

**Sinais de morte (checklist de diagnóstico)**:
- Último post meses atrás (comparar max(timestamp) do dataset com a data de hoje).
- Engajamento de fundo de poço: 2-11 likes com 9.763 seguidores (~0,05%); reels com 72-204 views.
- Legendas recicladas literalmente: a MESMA caption repostada meses depois (2 pares encontrados).
- Postagem cravada em horários redondos (12h e 18h BRT): cara de ferramenta de agendamento rodando sozinha.
- Conteúdo 100% corporativo: zero rosto, zero história, zero depoimento, listinha ✔ e CTA de produto.

**REGRA de decisão (nova, 14/09)**: ativar no Radar exige perfil VIVO (postando nos últimos ~2 meses). Perfil morto = `pausado` com motivo + "se voltar a postar, reativa com uma palavra". Cada dia de varredura em perfil morto é custo Apify sem novidade.

**Padrão cross (Clicare + Famyle, 2 casos)**: humanidade performa nos DOIS extremos. Clicare: depoimento textual 7x a média. Famyle: o único post acima da média (11 likes, 8 comentários vs. baseline 2-5) foi o mais curto e humano ("A escolha começa na conversa"). O resto morreu de corporativo repetido. Uso editorial: cita os 2 casos juntos ao defender o pilar 2 (histórias humanas) contra tentação de conteúdo de produto puro.

## Caso Vale SJC (14/09): zumbi + lição de hashtag
@cuidadoresdovalesjc, agência local de home care do Vale do Paraíba, 556 seguidores, 333 posts. Último post 11/08/2025 = 13 meses parado; 0-4 likes, zero comentários. Conteúdo genérico de calendário (Julho Amarelo, Agosto Dourado) com as mesmas 11 hashtags de cidade em TODO post. Decisão: `pausado`.
- É o handle CORRETO do perfil que o Rob indicou antes como "cuidadoresdovalejc": o descarte anterior por "handle inexistente" estava errado, era typo. Handle extraído do link novo do Rob.
- Lição: bloco de hashtag de cidade não constrói audiência; parece spam e não vira alcance local.
- Rede ampla de serviços (idosos, gestantes, crianças, pós-operatório) disputa a mesma família, mas sem jogo de conteúdo = zero ameaça.

## Caso GS Geração de Saúde (14/09): o ouro do nicho
@gscuidadoresdeidosos, agência de home care Curitiba/Florianópolis, **155.328 seguidores com SÓ 91 posts** (audiência de anúncio + viral; segue 2). Posta até hoje, cadência irregular em rajadas. Decisão: `ativo`.
- Reel "conselhos para um casal": **93.444 likes, 1.183 comentários, 820 mil plays** = 60% dos seguidores da Home Angels em likes num post só. Fórmula: idosos reais em vídeo + pergunta emocional na legenda + CTA de compartilhar.
- Outros virais: "Qual é sua maior saudade?" (8.905 likes / 129 mil views), "Qual é a sua história de amor?" (7.965 likes / 57 mil views).
- Máquina de comentários: pergunta direta rende 108-272 comentários ("comente porquê você indica a GS", posts de prêmio com pedido de voto).
- Oferta de entrada: "agende uma experiência gratuita" como CTA permanente da bio.
- Prova social de marca: prêmio TOPVIEW 2x, reportagem TV RPC, eventos p/ idosos (clube, festa julina), semana de capacitação das cuidadoras.
- Métrica -1 em likesCount = likes ocultos pelo perfil (o campo vem -1; tratar como "sem dado", não como número).

## Padrão cross (Clicare + Famyle + Luziane + Vale SJC + GS + Isabella + Fernanda + Nayara + Ivana, 9 casos)
- **Vídeo com gente real é o gap confirmado do nicho**: GS viraliza em massa com idosos reais em vídeo; Luziane tem reel emocional como campeão (2.185 likes); Clicare e Vale SJC não têm vídeo e engajam nada. Argumento definitivo pro roadmap de reels com pessoas reais autorizadas. Enquanto não há vídeo: pergunta emocional no card estático (layout 10).
- **Humanidade performa nos DOIS extremos**: Clicare (depoimento textual 7x a média) e Famyle (post mais humano = único acima da média) vs. corporativo puro morrendo (Famyle, Vale SJC).
- **Comment-bait que é nosso posicionamento**: "na hora de escolher cuidador, o que pesa mais: preço ou confiança?" com resposta = verificação + pagamento seguro. Pauta sugerida ao Planejador.
- **Oferta de entrada**: o "experiência gratuita" da GS sugere equivalente cuidar.vc (ex.: conversa de matchmaking gratuita) = decisão de produto do Rob, anotada como ideia.
- **Automação de horário é neutra; alma é o diferencial**: Famyle agenda em ponto (12h e 18h) e morre; Isabella agenda em ponto (12h50 TODO dia) e puxa 3,6 mil a 172 mil likes com ELA em 100% dos posts. Fecha o caso Famyle: o problema nunca foi o agendamento, foi postar sem alma. Uso editorial: mata o argumento "postar todo dia via ferramenta basta".
- **Funil palavra-chave no comentário, 2 datapoints**: Luziane ("comente QUERO CONHECER" em ~30% dos posts) e Nayara ("comenta FLOR" = 130x a média dela). Funciona melhor com item CONCRETO e visual (material, checklist, guia) do que com cadastro puro. Pauta pro Planejador: lead magnet + palavra-chave na legenda.
- **Legenda-funil FIXA sobre conteúdo variável (Ivana, 5,6 mi de seguidores)**: reel TODO dia às 11h30 com a MESMA legenda ("aula gratuita, link na bio") sobre ganchos variados; de 2.265 a 131.196 likes com a legenda idêntica (1 em ~8 viraliza). Legenda = anúncio fixo, formato = tráfego variável; variação não é fracasso quando o funil captura cada pico. Adotada na estratégia v2 (`squad/estrategia-conteudo.md`).
- **Polaridade Isabella × Fernanda = estratégia numa frase**: tom da Fernanda (premium acolhedor, validado como DNA do cuidar.vc) + mecânica da Isabella (fixado de vendas, cadência, pergunta, reação). O cuidar.vc não escolhe entre os polos.
- **Perfis que ensinam profissionais = canal de suprimento**: Nayara (fisios domiciliares) e SBGG (geriatras) têm audiência = nosso lado da OFERTA. Além de inspiração de formato, são canal futuro de aquisição de profissionais e parcerias.
- **Séries numeradas com gancho** ("comenta PARTE 2") puxam sequência de consumo; conteúdo técnico pede "salva este post" (Nayara, série de músculos).

## Caso Isabella Lacerda (14/09): referência FORA do nicho, aula de mecânica
@isabellalacerda_nutri, "A Nutri Sarcástica", 1.654.404 seguidores, verificada, 1.584 posts. Nutrição/emagrecimento com humor (programa pago GG, menos de R$ 50/mês, parcerias e YouTube). Posta TODO dia às 12h50 e engaja de 3,6 mil a 172 mil likes, com plays de até 1,9 milhão. Decisão: `ativo` como referência de MECÂNICA (nova categoria: fora do nicho, ativa por transferência de estrutura, não de tema).
- **REGRA "mecânica sim, tom NÃO"**: sarcasmo/picheira não é brand-safe pro cuidar.vc (nosso território é confiança e acolhimento); dela ficam os ossos, não a pele.
- **Post fixado de vendas = vitrine permanente** (o único carrossel do feed dela, pinned): lista "Só no GG você tem" + 8 benefícios com emoji + ancoramento de preço ("10x sem juros, menos de R$ 50/mês. A sua saúde vale muito mais do que isso") + CTA pro link da bio. Adaptável: "Só no cuidar.vc você tem: verificação, pagamento seguro, avaliações reais". Pauta sugerida ao Planejador (pilar 1).
- **Legenda-pergunta pedindo relato**: "quero escutar a experiência de vocês nos comentários" = 2.444 comentários. Mecânica barata, aplicável em qualquer nicho.
- **Conteúdo de reação a outro criador** = 131 mil likes (2º post mais engajado). Versão cuidar.vc: reagir a mitos e conselhos ruins de cuidado de idoso.
- **Bio em 3 tempos**: prova social (9 mil alunas) + promessa (sem passar fome) + CTA ("só falta você").

## Caso Fernanda Scheer (14/09): referência adjacente de TOM e pauta
@fernandascheernutri, nutricionista funcional de longevidade, 269.682 seguidores, verificada, 7.180 posts, 20+ anos de carreira, TEDx, Portal Ella (Jornada do Climatério, Protocolo Integra, eventos Confraria Ella em Floripa). Público = mulher 40+/climatério = nossa persona secundária (filha 45+ que cuida dos pais E pensa na própria longevidade). Engajamento FRACO pro tamanho (22 a 3.882 likes, maioria abaixo de 300; taxa ~0,1-0,2%; reels 1,5-22 mil plays).
- **Padrão limpo: carrossel prático + pergunta no final performa 5-10x acima do diário-pessoal.** Campeões: nutrientes pra pele (3.882), "o que você parou de fazer que melhorou sua vida" (1.212), produto coringa (1.219), fibra (1.079). Fundo: "resumo do meu mês", "comecei uma formação", agenda de eventos, recap de festival (22-215). Autoridade de 20 anos não segura conteúdo sem utilidade prática.
- **O que roubar**: o tom (premium acolhedor = valida o DNA de tom do cuidar.vc), CTA de compartilhamento "manda para quem vai se beneficiar", produtos com NOME claro, pauta adjacente de longevidade/climatério pra persona.
- Decisão: `ativo` como referência adjacente (pauta + tom).

## Caso Nayara (14/09): funil palavra-chave viral + canal de suprimento
@nayarasilveira_, fisioterapeuta geriátrica domiciliar em Floripa, 19.633 seguidores, verificada, 368 posts. Dois públicos: atende pacientes (B2C) E ensina fisioterapeutas domiciliares (B2B, materiais no linktree; parceria com @plataformanura). Não é concorrente: ela e a audiência dela = exatamente o perfil de profissional que o cuidar.vc quer na plataforma (canal de aquisição de OFERTA).
- **VIRAL: reel mostrando material comprado pra tempo de reação de idosos + "se quiser o link, é só comentar FLOR" = 26.062 likes, 2.996 comentários, 763 mil plays num perfil de 19 mil seg (~130x a média dela).** Por que voou: item visual e desejável + CTA por palavra no comentário (mesmo funil da Luziane, mas com objeto concreto) + cada comentário empurra alcance pro algoritmo.
- Outros campeões: humor "Eu e mais quem?" (928 likes, 47 com), post pessoal Dia dos Pais (522, 34 com), série técnica de músculos com loop "comenta PARTE 2" (87-158 likes, save-worthy com "salva este post").
- **Transferível já**: "comente CHECKLIST que enviamos o checklist de verificação de cuidador" (lead magnet + funil de comentário), séries numeradas com gancho, cultura "Ib: @" (adaptar trend de outro nicho creditando), conteúdo pros DOIS lados (família + profissional).
- Decisão: `ativo` como referência de funil + canal de suprimento.

## Caso Ivana Jauregui (14/09): a máquina de funil
@ivana__jauregui, especialista em parentalidade, **5.587.005 seguidores**, verificada, 2.592 posts, palestrante em turnê nacional paga (Alma Talks). Fora do nicho; público = mães = adjacente ao lado babás do cuidar.vc. Decisão: `ativo` como referência de MECÂNICA (funil evergreen + máquina de volume).
- **PADRÃO-OURO, legenda-funil FIXA**: reel TODO dia às 11h30 com a MESMA legenda ("preparei uma aula gratuita, o link está na bio") sobre vídeos-gancho variados; oscila de 2.265 a 131.196 likes com a legenda idêntica (1 em ~8 viraliza: 131 mil likes/1,97 mi plays; outro com 3,6 mi plays). Lição central: legenda = anúncio fixo, vídeo = tráfego variável; o funil captura cada pico, então variação não é fracasso. Nenhum post "dá prejuízo", todos alimentam a mesma aula gratuita.
- Bio com promessa de resultado ultra específica em 1 linha ("Aprenda a falar 1 vez e que seu filho te obedeça") + CTA.
- Post fixado evergreen desde 11/2024 com 100.444 likes (vitrine permanente, igual ao fixado de vendas da Isabella).
- Pessoal forte (férias na Itália: 12.321 likes); contraponto: posts de feed divulgando a turnê AFUNDAM (66 a 2.378 likes). Reels é a máquina, feed é vitrine, nunca palco de venda.
- Multi-receita: palestras pagas + funil de aula gratuita (o evento pago vem DEPOIS do funil, não no feed).

## Casos rápidos (14/09)
- **@sbggsc** (SBGG Santa Catarina): referência INSTITUCIONAL (sociedade científica de Geriatria/Gerontologia de SC), 5.415 seg, 1.076 posts; audiência = profissionais de saúde, nosso lado da OFERTA. Fórmula vencedora: trecho REAL de especialista + pergunta reflexiva. Valor: temas técnicos com credibilidade + canal futuro de parceria (lives, congressos). `ativo`.
- **@silpidigital** (SILPI): player adjacente B2B (SaaS de gestão para ILPIs; público administrador de instituição, não família). Veio RESTRICTED da API (sem posts, sem contagem) = monitoramento automático inviável. `pausado`.

## Pitfalls
- `perfis.json` tem escritores múltiplos (sessões do CMO + jobs do workspace disparam warnings de "sibling subagent" no write_file). Relê-lo imediatamente antes de cada escrita e conferir o conteúdo depois; o warning em si não é erro.
- Rodar as DUAS runs do actor: followersCount só vem no details, posts só na outra.
- Número só entra na análise se veio do dataset; senão escrever "sem dado".
- Nunca citar o concorrente analisado em conteúdo público do cuidar.vc; a análise vira insumo interno, o post leva pauta própria.
- Perfil RESTRICTED na API (caso @silpidigital 14/09: erro tipo "You must be 16 years old or over", zero posts e zero contagem) ≠ handle inexistente ≠ perfil morto: é bloqueio de acesso, monitoramento automático inviável. Cadastrar `pausado` com motivo e reativar só se a restrição sumir.
