# z-image-turbo (servidor Vultr do Rob) — fonte principal de arte (10/09)

**Grátis, sem créditos, ~15s/geração.** Descoberta e validada em 10/09 como fonte principal do Agente 3 (Artes). Krea AI = opção premium para artes especiais; Piapi = backup pendente.

## Endpoint
- `POST http://127.0.0.1:8789/v1/images/generations` (proxy local → servidor de inferência Vultr do Rob)
- Auth: `Authorization: Bearer $KEY` — key está em `providers.vultr.api_key` do `~/.hermes/profiles/cuidar/config.yaml` (não duplicar em outros arquivos)
- Body: `{"model": "z-image-turbo", "prompt": "...", "size": "1024x1024"}`
- Resposta: `{"data": [{"url": "..."}]}` — URL assinada do Vultr Objects, **expira em 1h** → baixar a imagem imediatamente.

## Regras de tamanho (crítico)
- **ACEITA APENAS `1024x1024`.** Tamanhos portrait testados e REJEITADOS com HTTP 422: `1080x1350`, `1024x1280`, `1024x1536`, `832x1216`, `768x1344`.
- Para feed 4:5: gerar 1024x1024 com composição centralizada e margens seguras → depois crop `819x1024` (PIL) OU postar como 1:1 (Instagram aceita nativo).

## Qualidade validada (10/09, card-3 do carrossel de lançamento)
- ✅ Texto em português acentuado impecável ("As referências são reais?", "famílias", "já")
- ✅ Foto realista, warm light, acolhedora; hierarquia visual boa — nota 8,5/10
- ❌ **DEFEITO CONHECIDO: QUALQUER texto no prompt sai errado** (wordmark virou "cuidar-vvc"; headlines podiam virar palavras distorcidas — o Rob corrigiu isso 2x em 10/09: "não consegue colocar o logo que enviei" + "tem palavras erradas"). **NUNCA pedir texto NENHUM no prompt — nem headline, nem subtítulo, nem wordmark, nem números.** A IA gera SÓ a foto. Tipografia e logo são compostos depois via `compose_card.py` (Logo 1 oficial: `/home/hermes/cuidarvc/squad/marca/logo-1-squircle-azul-wordmark-azul.png`).

## Método oficial: `compose_card.py` (validado 9/10 em 10/09)
Script pronto: `/home/hermes/cuidarvc/squad/compose_card.py` — o padrão DO AGENTE 3. Fluxo: gera a foto com prompt de **FOTO PURA** (cena + "absolutely NO text, NO letters, NO numbers, NO words, NO logos, NO watermarks, NO captions anywhere") e compõe o card 1080x1350: foto no topo (1080x1080), gradiente/painel azul #0ea5e9, headline e subtítulo em **Montserrat real** (variable TTF em `marca/fonts/`, `set_variation_by_axes`), **Logo 1 oficial** em chip branco no rodapé, handle `@cuidarvc.br`, indicador `N/total`. Tipografia real = zero erro ortográfico; logo colado = logo idêntico ao oficial.
Uso: `<python-do-venv-hermes> /home/hermes/cuidarvc/squad/compose_card.py <num> <total> '<cena-da-foto>' '<headline>' '<subtitulo>'` (exige Pillow no venv: `uv pip install --python ~/.local/share/uv/tools/hermes-agent/bin/python pillow`).
Saída: foto bruta em `artes/fotos/foto-card-N.png`, card final em `artes/cards/card-N.png`.

### ⚠️ Pegadinha do wrap (Rob pegou letras cortadas, 10/09)
- TODO texto desenhado com PIL deve passar pela função `wrap()` com margem de segurança `W - 180` (90px de cada lado) — headline E subtítulo. O script original só fazia wrap da headline; o subtítulo longo ("Você merece saber exatamente quem entra na sua casa.") saía **cortado na borda direita** — Rob rejeitou ("as letras estão cortadas"). Corrigido: wrap no subtítulo também, headline começa em y=930, line-heights 78 (headline) e 46 (subtítulo) para 2+2 linhas não colidirem com o chip do logo (y≈1202).
- Regra geral ao compor qualquer card: validar com vision QC **checando corte de borda** antes de entregar; subtítulos >55 chars em 36px quebram em 2 linhas — prever espaço.
- Foto em cache: se `artes/fotos/foto-card-N.png` existe, o script reusa (não regenera) — recompor tipografia não gasta geração nova.

## Prompt de card — REPROVADO (método antigo, não usar)
A estrutura antiga (headline PT dentro do prompt + overlay no prompt) dava nota 8,5 e RISCO de erro ortográfico — o Rob rejeitou 2x. Não repetir: o card-3 com compose_card.py (foto pura + tipografia composta) saiu 9/10, ZERO erros.
## Fallback manual: gerar foto bruta (python urllib — nunca curl inline com aspas aninhadas)
```python
import json, urllib.request, pathlib
payload = json.dumps({"model": "z-image-turbo", "prompt": PROMPT, "size": "1024x1024"}).encode()
req = urllib.request.Request("http://127.0.0.1:8789/v1/images/generations", data=payload,
    headers={"Authorization": "Bearer <KEY-DO-CONFIG>", "Content-Type": "application/json"})
resp = json.load(urllib.request.urlopen(req, timeout=120))
img = urllib.request.urlopen(resp["data"][0]["url"], timeout=60).read()
pathlib.Path("card.png").write_bytes(img)
```

## Quando usar cada fonte
| Fonte | Quando | Formato | Custo |
|---|---|---|---|
| **z-image-turbo (Vultr)** | Padrão da squad, posts diários | 1024x1024 | zero |
| Krea `google/nano-banana-2` | Artes especiais, 4:5 nativo | 1080x1350 | créditos (plano pago) |
| Krea `bytedance/seedream-4` | Topo de linha | varios | plano pago |
| Piapi | Backup | — | chave pendente |