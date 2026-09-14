# Framework de métricas: análise, crescimento e plano de ação (Agente 6 Métricas)

> Destilado em PT-BR do repo blacktwist/social-media-skills (MIT, mai/2026), adaptado ao cuidar.vc: dados via **Zernio** (`/v1/analytics`, `/v1/accounts/follower-stats`, `/v1/analytics/instagram/follower-history`, `/v1/analytics/content-decay`, `/v1/analytics/best-time`; filtrar por accountId). Carregue este arquivo antes de montar o relatório.

## Princípios fixos
- **Comparar TAXA, nunca número bruto**: ER = (curtidas + comentários + compartilhamentos + salvamentos) / impressões × 100. 50 likes em 500 views (10%) ganha de 200 likes em 10.000 (2%).
- **Benchmark = nossa própria média**, nunca "média do setor". Post top ou ruim é relativo ao nosso baseline do período.
- **Conta nova, sinal fraco**: com poucos posts/dados (best-time vazio, follower-history curto), REPORTAR o estado com nível de confiança (alto/médio/baixo). Nunca inventar número nem disfarçar vazio.
- **Post apagado pelo Rob sai da análise** (ex: carrossel antigo apagado 11/09).
- **Output ENXUTO**: o CMO recebe o output inteiro via `context_from` (injeção de contexto). Relatório = no máx. ~25 linhas; detalhe longo vai em arquivo no workspace (`metricas/`) e o relatório só cita o caminho.

## Análise de performance (janela: últimos 30 dias ou 20 posts)
1. **Baseline**: ER médio, impressões médias por post, comentários médios. Separar por rede (IG e FB têm alcances diferentes).
2. **Top 3–5 por ER**, com diagnóstico em 5 dimensões: tema/pilar (família vs cuidador), formato (foto/carrossel/Reels/story), gancho (qual dos 9 padrões de `copy-ig-fb.md`), horário, CTA usado.
3. **Piores 3–5 por ER**, mesma diagnose: gancho genérico? tema errado? horário ruim? formato desalinhado? tom promocional demais?
4. **Tendências**: ER subindo/caindo/estável? impressões? frequência corrê com performance? algum formato vencendo consistente?
- Diagnóstico específico, não genérico: "ER 8,4%, 3x nossa média; gancho de empatia + pilar família + terça de manhã" vale mais que "performou bem".
- Mínimo de 5 posts pra analisar performance, 10 pra padrão. Menos que isso: só baseline + confiança baixa.

## Padrões (quando acumular 10+ posts)
Média de ER por categoria, ranqueada: **pilar** (qual dos 4 pilares editoriais), **formato**, **horário/dia** (achar janelas e zonas mortas), **comprimento da legenda**, **tipo de gancho** (dos 9), **tom** (educativo tende a salvamentos; pessoal/emocional tende a comentários), **rede** (IG vs FB pro MESMO post: onde está o retorno por post?). Atenção ao viés de recência: post de ontem ainda acumula engajamento, sinalizar quando afetar a leitura.

## Crescimento de seguidores
- **Líquido por período** (fim menos início), **taxa** = ganhos / inicial × 100, e tendência (acelerando, freando, estável).
- **Picos** (dia com 2x+ a média): qual post saiu antes? salvamentos e compartilhamentos (descoberta) ou conversa (comunidade)?
- **Engajamento ≠ seguidores**: engajamento = ressonância com quem já segue; follow = descoberta e 1ª impressão. Post com muitos likes e poucos follows = entretenimento da audiência atual; post que traz follows = construtor de autoridade. Identificar qual conteúdo cai em cada caixa.
- **Estagnação**: frequência caiu? formato mudou? spike de unfollow (conteúdo decepcionou)? reportar como diagnóstico, não falha.
- **Projeção**: manter ritmo atual, quando chegamos na próxima marca redonda de seguidores (usar content-decay p/ contexto: ~78% do engajamento ocorre nas primeiras 24h).

## Plano de ação (fecha TODO relatório): 4 níveis, nessa ordem
1. **Wins rápidos** (menos de 1h, efeito imediato): ajuste de execução citando DADO específico ("seus 3 tops abrem com gancho de lista; use nas próximas 5 legendas").
2. **Mudanças estratégicas** (2–4 semanas p/ medir): mexer no mix de pilares/formatos/cadência, explicando o trade-off.
3. **Experimentos**: hipótese + teste (quantos posts, quantas semanas) + critério de sucesso E de fracasso ("se ER < 1,5x baseline em 3 tentativas, dropa").
4. **Parar de fazer** (corte com evidência, nunca opinião: "post promocional sem valor antes da oferta = 0,9% ER vs 4,3% com gancho de insight").
- Máx. 5 ações por relatório, ranqueadas por impacto esperado. Cada uma: o que fazer, por quê (dado), como medir.

## Alimentação do resto da squad (chaining)
- Gancho vencedor e horário forte → Copywriter e Agendador usam no próximo ciclo (o CMO replica no briefing).
- Padrão de ER por formato → Planejador ajusta o mix semanal.
- Teste A/B de gancho (mesmo corpo, 1ª linha diferente, 2–3 semanas de intervalo): Métricas declara o vencedor por ER.
