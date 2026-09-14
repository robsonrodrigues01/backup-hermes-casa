# Catálogo de layouts de post cuidar.vc (10 formatos, board 11/09)

Status FINAL (veredito do Rob, 11/09): repertório oficial = **1, 2, 3, 5, 6, 8, 10**. O board 1 (`artes/template-board.png`, grid 5x2) gerou os aprovados 1/3/5/6/10; o redo glass (`template_board_redo.py`, board `artes/template-board-redo.png`, cards em `artes/redo/layout-{2,8}.png`) aprovou o 2 meio a meio glass (Canva `DAHU6Ta4n6Q`) e o 8 checklist glass (Canva `DAHU6bvyEsQ`). Reprovados 2x, enterrados: 4, 7, 9. Board 2 (11–22) congelado até veredito. Coração em arte: SEMPRE via `squad/heart.py` (v2, sem aro escuro).

Fotos: reutilizar o acervo em cache antes de gerar novas no z-image-turbo (acervo 11/09: apresentação, cards 1–6 do carrossel, babá com bebê, enfermeira com idoso).

## Os 10 layouts

1. **Padrão atual**: foto cover em tela cheia + pill azul-escura no topo (#02426e, coração ciano + texto branco bold) + caixa branca arredondada na base com título, parágrafo e logo-1. É o layout do post de lançamento (`compose_post.py`).
2. **Meio a meio**: foto na metade de cima, bloco azul sólido na de baixo com título/texto brancos. Sobre fundo azul: logo BRANCO (regra da marca), sem chip.
3. **Painel lateral**: foto à esquerda (~60% da largura), painel branco arredondado à direita com texto em coluna vertical.
4. **Cartão flutuante**: cartão branco centralizado sobre a foto, coração ciano atravessando o topo do cartão.
5. **Moldura**: foto com margem/moldura sobre fundo branco, título abaixo. Visual clean, bom p/ fotos de estúdio (ex: babá com bebê).
6. **Dado educativo**: número gigante em azul #0ea5e9 (ex: "70%") + frase curta. Gancho estatístico, pilar educação.
7. **Citação**: fundo azul-escuro, aspas grandes, citação branca centralizada, foto circular no meio. Logo branco.
8. **Checklist**: faixa azul de cabeçalho ("Antes de contratar, verifique:") + corpo branco com itens de check (profissionais verificados, pagamento seguro, avaliações reais).
9. **Tipografia sobre foto**: gradiente escuro na base da foto, frase forte branca no centro, linha de apoio em peso 800.
10. **Polaroid**: moldura polaroid inclinada sobre fundo azul-claro, legenda curta embaixo. Tom mais despojado.

## Regras de legibilidade (QC reprovou 2x até chegar nestas)

- Badge/número sempre em canto VAZIO (superior direito da célula), nunca sobre área de texto.
- Linha de apoio sobre foto: peso 800 + sombra. Peso 400 sobre foto reprova no QC.
- Texto branco sobre foto: só com gradiente escuro atrás.
- PIL pitfall: `Image.new(mode, size, color)` são sempre 3 argumentos — `Image.new("RGBA", (W, H), (0, 0, 0, 0))`.

## Receita do board de escolha

1. Inventariar fotos em cache (`ls` dos diretórios de artes) antes de gerar novas.
2. `python3 template_board.py` no repo da squad → `artes/template-board.png`.
3. QC via `vision_analyze` ANTES de entregar: badge cobre texto? linhas sobre foto legíveis? textos cortados?
4. Se reprovar: patch no script, regerar, re-QC.
5. Entrega: `MEDIA:` + lista numerada curta (1 linha por layout). Rob responde os números.

Padrão geral de decisão: opções visuais viram board numerado único, nunca descrição verbal nem N imagens separadas.
