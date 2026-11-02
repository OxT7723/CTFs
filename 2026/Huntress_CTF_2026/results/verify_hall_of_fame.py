#!/usr/bin/env python3
"""Verify the additive Hall of Fame files from anonymized board rows.

Python standard library only. Makes no network requests and executes no
challenge code. This validates calculations within the shared snapshot; it
does not authenticate that snapshot against a live platform.
"""
import argparse
from bisect import bisect_left
from collections import Counter
import csv
import json
from pathlib import Path
import re

MODES = ['time_trial', 'mastery']
COLS = ['rank', 'elapsed_ms', 'par_ms', 'under_par_ms', 'answer_count', 'is_target']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sec(ms):
    return f'{ms // 1000}.{ms % 1000:03d}'


def plain(s):
    return re.sub(r'^[^\w]+', '', s).strip()


def reconstruct(data):
    require(data['anonymized_columns'] == COLS, 'Unexpected anonymized columns')
    ch = {c['id']: c for c in data['challenges']}
    require(len(ch) == len(data['challenges']), 'Duplicate challenge records')
    boards = {}
    own = []
    source_rows = 0
    for board in data['boards']:
        mode, cid = board['mode'], board['challenge_id']
        require(mode in MODES and cid in ch, 'Unknown mode or challenge')
        require((mode, cid) not in boards, 'Duplicate challenge/mode board')
        rows = board['rows']
        require(bool(rows), 'Present boards must contain rows')
        for row in rows:
            require(len(row) == len(COLS), 'Bad row width')
            require(all(type(v) is int for v in row[:5]), 'Expected integer metrics')
            require(type(row[5]) is bool, 'Target flag must be boolean')
            require(row[0] > 0 and row[1] > 0 and row[2] > 0 and row[4] >= 0, 'Invalid numeric metric')
            require(row[3] == row[2] - row[1] and row[3] > 0, 'Under-par arithmetic mismatch')
        times = [r[1] for r in rows]
        require(times == sorted(times), 'Rows must be in ascending elapsed order')
        counts = Counter(times)
        for rank, elapsed, *_ in rows:
            require(rank == 1 + bisect_left(times, elapsed), f'Competition rank mismatch on {mode}/{cid}')
        require(sum(r[5] for r in rows) <= 1, 'More than one target row on a board')
        boards[(mode, cid)] = board
        source_rows += len(rows)
        m = re.fullmatch(r'(.+)-day-(\d+)(?:-.*)?', cid)
        require(m is not None, 'Unexpected task identifier')
        for rank, elapsed, par, under, answers, mine in rows:
            if not mine:
                continue
            own.append({'mode': mode, 'challenge_id': cid, 'challenge_title': plain(ch[cid]['title']),
                'lane': m[1], 'lane_day': int(m[2]), 'release_day': ch[cid]['day'],
                'rank': rank, 'rank_is_tied': counts[elapsed] > 1, 'equal_elapsed_entries': counts[elapsed],
                'board_exported_entries': len(rows), 'elapsed_ms': elapsed, 'elapsed_seconds': sec(elapsed),
                'par_ms': par, 'par_seconds': sec(par), 'under_par_ms': under, 'under_par_seconds': sec(under),
                'answer_count': answers, 'fastest_exported_elapsed_ms': times[0],
                'behind_fastest_exported_ms': elapsed - times[0]})
    own.sort(key=lambda r: (MODES.index(r['mode']), r['rank'], r['elapsed_ms'], r['challenge_id']))
    coverage = []
    per_mode = {}
    for mode in MODES:
        counts = Counter()
        present = {cid: b for (mo, cid), b in boards.items() if mo == mode}
        for c in data['challenges']:
            cid = c['id']
            board = present.get(cid)
            rows = board['rows'] if board else []
            times = Counter(r[1] for r in rows)
            pars = {r[2] for r in rows}
            answers = {r[4] for r in rows}
            mine = [r for r in rows if r[5]]
            m = re.fullmatch(r'(.+)-day-(\d+)(?:-.*)?', cid)
            repeated_names = board['source_repeated_display_name_count'] if board else 0
            coverage.append({'mode': mode, 'challenge_id': cid, 'challenge_title': plain(c['title']),
                'lane': m[1], 'lane_day': int(m[2]), 'release_day': c['day'],
                'board_present': bool(rows), 'exported_entries': len(rows),
                'min_rank': min((r[0] for r in rows), default=''),
                'max_rank': max((r[0] for r in rows), default=''),
                'competition_ranks_valid': True if rows else '',
                'distinct_elapsed_values': len(times), 'tied_elapsed_groups': sum(n > 1 for n in times.values()),
                'entries_in_tied_elapsed_groups': sum(n for n in times.values() if n > 1),
                'source_repeated_display_names': repeated_names,
                'par_min_ms': min(pars, default=''), 'par_max_ms': max(pars, default=''),
                'distinct_par_values': len(pars), 'answer_count_min': min(answers, default=''),
                'answer_count_max': max(answers, default=''), 'distinct_answer_counts': len(answers),
                'target_present': bool(mine), 'target_rank': mine[0][0] if mine else '',
                'target_elapsed_ms': mine[0][1] if mine else ''})
            if rows:
                counts['boards_present'] += 1
                counts['boards_with_equal_elapsed_times'] += any(n > 1 for n in times.values())
                counts['tied_elapsed_groups'] += sum(n > 1 for n in times.values())
                counts['entries_in_tied_elapsed_groups'] += sum(n for n in times.values() if n > 1)
                counts['boards_with_repeated_display_names'] += repeated_names > 0
                counts['boards_with_varying_par_ms'] += len(pars) > 1
                counts['boards_with_varying_answer_count'] += len(answers) > 1
        om = [r for r in own if r['mode'] == mode]
        counts.update({'rows': sum(len(b['rows']) for b in present.values()), 'challenge_catalog_count': len(ch),
            'boards_absent': len(ch) - len(present),
            'largest_exported_board': max(len(b['rows']) for b in present.values()),
            'smallest_exported_board': min(len(b['rows']) for b in present.values()),
            'target_records': len(om), 'target_unique_tasks': len({r['challenge_id'] for r in om}),
            'target_top_1': sum(r['rank'] == 1 for r in om),
            'target_top_3': sum(r['rank'] <= 3 for r in om),
            'target_top_10': sum(r['rank'] <= 10 for r in om),
            'target_top_25': sum(r['rank'] <= 25 for r in om),
            'target_top_10_in_boards_with_at_least_10_entries': sum(r['rank'] <= 10 and r['board_exported_entries'] >= 10 for r in om)})
        per_mode[mode] = dict(counts)
        per_mode[mode]['absent_board_ids'] = [c['id'] for c in data['challenges'] if c['id'] not in present]
        per_mode[mode]['target_records_by_lane'] = dict(sorted(Counter(r['lane'] for r in om).items()))
    coverage.sort(key=lambda r: (r['release_day'], r['lane'], r['lane_day'], MODES.index(r['mode'])))
    both = set(r['challenge_id'] for r in own if r['mode'] == MODES[0]) & set(r['challenge_id'] for r in own if r['mode'] == MODES[1])
    expected_summary = {'source_challenge_count': len(ch), 'source_mode_board_slots': len(ch)*len(MODES),
        'source_present_boards': len(boards), 'source_rows': source_rows,
        'source_missing_mode_boards': len(ch)*len(MODES)-len(boards), 'per_mode': per_mode,
        'target_records': len(own), 'target_distinct_tasks': len({r['challenge_id'] for r in own}),
        'target_tasks_in_both_modes': len(both), 'target_top_1': sum(r['rank'] == 1 for r in own),
        'target_top_3': sum(r['rank'] <= 3 for r in own), 'target_top_10': sum(r['rank'] <= 10 for r in own),
        'target_top_25': sum(r['rank'] <= 25 for r in own),
        'target_top_10_in_boards_with_at_least_10_entries': sum(r['rank'] <= 10 and r['board_exported_entries'] >= 10 for r in own),
        'target_highlights_top_10': [r for r in own if r['rank'] <= 10],
        'target_tied_records': [{'mode': r['mode'], 'challenge_id': r['challenge_id'], 'rank': r['rank'],
            'elapsed_ms': r['elapsed_ms'], 'equal_elapsed_entries': r['equal_elapsed_entries']}
            for r in own if r['rank_is_tied']]}
    return own, coverage, expected_summary


