# Submódulos (gitlinks) observados na casa — sessão 14/09

Qualquer pasta com `.git` dentro, ao ser adicionada num repo maior, vira um
**gitlink** (mode `160000` em `git ls-files -s`): o git registra só o SHA do
commit apontado. Consequências práticas para o backup no GitHub:

- o CLONE do backup **não contém** os arquivos dessa pasta;
- `git ls-files | wc -l` subnotifica feio (2463 rastreados vs ~24.800
  arquivos reais na casa — cada gitlink colapsa uma árvore inteira em 1
  linha);
- o snapshot REAL deles fica salvo no zip de migração anexo de Release
  (foto completa de 12/09).

## Os 12 gitlinks encontrados em /home/hermes (14/09)
1. .hermes/plugins/gbrain (146MB no disco, ~22MB só de .git pack — clonado)
2. .hermes/plugins/postiz-app (34MB)
3. .hermes/plugins/agent-vision-toolkit (42MB)
4. cuidarvc/repo (35MB)
5. headroom-test/headroom (105MB; 34MB é .git)
6. tools/agent-reach (2.7MB)
7. tools/last30days-skill (59MB)
8. tools/scan-okjpg/agent-context-kit
9. tools/scan-okjpg/agente-orquestrador
10. tools/scan-okjpg/gbrain
11. tools/scan-okjpg/skill-creator
12. tools/scan-okjpg/skills

## Decisão registrada (14/09)
MANTER como gitlink. Razões: (a) o conteúdo deles está no snapshot/zip de
Release com data certa; (b) remover `.git`s internos converteria clones
ativos em árvores congeladas dentro do backup (e bagunça os repos reais);
(c) gbrain/postiz são externos e reinstaláveis via clone quando precisar.

## Como listar os gitlinks de novo (runbook)
```bash
git ls-files -s | grep ^160000 | awk '{print $4}'
```
Se um dia um desses repos MORRER (fora do ar), tirar do backup no próximo
checkpoint: `git rm --cached <caminho>` e seguir sem ele.
