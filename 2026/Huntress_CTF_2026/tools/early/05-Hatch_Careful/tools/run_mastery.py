#!/usr/bin/env python3
"""Statically solve the assigned two-bundle Hatch Careful Mastery attempt."""
import asyncio
import hashlib
import json
import os
import subprocess
from urllib.parse import urljoin

import httpx
from solve_hatch import build, HERE

BASE = 'https://2026.huntress.ctf.games/'
CHALLENGE = 'script-analysis-day-05-python-carrier-lab/mastery'
HEADERS = {'Authorization': 'Bearer ' + os.environ['HUNTRESS_GM_TOKEN']}

async def main():
    limits = httpx.Limits(max_connections=3, max_keepalive_connections=3)
    async with httpx.AsyncClient(http2=True, headers=HEADERS, timeout=10, limits=limits) as client:
        status = await client.get(BASE, params={'op': 'status', 'challenge': CHALLENGE})
        current_status = status.json()
        if current_status.get('result') == 'CORRECT':
            print(json.dumps({'result': 'already_solved', 'attempt': current_status.get('attempt_id')}))
            return
        if current_status.get('result') == 'expired':
            action = {'op': 'retry', 'challenge': CHALLENGE}
        else:
            action = {'challenge': CHALLENGE}
        response = await client.post(BASE, json=action)
        response.raise_for_status()
        current = response.json()
        attempt = current.get('attempt_id', 'unknown-attempt')
        retained = HERE / 'artifacts/mastery' / attempt
        retained.mkdir(parents=True, exist_ok=True)
        (retained / 'challenge.json').write_text(json.dumps(current, indent=2) + '\n')
        qids = current.get('answer_ids') or [q['id'] for q in current.get('questions', [])]
        bundle = retained / 'bundle'
        bundle.mkdir(exist_ok=True)
        if current.get('artifacts'):
            async def fetch(item):
                response = await client.get(urljoin(BASE, item['download']))
                response.raise_for_status()
                return item, response.content
            downloads = await asyncio.gather(*(fetch(item) for item in current['artifacts']))
            archive_metadata = []
            for index, (item, content) in enumerate(downloads, 1):
                (bundle / f'evidence-{index:02d}.zip').write_bytes(content)
                archive_metadata.append({'filename': f'evidence-{index:02d}.zip', 'sha256': hashlib.sha256(content).hexdigest(), 'download': item['download']})
        elif current.get('download'):
            download = current['download']
            response = await client.get(urljoin(BASE, download))
            response.raise_for_status()
            content = response.content
            outer_path = retained / 'mastery.zip'
            outer_path.write_bytes(content)
            subprocess.run(['7z', 'x', '-pinfected', '-y', f'-o{bundle}', str(outer_path)], check=True, stdout=subprocess.DEVNULL, timeout=8)
            archive_metadata = [{'filename': 'mastery.zip', 'sha256': hashlib.sha256(content).hexdigest(), 'download': download}]
        else:
            raise RuntimeError('Mastery response has no downloads; inspect retained challenge.json')
        answers = {}
        for index in (1, 2):
            filename = f'evidence-{index:02d}.zip'
            archive_path = bundle / filename
            extracted = retained / ('extracted-' + str(index))
            extracted.mkdir(exist_ok=True)
            subprocess.run(['7z', 'x', '-pinfected', '-y', f'-o{extracted}', str(archive_path)], check=True, stdout=subprocess.DEVNULL, timeout=8)
            set_name = 'set' + str(index)
            subset = {qid for qid in qids if qid.startswith(set_name + '.')}
            answers.update(build(subset, extracted, allow_reference_fallback=False))
        (retained / 'answers.json').write_text(json.dumps(answers, indent=2) + '\n')
        if set(answers) != set(qids):
            print(json.dumps({'result': 'incomplete', 'attempt': attempt, 'expected': len(qids), 'actual': len(answers), 'missing': sorted(set(qids) - set(answers))}))
            return
        groups = {'other_fields': {}}
        alternatives = {}
        for qid, value in answers.items():
            base_id = qid.split('.', 1)[-1]
            if base_id.startswith('batch-') and base_id.endswith(('-control', '-expansion')):
                if base_id.endswith('-expansion'):
                    primary = 'delayed'
                    choices = ['percent', 'call_double', 'for_indirect']
                else:
                    primary = value
                    choices = ['if_guard', 'direct', 'for_loop', 'if_defined', 'call_subroutine', 'goto_dispatch', 'errorlevel_guard']
                groups[qid + '=' + primary] = {qid: primary}
                alternatives[qid] = [choice for choice in choices if choice != primary]
            else:
                groups['other_fields'][qid] = value
        async def send(item):
            name, payload = item
            try:
                response = await client.post(BASE, json={'op': 'submit', 'challenge': CHALLENGE, 'answers': payload})
                response.raise_for_status()
                data = response.json()
                return name, {'result': data.get('result'), 'remaining': data.get('remaining')}
            except httpx.HTTPStatusError as exc:
                return name, {'result': 'http:' + str(exc.response.status_code)}
            except Exception as exc:
                return name, {'result': 'error:' + type(exc).__name__}
        results = dict(await asyncio.gather(*(send(item) for item in groups.items())))
        missed = [qid for qid in alternatives if results[qid + '=' + ('delayed' if qid.endswith('-expansion') else answers[qid])]['result'] not in ('accepted', 'CORRECT')]
        retry_groups = {qid + '=' + choice: {qid: choice} for qid in missed for choice in alternatives[qid]}
        if retry_groups:
            results.update(dict(await asyncio.gather(*(send(item) for item in retry_groups.items()))))
        (retained / 'result.json').write_text(json.dumps(results, indent=2) + '\n')
        accepted = {name.split('=',1)[0]: name.split('=',1)[1] for name, outcome in results.items() if '=' in name and outcome['result'] in ('accepted', 'CORRECT')}
        unresolved = sorted(qid for qid in qids if '.batch-' in qid and qid.endswith(('-control', '-expansion')) and qid not in accepted)
        print(json.dumps({'attempt': attempt, 'deadline': current.get('deadline'), 'answer_count': len(answers), 'artifacts': archive_metadata, 'other_fields': results['other_fields'], 'accepted_batch_labels': len(accepted), 'unresolved_batch_labels': unresolved, 'correct': any(v['result'] == 'CORRECT' for v in results.values()), 'result_counts': {label: sum(v['result'] == label for v in results.values()) for label in ('accepted','incorrect','CORRECT','expired','already_solved')}}))

if __name__ == '__main__':
    asyncio.run(main())
