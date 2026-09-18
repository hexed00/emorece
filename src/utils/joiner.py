import aiohttp
import asyncio

async def join_server(token, invite_code):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://discord.com/api/v10/invites/{invite_code}',
                headers={'Authorization': token, 'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as r:
                if r.status in [200, 201]:
                    return {'success': True, 'status': r.status}
                else:
                    data = await r.json() if r.content_type == 'application/json' else {}
                    return {'success': False, 'status': r.status, 'message': data.get('message', 'Unknown error')}
    except asyncio.TimeoutError:
        return {'success': False, 'status': 0, 'message': 'Timeout'}
    except Exception as e:
        return {'success': False, 'status': 0, 'message': str(e)}

async def mass_join(tokens, invite_code, limit=None, delay_ms=800, max_concurrent=5):
    if limit:
        tokens = tokens[:limit]
    
    joined = 0
    failed = 0
    
    delay = delay_ms / 1000
    
    for i in range(0, len(tokens), max_concurrent):
        batch = tokens[i:i + max_concurrent]
        results = await asyncio.gather(*[join_server(token, invite_code) for token in batch])
        
        for result in results:
            if result['success']:
                joined += 1
            else:
                failed += 1
        
        if i + max_concurrent < len(tokens):
            await asyncio.sleep(delay)
    
    return {'joined': joined, 'failed': failed, 'total': len(tokens)}
