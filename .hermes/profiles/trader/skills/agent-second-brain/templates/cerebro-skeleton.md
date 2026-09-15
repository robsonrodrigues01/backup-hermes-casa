# Cerebro Skeleton — starter files to copy with modifications

Three files to create inside `~/.hermes/profiles/<name>/brain/`. Replace
<PLACEHOLDERS>. Keep it plain markdown; no secrets (names of where things
live, never values).

## File 1: 00-CEREBRO.md

```markdown
# Cérebro <NOME> — manual de operação

Regra única: **nada importante morre fora daqui.** Se não está nos arquivos
desta pasta, não aconteceu.

- Fim de cada dia → bloco em `diario.md` (3-5 linhas: o que fizemos, o que
  decidiu, o que ficou aberto).
- Decisão nova (fornecedor, preço, processo, promessa pra cliente) → arquivo
  em `decisoes/<data>-<tema>.md`.
- Progresso de cliente/projeto → arquivo da pasta correspondente.
- Arquivo avulso sem destino ainda → `dropbox/`.
- `snapshot/` = cópia dos arquivos de serviço; atualizar quando eles mudarem.

Este cérebro é espelhado no GitHub (repo privado). Nada de senhas/tokens
aqui — nunca.
```

## File 2: 00-RAIO-X.md

```markdown
# Raio-X — marco zero (<AAAA-MM-DD>)

Fotografia de tudo que já existia quando o cérebro nasceu.

## Casa
- Agente: <perfil/bot, no ar desde quando>
- Gateway: <unidade systemd>, <status>
- Cérebro espelhado: <repo privado / ainda local>
- Memórias fortes: <3-4 bullets: o que o agente já "sabe de cor">

## Operação
- <domínio>: <arquivos que já existiam — leads, pipeline, contratos, com destaques>
- Pautas em curso: <o que estava em andamento>
```

## File 3: diario.md (first block template)

```markdown
# Diário

## <AAAA-MM-DD>
- **Fizemos:** ...
- **Decidimos:** ...
- **Ficou aberto:** ...
- **Próximo marco:** ...
```
