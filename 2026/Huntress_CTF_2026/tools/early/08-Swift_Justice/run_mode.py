"""Run the local Swift Justice parser against a current timed GM assignment.

Usage: python run_mode.py time_trial|mastery
Requires HUNTRESS_GM_TOKEN in the environment. Never stores the token.
"""
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gm import GameMasterClient


BASE_ID = 'binary-reverse-engineering-day-08-swift-network-configuration'
HERE = Path(__file__).resolve().parent


def post(client, body):
    request = Request(client.base_url, data=json.dumps(body, separators=(',', ':')).encode(),
                      headers={'Authorization': 'Bearer ' + client.token,
                               'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(request, timeout=90) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


def process_delivery(client, assignment, index, run_dir):
    delivery_dir = run_dir / f'delivery_{index + 1}'
    delivery_dir.mkdir(parents=True, exist_ok=True)
    archive = delivery_dir / 'evidence.zip'
    if archive.exists() and hashlib.sha256(archive.read_bytes()).hexdigest() == assignment['sha256']:
        data = None
    else:
        url = client.base_url.rstrip('/') + assignment['download']
        request = Request(url, headers={'Authorization': 'Bearer ' + client.token})
        with urlopen(request, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != assignment['sha256']:
            raise RuntimeError(f'delivery {index + 1}: sha256 mismatch')
        archive.write_bytes(data)
    extracted = delivery_dir / 'extracted'
    extracted.mkdir(exist_ok=True)
    if not any(extracted.iterdir()):
        subprocess.run(['7z', 'x', '-y', '-pinfected', '-o' + str(extracted), str(archive)],
                       stdout=subprocess.DEVNULL, check=True)
    output = subprocess.check_output([sys.executable, str(HERE / 'solve_evidence.py'), str(extracted)])
    return json.loads(output)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('time_trial', 'mastery'):
        raise SystemExit('usage: run_mode.py time_trial|mastery')
    mode = sys.argv[1]
    challenge = BASE_ID + '/' + mode
    client = GameMasterClient()
    code, start = post(client, {'op': 'start', 'challenge': challenge})
    if code != 200 or 'attempt_id' not in start:
        raise RuntimeError(f'start failed: HTTP {code}, status={start.get("status", start.get("error"))}')
    run_dir = HERE / 'timed_runs' / mode / start['attempt_id']
    run_dir.mkdir(parents=True, exist_ok=True)
    assignments = start.get('artifacts') or [start]
    print(f'{mode}: attempt={start["attempt_id"]} deliveries={len(assignments)} deadline={start.get("deadline")}', flush=True)
    with ThreadPoolExecutor(max_workers=min(5, len(assignments))) as pool:
        solved = list(pool.map(lambda pair: process_delivery(client, pair[1], pair[0], run_dir), enumerate(assignments)))
    answers = {}
    for i, result in enumerate(solved):
        if mode == 'mastery':
            answers.update({f'set{i + 1}.{key}': value for key, value in result.items()})
        else:
            answers.update(result)
    expected = set(start['answer_ids'])
    if set(answers) != expected:
        raise RuntimeError(f'answer ID mismatch: missing={len(expected-set(answers))} extra={len(set(answers)-expected)}')
    (run_dir / 'answers.json').write_text(json.dumps(answers, indent=2) + '\n')
    code, result = post(client, {'op': 'submit', 'challenge': challenge, 'answers': answers})
    summary = {key: result.get(key) for key in ('result', 'status', 'remaining', 'message', 'unique_attempts_remaining') if key in result}
    (run_dir / 'result_summary.json').write_text(json.dumps({'http_status': code, **summary}, indent=2) + '\n')
    print(f'{mode}: HTTP {code} answers={len(answers)} {summary}', flush=True)


if __name__ == '__main__':
    main()
