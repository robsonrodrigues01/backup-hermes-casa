# Leonardo Da Vinci — o agente orquestrador da sua empresa

> Distribuição oficial do **Pixel AI Hub** (Trilha 4 — Empresa Agêntica). Este
> repositório instala o **Leonardo** (o Léo): o agente que cuida do cérebro da sua
> empresa — puxa informação entre cérebros, audita todos e cuida do conjunto.

## Você não instala isto na mão

O jeito certo de usar está na **aula 4.1 do Pixel AI Hub**: você cola o
**INSTALADOR-DO-ORQUESTRADOR** (vem no kit da aula) no agente que você já tem, e **ele**
instala o Leonardo pra você — cria o perfil isolado, te guia no bot do Telegram e liga o
gateway. Zero terminal.

Por baixo, o que o seu agente roda é:

```
hermes profile install github.com/okjpg/agente-orquestrador --alias leonardo -y
```

## O que vem aqui

- `SOUL.md` — a identidade do Leonardo (orquestrador da empresa, regras da casa)
- `config.yaml` — a casa dele já apontada pro workspace do cérebro da empresa
- `distribution.yaml` — o manifesto (nome, versão)

O que **não** vem (de propósito): suas memórias, chaves, token de bot e sessões são
**seus** — nascem na sua máquina e **nunca** entram neste repositório. O instalador do
Hermes exclui esses arquivos por design, em qualquer distribution.

## Atualizar o Leonardo (sem perder nada)

Quando a Pixel publicar uma versão nova:

```
hermes profile update leonardo
```

Isso troca a identidade e as skills da distribuição e **preserva as suas memórias,
sessões, chaves e configuração** — testado e provado antes de entrar na aula.

---

*Pixel Educação · Pixel AI Hub — Trilha 4 · v1.0.0*