def verify_csv(path, records):
    with path.open(newline='', encoding='utf-8') as f:
        actual = list(csv.DictReader(f))
    expected = [{k: str(v) for k, v in r.items()} for r in records]
    require(actual == expected, f'CSV differs from recomputed values: {path.name}')


def main():
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=here / 'hall-of-fame-data.json')
    p.add_argument('--csv', type=Path, default=here / 'hall-of-fame-results.csv')
    p.add_argument('--json', type=Path, default=here / 'hall-of-fame-results.json')
    p.add_argument('--summary', type=Path, default=here / 'hall-of-fame-summary.json')
    p.add_argument('--coverage', type=Path, default=here / 'hall-of-fame-board-coverage.csv')
    p.add_argument('--output', type=Path, help='Optionally write freshly calculated target CSV')
    args = p.parse_args()
    data = json.loads(args.data.read_text(encoding='utf-8'))
    own, coverage, expected = reconstruct(data)
    verify_csv(args.csv, own)
    verify_csv(args.coverage, coverage)
    result_json = json.loads(args.json.read_text(encoding='utf-8'))
    require(result_json['results'] == own, 'Target JSON differs from recomputed results')
    summary = json.loads(args.summary.read_text(encoding='utf-8'))
    for key in ['source_sha256', 'captured_at', 'target_team_name']:
        require(result_json[key] == data[key] == summary[key], f'Metadata mismatch: {key}')
    for key, value in expected.items():
        if key == 'target_tied_records':
            # Source snapshots are in release-day order, whereas CSV output is in rank order.
            order = lambda r: (r['mode'], r['challenge_id'])
            require(sorted(summary[key], key=order) == sorted(value, key=order), f'Summary mismatch: {key}')
        else:
            require(summary[key] == value, f'Summary mismatch: {key}')
    if args.output:
        with args.output.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(own[0]))
            w.writeheader()
            w.writerows(own)
    print(f'Verified {expected["source_rows"]:,} anonymized rows across {expected["source_present_boards"]} boards; '
          f'{len(own)} target records, {expected["target_distinct_tasks"]} distinct tasks, '
          f'{expected["target_top_10"]} top-10 rows. CSV, JSON, coverage, and numerical summary agree.')
    print('This confirms the supplied snapshot calculations; it does not authenticate a live leaderboard or establish completeness.')


if __name__ == '__main__':
    main()
