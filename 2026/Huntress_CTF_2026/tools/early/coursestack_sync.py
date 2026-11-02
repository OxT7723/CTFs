#!/usr/bin/env python3
"""Sync CourseStack JSON exports into CTF notes. Python 3.10+, no dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

VERSION = 1
SOURCE_START = '<!-- coursestack:source:start -->'
SOURCE_END = '<!-- coursestack:source:end -->'
NOTES = '''
---

## My Notes

### Initial Thoughts

### Enumeration / Analysis

### Commands Used

```bash

```

### Solution

### Flag

```text

```

### Lessons Learned

'''


def clean(value):
    """Remove leading emoji for labels; retain original Unicode text in prompts."""
    text = str(value or '').replace('ℹ', '').replace('\ufe0f', '').strip()
    return re.sub(r'^[^\w]+', '', text).strip()


def folder_name(value):
    value = re.sub(r'[^\w\s-]', '', clean(value))
    value = re.sub(r'\s+', '_', value).strip(' ._-')[:100] or 'Challenge'
    if value.upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}:
        value = '_' + value
    return value


def cell(value):
    return str(value).replace('\n', ' ').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')


def block(text, start, end):
    """Find exactly one valid pair; malformed markers must never erase notes."""
    if start not in text and end not in text:
        return None
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError('Missing or duplicate managed-section markers; restore the markers before syncing.')
    a, b = text.index(start), text.index(end)
    if b < a:
        raise ValueError('Managed-section end marker occurs before its start.')
    return a, b + len(end)


def replace_block(text, content, start, end):
    bounds = block(text, start, end)
    managed = start + '\n' + content.rstrip() + '\n' + end
    if bounds is None:
        return text.rstrip() + '\n\n' + managed + '\n'
    a, b = bounds
    return text[:a] + managed + text[b:]


def find_course(data):
    """Accept course, {course: ...}, Next.js pageProps, and data wrappers."""
    candidates = []
    def visit(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get('chapters'), list):
                candidates.append(obj)
            else:
                for k in ('course', 'pageProps', 'data', 'props'):
                    if k in obj:
                        visit(obj[k])
    visit(data)
    if len(candidates) != 1:
        raise ValueError('Expected one course with chapters[]. Export the course JSON containing lessons and content, not a tenant-only page JSON.')
    return candidates[0]


def category_from(lesson, markdown):
    category = lesson.get('category')
    if isinstance(category, dict):
        category = category.get('name')
    if isinstance(category, str) and category:
        return clean(category)
    lines = markdown.splitlines()
    for n, line in enumerate(lines):
        if line.strip().startswith('|'):
            headers = [x.strip().strip('*').lower() for x in line.strip().strip('|').split('|')]
            if 'category' in headers and n + 2 < len(lines):
                values = [x.strip() for x in lines[n + 2].strip().strip('|').split('|')]
                index = headers.index('category')
                if index < len(values):
                    return clean(values[index].strip('*'))
    match = re.search(r'^\s*\*{0,2}Category\s*:?\*{0,2}\s*:?\s*(.+)$', markdown, re.M | re.I)
    return clean(match.group(1).strip('*')) if match else 'Unknown'


def correct(question):
    if question.get('state') == 'correct':
        return True
    result = question.get('attempt', {}).get('result', {}) if isinstance(question.get('attempt'), dict) else {}
    return isinstance(result, dict) and result.get('correct') is True


def extract(course, args):
    records = []
    for chapter in course['chapters']:
        name = str(chapter.get('name', ''))
        match = re.search(r'\bDay\s*[-_ ]?\s*(\d+)\b', name, re.I)
        day = int(match.group(1)) if match else None
        if args.day is not None and day != args.day:
            continue
        for lesson in chapter.get('lessons', []):
            content = lesson.get('content') or {}
            if not isinstance(content, dict):
                raise ValueError(f'Unexpected content structure in {lesson.get("name")!r}.')
            items = list(content.get('items', []))
            for page in content.get('pages', []):
                items.extend(page.get('items', []))
            quiz = lesson.get('latest_quiz_attempt') or {}
            quiz_correct = {str(q.get('question_id')) for q in quiz.get('quiz_attempt_answer', []) if q.get('is_correct') is True}
            questions = [x for x in items if str(x.get('type', '')).startswith('question')]
            if not questions and not args.include_info:
                continue
            if lesson.get('is_available') is False:
                continue
            title = clean(lesson.get('name', 'Untitled'))
            identity = str(lesson.get('id') or lesson.get('slug') or '')
            if not identity:
                raise ValueError(f'Lesson {title!r} has no ID or slug; stable updates require one.')
            key = hashlib.sha256(identity.encode()).hexdigest()[:20]
            texts = '\n\n'.join(str(x.get('markdown', '')) for x in items if x.get('type') == 'text')
            safe_questions = []
            for n, q in enumerate(questions):
                prompt = str(q.get('question', ''))
                safe_questions.append({'id': str(q.get('id') or f'question-{n}'), 'prompt': prompt,
                                       'points': q.get('points'), 'solved': correct(q) or str(q.get('id')) in quiz_correct,
                                       'single': bool(re.match(r'\s*Single Solve\b', prompt, re.I))})
            # Explicit allowlist: never serialize attempts, submitted answers, tokens, or matchedAnswer.
            parts = []
            for item in items:
                kind = str(item.get('type', ''))
                if kind == 'text':
                    parts.append(str(item.get('markdown', '')))
                elif kind == 'file':
                    parts.append('**Challenge file:** ' + cell(item.get('name', 'Unnamed file')))
                elif kind == 'system':
                    parts.append('**System:** Start/connect through CourseStack or the challenge instructions.')
                elif kind.startswith('question'):
                    points = item.get('points')
                    parts.append('**Scored task:** ' + str(item.get('question', '')) +
                                 (f'\n\n**Points:** {points}' if points is not None else ''))
                else:
                    print(f'Warning: unsupported content type {kind!r} in {title}; review the original page.', file=sys.stderr)
            records.append({'key': key, 'identity': identity, 'title': title, 'day': day,
                            'chapter': clean(name), 'category': category_from(lesson, texts),
                            'source': '\n\n'.join(parts), 'questions': safe_questions,
                            'completed': lesson.get('completed') is True})
    if not records:
        raise ValueError('No available scored challenges found. Check --day, or use --include-info for unscored lessons.')
    if len({r['key'] for r in records}) != len(records):
        raise ValueError('Duplicate lesson IDs in export; refusing ambiguous updates.')
    return records


def solved_label(record, policy):
    qs = record['questions']
    count = sum(q['solved'] for q in qs)
    if record['completed'] or (qs and count == len(qs)):
        return '✅' + (f' ({count}/{len(qs)})' if qs else '')
    if count == 0:
        return '' if qs else '—'
    single = any(q['single'] and q['solved'] for q in qs)
    if policy == 'any' or (policy == 'single' and (single or len(qs) == 1)):
        return f'✅ {"Single Solve " if single else ""}({count}/{len(qs)})'
    return f'Partial ({count}/{len(qs)})'


def writeups(text):
    result = {}
    # Read legacy CourseStack rows wherever they occur, including cs: comments
    # embedded in the Huntress-owned primary index. This importer no longer
    # renders or replaces any root README index region.
    for line in text.splitlines():
        match = re.search(r'<!-- cs:([0-9a-f]{20}) -->', line)
        if match:
            values = re.split(r'(?<!\\)\|', line.strip().strip('|'))
            if len(values) < 5:
                raise ValueError('A CourseStack index row has an invalid number of columns. Escape literal pipes as \\|.')
            result[match.group(1)] = values[-1].strip()
    return result


def checked_path(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes output directory: {relative}')
    return path


def read_text(path):
    return path.read_text(encoding='utf-8') if path.exists() else ''


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.sync-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sync(args):
    source = args.json.resolve()
    root = (args.output or source.parent).resolve()
    data = json.loads(source.read_text(encoding='utf-8-sig'))
    course = find_course(data)
    incoming = extract(course, args)
    state_path = root / '.coursestack-sync.json'
    state = json.loads(read_text(state_path)) if state_path.exists() else {'version': VERSION, 'records': {}}
    if state.get('version') != VERSION:
        raise ValueError('Unsupported sync-state version.')
    course_id = str(course.get('id') or course.get('name') or '')
    if state.get('course_id') and state['course_id'] != course_id:
        raise ValueError('This folder belongs to a different CourseStack course. Use a separate output folder.')
    state['course_id'] = course_id
    title = args.title or state.get('title') or clean(course.get('name', 'CourseStack CTF'))
    state['title'] = title
    records = state['records']
    index_path = root / 'README.md'
    # Respect an existing lower-case root readme on Linux/Windows.
    if not index_path.exists() and (root / 'readme.md').exists():
        index_path = root / 'readme.md'
    index_text = read_text(index_path)
    manual = writeups(index_text)
    for key, value in manual.items():
        if key in records and value:
            records[key]['writeup'] = value
    occupied = {r['path'].casefold() for r in records.values()}
    planned = []
    for new in incoming:
        key = new['key']
        old = records.get(key)
        if old:
            new['path'] = old['path']
            new['writeup'] = old.get('writeup', '')
            new['completed'] = new['completed'] or old.get('completed', False)
            prior = {q['id']: q for q in old['questions']}
            for q in new['questions']:
                q['solved'] = q['solved'] or prior.get(q['id'], {}).get('solved', False)
            # Retain question completion history if a later export omits old modes.
            new['questions'].extend(q for q in old['questions'] if q['id'] not in {x['id'] for x in new['questions']})
        else:
            prefix = f'{new["day"]:02d}' if new['day'] is not None else 'Info'
            base = f'{prefix}-{folder_name(new["title"])}'
            relative = f'{base}/readme.md'
            # Never adopt unrelated existing folders merely because their names match.
            if relative.casefold() in occupied or (root / base).exists():
                relative = f'{base}-{key[:8]}/readme.md'
            if relative.casefold() in occupied or (root / Path(relative).parent).exists():
                raise ValueError(f'Folder collision: {relative}. Move unrelated files or restore sync state.')
            new['path'] = relative
            new['writeup'] = ''
            occupied.add(relative.casefold())
        path = checked_path(root, new['path'])
        text = read_text(path)
        if text and block(text, SOURCE_START, SOURCE_END) is None:
            print(f'Warning: source markers missing in {new["path"]}; existing content preserved and current source appended.', file=sys.stderr)
        content = f'**Release:** {cell(new["chapter"])}\n\n' + new['source']
        updated = replace_block(text, content, SOURCE_START, SOURCE_END)
        if not text:
            updated += NOTES
        planned.append((path, updated))
        records[key] = new
    # Root README index ownership belongs to huntress_sync.py. Keep reading
    # cs: comments above to preserve CourseStack write-up links in sync state,
    # but never overwrite the Huntress-managed primary table.
    planned.append((state_path, json.dumps(state, ensure_ascii=False, indent=2) + '\n'))
    # All parsing and marker validation happens before any write.
    changes = [(p, text) for p, text in planned if read_text(p) != text]
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for path, text in changes:
        action = 'Update' if path.exists() else 'Create'
        print(f'{action}: {path.relative_to(root)}')
        if not args.dry_run:
            if path.exists():
                backup = root / '.coursestack-backups' / timestamp / path.relative_to(root)
                atomic_write(backup, read_text(path))
            atomic_write(path, text)
    print(f'{"Preview" if args.dry_run else "Finished"}: {len(incoming)} exported lessons; {len(records)} retained; {len(changes)} changed files.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json', nargs='?', type=Path, default=Path('challenges.json'), help='Exported course JSON (default: challenges.json)')
    parser.add_argument('-o', '--output', type=Path, help='CTF root; defaults to the JSON file directory')
    parser.add_argument('--title', help='Event title used when creating the root README')
    parser.add_argument('--day', type=int, help='Only sync one release day; retain all previous records')
    parser.add_argument('--include-info', action='store_true', help='Include available unscored lessons, including welcome pages and placeholders')
    parser.add_argument('--solved-policy', choices=('single', 'all', 'any'), default='single', help='Check mark for single solve (default), every mode, or any mode; completion counts always shown')
    parser.add_argument('--dry-run', action='store_true', help='Validate and preview without writing anything')
    args = parser.parse_args(argv)
    root = (args.output or args.json.resolve().parent).resolve()
    lock = root / '.coursestack-sync.lock'
    acquired = False
    try:
        if not args.dry_run:
            root.mkdir(parents=True, exist_ok=True)
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            acquired = True
            with os.fdopen(fd, 'w') as stream:
                stream.write(str(os.getpid()))
        sync(args)
        return 0
    except FileExistsError:
        print('Error: sync lock exists. Close other sync processes; after a crash remove .coursestack-sync.lock and retry.', file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    finally:
        if acquired:
            lock.unlink(missing_ok=True)


if __name__ == '__main__':
    raise SystemExit(main())
