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

async def main():
    async with streamablehttp_client(URL, headers={'Authorization': f'Bearer {TOKEN}'},
                                     timeout=timedelta(seconds=280)) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()

            res = await s.call_tool('search-actors', {'keywords': 'instagram profile scraper'})
            txt = text_of(res)
            print('STEP1 found:', WANT in txt or 'instagram-profile-scraper' in txt)
            d = payload(res)
            if isinstance(d, list):
                names = [f"{i.get('user',{}).get('username','?')}/{i.get('name','?')}" if isinstance(i.get('user'), dict) else str(i)[:70] for i in d]
                print('STEP1 actors:', names[:8])
            else:
                print('STEP1 raw:', str(d)[:300].replace('\n', ' | '))

            res = await s.call_tool('call-actor', {
                'actor': WANT,
                'input': {'usernames': ['cuidadoresdovalejc'], 'resultsLimit': 6},
                'waitSecs': 45})
            print('STEP2 isError:', res.isError)
            d2 = payload(res)
            items = dataset_id = run_id = status = None
            if isinstance(d2, dict):
                status = d2.get('status'); run_id = d2.get('runId') or (d2.get('run') or {}).get('id')
                dataset_id = d2.get('defaultDatasetId') or d2.get('datasetId') or (d2.get('output', {}) or {}).get('datasetId')
                items = d2.get('items')
            elif isinstance(d2, list):
                items = d2
            print('STEP2:', {'status': status, 'runId': run_id, 'datasetId': dataset_id,
                             'n_items': len(items) if isinstance(items, list) else None})

            if (not isinstance(items, list) or not items):
                print('STEP2 raw:', str(d2)[:500].replace('\n', ' | '))
                if run_id:
                    for attempt in range(4):
                        d3 = payload(await s.call_tool('get-actor-run', {'runId': run_id, 'waitSecs': 45}))
                        if isinstance(d3, dict):
                            status = d3.get('status')
                            dataset_id = d3.get('defaultDatasetId') or dataset_id
                        print(f'STEP2 wait{attempt+1}: status={status}')
                        if status in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
                            break

            if (not isinstance(items, list) or not items) and dataset_id:
                d4 = payload(await s.call_tool('get-dataset-items', {'datasetId': dataset_id, 'limit': 20, 'clean': True}))
                if isinstance(d4, list):
                    items = d4
                else:
                    print('STEP3 raw:', str(d4)[:400].replace('\n', ' | '))

            n = len(items) if isinstance(items, list) else 0
            print('FINAL n_posts:', n)
            if n:
                p = items[0]
                print('FIRST keys:', list(p.keys())[:20])
                print('FIRST type:', p.get('type'))
                print('FIRST date:', p.get('timestamp'))
                cap = str(p.get('caption') or '').replace('\n', ' ')
                print('FIRST caption120:', cap[:120])
                types = {}
                for it in items:
                    t = str(it.get('type', '?'))
                    types[t] = types.get(t, 0) + 1
                print('TYPES:', types)
                errs = [it for it in items if it.get('errorDetails')]
                print('ERRORS:', len(errs))

asyncio.run(main())
