import asyncio, json, urllib.request
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

TOKEN = json.load(open('/home/hermes/.hermes/profiles/cuidar/mcp-tokens/apify.json'))['access_token']
URL = 'https://mcp.apify.com/'

def text_of(res):
    return '\n'.join(getattr(c, 'text', '') for c in (res.content or []))

# 1) Instagram public page check
req = urllib.request.Request('https://www.instagram.com/cuidadoresdovalejc/',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'})
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read(40000).decode('utf-8', 'ignore')
        print('IG status:', resp.status)
        import re
        m = re.search(r'<meta property="og:title" content="([^"]*)"', body)
        print('IG og:title:', m.group(1) if m else '(none)')
        print('IG notfound marker:', 'Page Not Found' in body)
except Exception as e:
    print('IG check error:', repr(e)[:200])

# 2) items do run 1 (details mode) - dataset BTQa3HfLebvkbteke
async def main():
    async with streamablehttp_client(URL, headers={'Authorization': f'Bearer {TOKEN}'},
                                     timeout=timedelta(seconds=120)) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool('get-dataset-items', {'datasetId': 'BTQa3HfLebvkbteke', 'limit': 5, 'clean': True})
            print('RUN1 dataset items:')
            print(text_of(res)[:500].replace('\n', ' | '))

asyncio.run(main())
