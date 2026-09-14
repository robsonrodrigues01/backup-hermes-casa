---
name: brand-assets
description: Cria, avalia e aplica assets de marca (foto de perfil/avatar, logo, arte flat-vector) para o bot e canais da ERA 4.0 — renderização multiconceito com Pillow, revisão visual de candidatos e aplicação de foto de perfil do bot via Telegram Bot API (sem BotFather manual).
---

# brand-assets

## Quando usar
- Trocar/criar foto de perfil, avatar, logo ou arte flat-vector para o bot ou canais da agência.
- Aplicar foto de perfil do bot via Telegram Bot API.

## Fluxo padrão (render → revisar → escolher → aplicar → arquivar)
1. Definir **3 conceitos distintos** (persona/assistente, monograma-logo, mascote) — dá ao usuário grau de escolha real sem pedir para escolher no vazio.
2. Renderizar com Pillow: desenha em 2048×2048 e desce com Lanczos para 1024×1024; gradientes via grid de 512px reescalado; glow = camada RGBA borrada + `alpha_composite` (1–2 passes reforçam o brilho). Copie `templates/generate_avatar_variants.py` para um scratch path, edite os conceitos e rode com venv de Pillow.
3. Legibilidade no próprio gerador: thumbnail 64px + probes de pixel (o gerador já imprime os dois).
4. `vision_analyze` (1 call por candidato): legibilidade em 64px, defeitos de composição, risco de clip no corte circular do Telegram.
5. Escolher com justificativa documentada. Peso: leitura em tamanho pequeno > riqueza de detalhe.
6. Aplicar via API — receita em `references/telegram-setprofilephoto.md`.
7. Arquivar todas as candidatas em `~/.hermes/profiles/era4/assets/c{n}_{slug}.png` e ofertar troca futura em 1 comando.

## Aplicar foto de perfil do bot (resumo da receita)
- Validar token com `getMe` antes de postar.
- Converter o PNG escolhido para **JPG 1024×1024 quality 92**.
- Multipart: campo `photo` = JSON string `{"type":"static","photo":"attach://img"}` + arquivo JPG numa parte `img`.
- Token via `set -a && . ~/.hermes/profiles/era4/.env && set +a` no shell e `os.environ` no python — nunca ecoar o token.

## Pitfalls
- `setMyProfilePhoto` rejeita PNG e file_id ("photo isn't specified" / "can't parse photo JSON object") — só multipart `attach://` + **JPG**.
- Corte circular do Telegram: mãos/detalhes perto dos cantos do quadro podem ser clipados; sujeito central, cabeça ocupando 70–80% do quadro para avatar (não os 55% que funcionam para post).
- Subagentes (delegate_task) rodam com terminal isolado: arquivos gerados lá não persistem no /tmp do agente pai — renderizar no terminal da sessão principal.
- Instalações de pacotes podem bloquear esperando aprovação manual (approvals.mode=manual): se bloquear, peça destravamento ao usuário com uma pergunta clara (clarify) e espere; não tente contornar.
- O python do sistema pode não ter Pillow e o venv do hermes-agent tampouco — isso é estado do ambiente, não quebra; o remédio é venv descartável: `uv venv /tmp/pxv && uv pip install --python /tmp/pxv/bin/python pillow`.

## Arquivos de apoio
- `references/telegram-setprofilephoto.md` — receita exata validada + tabela erro→causa da sessão de debugging.
- `templates/generate_avatar_variants.py` — gerador multiconceito conhecido-bom (copie e edite; não rode sobre assets finais).