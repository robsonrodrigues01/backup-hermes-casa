import asyncio, json
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

TOKEN = json.load(open('/home/hermes/.hermes/profiles/cuidar/mcp-tokens/apify.json'))['access_token']
URL = 'https://mcp.apify.com/'
WANT = 'apify/instagram-profile-scraper'

def text_of(res):
    return '\n'.join(getattr(c, 'text', '') for c in (res.content or []))

def payload(res):
    sc = getattr(res, 'structuredContent', None)
    if isinstance(sc, (dict, list)):
        return sc
    txt = text_of(res)
    try:
        return json.loads(txt)
    except Exception:
        for i, ch in enumerate(txt):
            if ch in '{[':
                try:
                    return json.loads(txt[i:])
                except Exception:
                    continue
    return txt

def extract_dataset(d):
    if not isinstance(d, dict):
        return None, None
    ds = (d.get('storages') or {}).get('datasets') or {}
    default = ds.get('default') or {}
    return default.get('id'), default.get('itemCount')

async def main():
    async with streamablehttp_client(URL, headers={'Authorization': f'Bearer {TOKEN}'},
                                     timeout=timedelta(seconds=280)) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()

            res = await s.call_tool('call-actor', {
                'actor': WANT,
                'input': {'usernames': ['cuidadoresdovalejc'],
                          'resultsType': 'posts', 'resultsLimit': 6},
                'waitSecs': 45})
            print('isError:', res.isError)
            d2 = payload(res)
            status = d2.get('status') if isinstance(d2, dict) else None
            run_id = d2.get('runId') if isinstance(d2, dict) else None
            dataset_id, item_count = extract_dataset(d2)
            print('run:', {'status': status, 'runId': run_id,
                           'datasetId': dataset_id, 'itemCount': item_count})
            if status != 'SUCCEEDED':
                for attempt in range(4):
                    d3 = payload(await s.call_tool('get-actor-run', {'runId': run_id, 'waitSecs': 45}))
                    status = d3.get('status') if isinstance(d3, dict) else None
                    dataset_id, item_count = extract_dataset(d3) or (dataset_id, item_count)
                    print(f'wait{attempt+1}: status={status}')
                    if status in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
                        break

            items = []
            if dataset_id:
                d4 = payload(await s.call_tool('get-dataset-items',
                            {'datasetId': dataset_id, 'limit': 20, 'clean': True}))
                if isinstance(d4, list):
                    items = d4
                else:
                    print('dataset raw:', str(d4)[:300].replace('\n', ' | '))
            print('N_POSTS:', len(items))
            if items:
                p = items[0]
                print('FIRST keys:', list(p.keys())[:18])
                print('FIRST type:', p.get('type'))
                print('FIRST date:', p.get('timestamp'))
                cap = str(p.get('caption') or '').replace('\n', ' ')
                print('FIRST caption120:', cap[:120])
                types = {}
                for it in items:
                    types[str(it.get('type', '?'))] = types.get(str(it.get('type', '?')), 0) + 1
                print('TYPES:', types)
                print('ERRORS:', sum(1 for it in items if it.get('errorDetails')))

asyncio.run(main())
