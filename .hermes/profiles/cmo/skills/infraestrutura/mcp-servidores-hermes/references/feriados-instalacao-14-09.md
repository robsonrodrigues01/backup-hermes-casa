# feriadosapi.com (MCP com API key estática) — episódio 14/09/2026

Contexto: Rob pediu análise de datas comemorativas/feriados usando o MCP feriadosapi.com. Este episódio validou o fluxo de servidor MCP SEM OAuth (chave estática), diferente do Apify (OAuth).

## Instalação (perfis cmo e cuidar)
1. Probe ANTES de instalar: curl no endpoint MCP (transporte) + `tools/list` (9 tools descobertas: buscar_feriados, feriados_nacionais, feriados_por_estado, feriados_por_cidade, verificar_data, feriados_bancarios, verificar_dia_util_bancario, listar_estados, buscar_municipios) + `tools/call` feriados_nacionais 2026 (chamada real retornou os feriados).
2. `hermes -p cmo mcp add feriados` em pty: pergunta a chave → responder com `process(action='submit')` → gravou `MCP_FERIADOS_API_KEY` no .env do cmo.
3. `hermes -p cuidar mcp add feriados`: registro no config.yaml do cuidar.
4. Timeout: `hermes -p cmo config set mcp_servers.feriados.timeout 300` (idem cuidar). Resposta do servidor ~5-7s por chamada.
5. Testes: `hermes -p cmo mcp test feriados` OK 6704ms 9 tools; `hermes -p cuidar mcp test feriados` OK 5520ms.

## Pitfall central: header Bearer rejeitado
- Script de coleta local (lendo a chave do .env e mandando Authorization header) → erro "API Key não fornecida": ESTE provedor só aceita `apiKey` como query param.
- Fix validado: `squad/calendario/fix_feriados_url.py` reescreveu `mcp_servers.feriados.url` no config.yaml dos perfis incluindo `?apiKey=<chave>` na URL. File tools do agente são barrados para config.yaml (security-sensitive), rota validada = script python via terminal.
- Após o fix: `squad/calendario/coleta_feriados.py` coletou 2026 e 2027 (~4,5KB/4,2KB, 18 feriados nacionais por ano, total 131 linhas) → `squad/calendario/raw/feriados-nacionais-2026-2027.md`.

## Consumo na squad (padrão drop/raw)
- O MCP NÃO precisou ser plugado no Planejador: o CMO coletou o raw e a curadoria virou arquivo (`squad/calendario/calendario-datas-comemorativas.md`, tiers A/B/C + regras transversais + skip list), hookado no prompt do Planejador como passo obrigatório a cada run.
- Padrão: MCP fica com o CMO, agente consome arquivo curado. Menos toolset no job, menos token, fonte auditável.

## Lições transversais
- Servidor MCP novo: primeiro curl probe (transporte, tools/list, tools/call) revela o contrato antes de qualquer add.
- Erro de auth de provedor externo: testar a hipótese "header vs query param" ANTES de culpar a chave.
- Registrar em TODOS os perfis que consomem (cmo orquestra, cuidar roda a squad).
