import asyncio, json
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

TOKEN = json.load(open('/home/hermes/.hermes/profiles/cuidar/mcp-tokens/apify.json'))['access_token']
URL = 'https://mcp.apify.com/'

async def main():
    async with streamablehttp_client(URL, headers={'Authorization': f'Bearer {TOKEN}'},
                                     timeout=timedelta(seconds=120)) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print('N_TOOLS:', len(tools.tools))
            for t in tools.tools:
                if t.name in ('search-actors', 'call-actor', 'get-dataset-items', 'get-actor-run'):
                    print('=== TOOL:', t.name)
                    print(json.dumps(t.inputSchema, ensure_ascii=False)[:1200])

asyncio.run(main())
