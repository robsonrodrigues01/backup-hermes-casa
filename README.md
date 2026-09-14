# Cofre da Casa Hermes

Backup do **nosso Hermes** — perfis, agentes, subagentes, skills, memórias, cron e configs — nada de outros repositórios.

## O que tem dentro
- `.hermes/` completa do `default` + perfis **cuidar, era4, lab, cmo, cto** (agents, subagents, skills, memories, cron, PENDENTES.md, MAPA.md, SOUL)
- `scripts/`, `tools/` (código próprio de casa), configs de casa (`.bashrc`, headroom, etc.)

## O que NÃO tem (e por quê)
- **Tokens / .env / secrets** — segredo não vai pro git (Rob: "tokens de fora")
- **Logs de conversa (state.db)** — pesados (113MB+); vão no zip mensal (Release dia 1)
- **Plugins de terceiros** (gbrain, postiz, agent-vision) — reinstaláveis, são "outros repositórios"
- **Binários** (tirith 38MB×5, lsp) e node_modules/caches — reinstaláveis

## Como restaurar a casa (máquina nova)
```bash
git clone https://github.com/robsoncoffy/backup-hermes-casa.git /home/hermes
# baixar o zip completo do último Release (tem os logs de conversa) e extrair por cima
# reinstalar dependências:
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash   # hermes
bun install -g github:garrytan/gbrain                                # plugin gbrain
git clone https://github.com/imhechul/postiz-app .hermes/plugins/postiz-app  # postiz
```
Tokens voltam do cofre de senhas / telemetria do Rob (não estão aqui).

## Rotina automática
- **Todos os dias 17h (Brasília)**: git push do que mudou
- **Dia 1 de cada mês**: zip completo da casa (com logs) anexado no Release `cofre-YYYY-MM`

## Recompensa em 3 passos (se algo quebrar)
1. `git clone` este repo em `/home/hermes`
2. Extrair o zip do último Release por cima
3. Rodar `hermes gateway start` em cada perfil
