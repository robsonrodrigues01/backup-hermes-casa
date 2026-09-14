#!/usr/bin/env python3
"""Valida um MCP OAuth do profile cto chamando uma tool real, sem esperar a proxima sessao do profile.

Uso (com o python do Hermes, que tem mcp==1.26.0):
  /home/hermes/.local/share/uv/tools/hermes-agent/bin/python scripts/mcp_check.py <server> <tool> [args_json] [url_mcp]

Exemplos:
  ... mcp_check.py lovable list_workspaces
  ... mcp_check.py lovable list_projects '{"workspace_id": "9y0FI1ViVHXaLPBIhiO3"}'

Se o access_token estiver expirado (~8h no Lovable), o servidor responde 401: refazer o fluxo
manual (passos 1 e 2 da skill) ou aguardar o Hermes refrescar numa sessao que ja carrega o MCP.
"""
import json, asyncio, sys
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Absoluto de proposito: Path.home() no terminal tool do profile aponta para <profile>/home e monta caminho duplicado.
TOKENS_DIR = Path("/home/hermes/.hermes/profiles/cto/mcp-tokens")
KNOWN_URLS = {"lovable": "https://mcp.lovable.dev/?src=skill"}

server = sys.argv[1]
tool = sys.argv[2]
args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
url = sys.argv[4] if len(sys.argv) > 4 else KNOWN_URLS[server]

tok = json.loads((TOKENS_DIR / f"{server}.json").read_text())
headers = {"Authorization": f"Bearer {tok['access_token']}"}

async def main():
    async with streamablehttp_client(url, headers=headers) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool(tool, args)
            for c in res.content:
                print(c.text[:2000])

asyncio.run(main())
