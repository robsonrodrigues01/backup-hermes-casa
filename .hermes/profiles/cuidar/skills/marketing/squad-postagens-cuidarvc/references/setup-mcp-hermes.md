# Setup de MCP servers no Hermes (perfil cuidar) — validado 10/09

## Fix de versão (OBRIGATÓRIO antes de conectar server HTTP)
O venv uv do hermes-agent exige **`mcp==1.26.0` exato**. Versões novas renomeiam `streamablehttp_client` → `streamable_http_client` e quebram (`streamable_http not available` / `unexpected keyword argument 'verify'`). Instalar/atualizar:
```bash
uv pip install --python ~/.local/share/uv/tools/hermes-agent/bin/python mcp==1.26.0
```
Checagem rápida: `~/.local/share/uv/tools/hermes-agent/bin/python -c "from hermes_client.streamable_http import streamablehttp_client"` — se o import falhar, a versão está errada. Fonte da verdade: `importlib.metadata.requires('hermes-agent')` mostra o pin exato.

## `hermes mcp add <nome> --url <url>` — pegadinhas do fluxo interativo
- Prompts em ordem: **[Overwrite? y/N se já existe]** → **[Does this server require authentication? Y/n]** → **[API key / Bearer token]** (SÓ SE `MCP_<NOME>_API_KEY` NÃO existir no .env) → probe de conexão → **[Enable all tools? Y/n/select]** → **[Save config anyway? y/N se o probe falhou]**.
- Se o probe falhar (401 etc.), o server fica salvo **disabled**; ao reconectar com sucesso ele habilita e **descobre as ferramentas** (krea-ai: 34 tools).
- ⚠️ Piped stdin (`printf 'y\n...'`) é frágil (ordem muda quando o server já existe): prefiro ajustar a key primeiro via `save_env_value` e rodar `printf 'y\ny\ny\ny\n' | hermes mcp add ...` para cobrir todos os prompts.

## Trocar/gravar API key de MCP (o .env é protegido!)
`.env` e `config.yaml` do perfil **não aceitam patch/write_file direto** (guard de credenciais). O caminho oficial:
```python
# via ~/.local/share/uv/tools/hermes-agent/bin/python
from hermes_cli.config import save_env_value, get_env_value
save_env_value('MCP_KREA_AI_API_KEY', '<valor>')   # escreve no .env do perfil ATIVO (respeita HERMES_PROFILE)
v = get_env_value('MCP_KREA_AI_API_KEY')           # read-back p/ conferir (len + prefix)
```

## Aplicar mudanças de config/MCP (restart do gateway SEM perder a resposta)
Unidades systemd do Hermes são **user-level** (`systemctl --user`, NÃO system). Restart que derruba a própria sessão → agendar timer transitório que dispara DEPOIS de a resposta ser entregue (~25s):
```bash
systemd-run --user --on-active=25s --unit=<nome-timer> systemctl --user restart hermes-gateway-cuidar.service
```
Confirmar depois: `systemctl --user status hermes-gateway-cuidar` (Active since novo). Serviços: nunca usar sudo/system-level restart (falha e parece que derrubou algo — não derruba).

## Servers conectados no perfil cuidar (10/09)
- **krea-ai**: `https://api.krea.ai/mcp`, 34 ferramentas habilitadas, key em `MCP_KREA_AI_API_KEY` no .env. Notas de uso (modelos, 402, aspas simples no prompt) em `references/krea-mcp-notas.md`.
- **Canva**: NÃO é MCP — integração REST OAuth própria; ver `references/canva-connect-notas.md`.
