"""Run one current Mastery retry and submit statically derived answers."""
import asyncio
import hashlib
import json
from pathlib import Path
import sys
import httpx
sys.path.insert(0, str(Path(__file__).parent.parent))
from gm import GameMasterClient
import solve

CID = 'binary-reverse-engineering-day-06-java-bytecode-loader/mastery'
DIR = Path(__file__).parent


async def main():
    gm = GameMasterClient()
    async with httpx.AsyncClient(http2=True, timeout=20,
                                 headers={'Authorization': 'Bearer ' + gm.token}) as client:
        r = await client.post(gm.base_url, json={'op': 'practice', 'challenge': CID})
        r.raise_for_status()
        state = r.json()
        print('attempt', state['attempt_id'], 'deadline', state['deadline'], flush=True)
        artifacts = state['artifacts']
        responses = await asyncio.gather(*(client.get(gm.base_url.rstrip('/') + x['download']) for x in artifacts))
        payloads = []
        for i, (response, artifact) in enumerate(zip(responses, artifacts), 1):
            response.raise_for_status()
            blob = response.content
            assert hashlib.sha256(blob).hexdigest() == artifact['sha256']
            payloads.append(blob)
        answer_ids = state['answer_ids']
        solve.QUESTION_IDS.update(x.split('.', 1)[1] for x in answer_ids)
        answers = {}
        for i, blob in enumerate(payloads, 1):
            answers.update({f'set{i}.{k}': v for k, v in solve.solve(blob).items()})
        assert set(answers) == set(answer_ids), (set(answer_ids) - set(answers), set(answers) - set(answer_ids))
        response = await client.post(gm.base_url, json={'op': 'submit', 'challenge': CID, 'answers': answers})
        response.raise_for_status()
        result = response.json()
        print('result', result.get('result'), 'remaining', result.get('remaining'), flush=True)
        for i, blob in enumerate(payloads, 1):
            (DIR / f'mastery_set{i}_evidence.zip').write_bytes(blob)
        (DIR / 'mastery_answers.json').write_text(json.dumps(answers, indent=2))
        (DIR / 'mastery_result.json').write_text(json.dumps({k:v for k,v in result.items()
                                                     if k not in ('questions','prompt','guidance')}, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
