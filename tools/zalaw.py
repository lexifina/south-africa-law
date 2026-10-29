"""Prints the Constitution, or one provision of it, as in force on a given day, from this repository's history.

    python tools/zalaw.py 2013-08-22 constitution 169     # section 169 the day before the Seventeenth Amendment
    python tools/zalaw.py 2013-08-23 constitution 169     # ... and the day it took effect
    python tools/zalaw.py 2026-07-01 constitution         # the whole Constitution on 1 July 2026
    python tools/zalaw.py 2010-01-01 constitution sch-1a  # Schedule 1A ("sch-1a", "chapter-8", "preamble")

Every commit carries the day its change took effect in an `In-force:` trailer. The text in force on a day is the last
commit whose In-force date is on or before that day, read from the trailer, not from git's commit date, so the answer
does not depend on the reader's time zone. The record starts on 2009-04-02 (a baseline: see the README); earlier days
are refused. Standard library only.
"""
import datetime as dt
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def order(path: str) -> tuple:
    name = path.rsplit('/', 1)[1][:-3]
    kinds = ['preamble', 'chapter', 'section', 'schedule', 'annexure']
    m = re.search(r'-0*(\d+)([a-z]?)$', name)
    return (kinds.index(name.split('-')[0]), int(m.group(1)) if m else 0, m.group(2) if m else '')


def file_for(key: str) -> str:
    key = key.lower()
    m = re.fullmatch(r'(?:s|section)?-?0*(\d+)([a-z]?)', key)
    if m:
        return f'section-{int(m.group(1)):03d}{m.group(2)}.md'
    m = re.fullmatch(r'(?:sch|schedule)-?(\w+)', key)
    if m:
        return f'schedule-{m.group(1)}.md'
    m = re.fullmatch(r'(?:ch|chapter)-?0*(\d+)', key)
    if m:
        return f'chapter-{int(m.group(1)):02d}.md'
    m = re.fullmatch(r'annexure-?(\w)', key)
    if m:
        return f'annexure-{m.group(1)}.md'
    return key if key.endswith('.md') else key + '.md'


def commit_on(day: str, act: str) -> str:
    out = git('log', '--no-merges', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', act)
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        if d.strip() and d.strip() <= day:
            return h
    return ''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    day, act = sys.argv[1], sys.argv[2].strip('/')
    dt.date.fromisoformat(day)
    commit = commit_on(day, act)
    if not commit:
        sys.exit(f'{act} is not in the record on {day} (the record starts on 2009-04-02).')
    if len(sys.argv) > 3:
        name = file_for(sys.argv[3])
        try:
            sys.stdout.write(git('show', f'{commit}:{act}/{name}'))
        except subprocess.CalledProcessError:
            sys.exit(f'{act}/{name} was not in the text on {day}.')
        return
    entries = {}
    for line in git('ls-tree', '-r', commit, f'{act}/').splitlines():
        meta, path = line.split('\t')
        if path.endswith('.md'):
            entries[path] = meta.split()[2]
    paths = sorted(entries, key=order)
    # one git process for every file: fast enough to print the whole Constitution
    out = subprocess.run(['git', 'cat-file', '--batch'], input=''.join(entries[p] + '\n' for p in paths).encode(),
                         capture_output=True, check=True).stdout
    pos = 0
    for _ in paths:
        nl = out.index(b'\n', pos)
        size = int(out[pos:nl].split()[2])
        sys.stdout.write(out[nl + 1:nl + 1 + size].decode('utf-8') + '\n')
        pos = nl + 1 + size + 1


if __name__ == '__main__':
    main()
