#!/usr/bin/env python3
"""Reconstruct UTC daily standings from anonymized saved scoring events.

Python standard library only. No network, challenge execution, or dependencies.
Use --verify to compare the checked-in CSV; --output writes a new CSV.
"""
import argparse
from bisect import bisect_left
import csv
from datetime import date, datetime, timedelta, timezone
import io
import json
from pathlib import Path


def reconstruct(data, first, last):
    entries = data['entries']
    if len(entries) != data['entry_count']:
        raise ValueError('Entry count does not match metadata')
    ids = [e['id'] for e in entries]
    if len(set(ids)) != len(ids) or data['target_entry_id'] not in ids:
        raise ValueError('Entries must have unique identifiers and include target')
    indexed = []
    for entry in entries:
        events = entry['scores']
        times = [e[0] for e in events]
        if times != sorted(times):
            raise ValueError('Scoring timestamps must be sorted')
        # Require the fixed-width UTC ISO strings used by this dataset so lexical
        # comparison preserves chronology, including the millisecond boundary.
        for ts in times:
            parsed = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
            if ts != parsed.isoformat(timespec='milliseconds') + 'Z':
                raise ValueError('Expected fixed-width millisecond UTC timestamps')
        indexed.append((entry['id'], times, events))
    rows = []
    current = first
    while current <= last:
        cutoff = datetime.combine(current + timedelta(days=1), datetime.min.time(),
                                  timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        states = []
        for entry_id, times, events in indexed:
            i = bisect_left(times, cutoff)
            event = events[i - 1] if i else None
            points = event[1] if event else 0
            reached = event[0] if event else ''
            states.append((entry_id, points, reached))
        states.sort(key=lambda s: (-s[1], s[2] or '9999', s[0]))
        rank, own = next((i, s) for i, s in enumerate(states, 1)
                         if s[0] == data['target_entry_id'])
        rows.append({'date_utc': current.isoformat(), 'rank': rank, 'points': own[1],
                     'last_scored_at_utc': own[2], 'included_entries': len(entries),
                     'checkpoint_exclusive_utc': cutoff})
        current += timedelta(days=1)
    return rows


def main():
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, default=here / 'rank-inputs.json')
    p.add_argument('--start', type=date.fromisoformat, default=date(2026, 10, 1))
    p.add_argument('--end', type=date.fromisoformat, default=date(2026, 10, 31))
    p.add_argument('--output', type=Path, help='Write calculated CSV to this path')
    p.add_argument('--verify', type=Path, nargs='?', const=here / 'daily-placement.csv',
                   help='Compare every field with an existing CSV (default: checked-in daily-placement.csv)')
    args = p.parse_args()
    if args.start > args.end:
        p.error('--start must not follow --end')
    data = json.loads(args.input.read_text(encoding='utf-8'))
    rows = reconstruct(data, args.start, args.end)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    text = stream.getvalue()
    if args.output:
        args.output.write_text(text, encoding='utf-8', newline='')
    if args.verify:
        with args.verify.open(newline='', encoding='utf-8') as f:
            expected = list(csv.DictReader(f))
        actual = [{k: str(v) for k, v in row.items()} for row in rows]
        if actual != expected:
            raise SystemExit('Verification failed: computed rows differ from saved CSV')
        print(f'Verified {len(rows)} daily checkpoints across {len(data["entries"]):,} anonymized entries.')
    elif not args.output:
        print(text, end='')


if __name__ == '__main__':
    main()
