#!/usr/bin/env python3
"""Resume a live Time Trial or retry an expired one, using assigned bytes only."""
import hashlib
import asyncio
import httpx
import json
import os
import subprocess
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from solve_hatch import build, HERE

BASE = 'https://2026.huntress.ctf.games/'
CHALLENGE = 'script-analysis-day-05-python-carrier-lab/time_trial'
HEADERS = {'Authorization': 'Bearer ' + os.environ['HUNTRESS_GM_TOKEN']}

def get(url):
    with urlopen(Request(url, headers=HEADERS), timeout=8) as response:
        return response.read()

def post(data):
    req = Request(BASE, data=json.dumps(data).encode(), headers={**HEADERS, 'Content-Type': 'application/json'})
    with urlopen(req, timeout=8) as response:
        return json.load(response)

def main():
    status = json.loads(get(BASE + '?op=status&challenge=' + CHALLENGE))
    if status.get('result') == 'CORRECT':
        print(json.dumps({'result': 'already_solved', 'attempt': status.get('attempt_id')}))
        return
    current = post({'op': 'retry', 'challenge': CHALLENGE}) if status.get('result') == 'expired' else post({'challenge': CHALLENGE})
    qids = current.get('answer_ids') or [q['id'] for q in current.get('questions', [])]
    attempt = current.get('attempt_id', 'unknown-attempt')
    retained = HERE / 'artifacts/time_trial' / attempt
    retained.mkdir(parents=True, exist_ok=True)
    (retained / 'challenge.json').write_text(json.dumps(current, indent=2) + '\n')
    archive = get(urljoin(BASE, current['download']))
    archive_path = retained / 'evidence.zip'
    archive_path.write_bytes(archive)
    extracted = retained / 'extracted'
    extracted.mkdir(exist_ok=True)
    subprocess.run(['7z', 'x', '-pinfected', '-y', f'-o{extracted}', str(archive_path)], check=True, stdout=subprocess.DEVNULL)
    answers = build(set(qids), extracted, allow_reference_fallback=False)
    (retained / 'answers.json').write_text(json.dumps(answers, indent=2) + '\n')
    if set(answers) != set(qids):
        print(json.dumps({'result': 'incomplete', 'attempt': attempt, 'answer_count': len(answers), 'expected': len(qids), 'missing': sorted(set(qids)-set(answers))}))
        return
    groups = {'other_fields': {}}
    for qid, value in answers.items():
        if qid.startswith('batch-') and qid.endswith(('-control', '-expansion')):
            if qid.endswith('-expansion'):
                choices = ['delayed', 'percent', 'call_double', 'for_indirect']
            else:
                choices = list(dict.fromkeys([value, 'if_guard', 'direct', 'for_loop']))
            for choice in choices:
                groups[qid + '=' + choice] = {qid: choice}
        else:
            groups['other_fields'][qid] = value
    async def submit_groups():
        limits = httpx.Limits(max_connections=2, max_keepalive_connections=2)
        async with httpx.AsyncClient(http2=True, headers=HEADERS, timeout=8, limits=limits) as client:
            async def send(item):
                name, payload = item
                try:
                    response = await client.post(BASE, json={'op': 'submit', 'challenge': CHALLENGE, 'answers': payload})
                    response.raise_for_status()
                    data = response.json()
                    return name, {'result': data.get('result'), 'remaining': data.get('remaining')}
                except Exception as exc:
                    return name, {'result': 'error:' + type(exc).__name__, 'remaining': None}
            return dict(await asyncio.gather(*(send(item) for item in groups.items())))
    results = asyncio.run(submit_groups())
    accepted = {name.split('=', 1)[0]: name.split('=', 1)[1] for name, outcome in results.items() if '=' in name and outcome['result'] in ('accepted', 'CORRECT')}
    results['_accepted'] = accepted
    (retained / 'result.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'attempt': attempt, 'deadline': current.get('deadline'), 'sha256': hashlib.sha256(archive).hexdigest(), 'download': current['download'], 'answer_count': len(answers), 'results': results}))

if __name__ == '__main__':
    main()
