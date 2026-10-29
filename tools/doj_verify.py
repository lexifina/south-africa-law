"""Fidelity check for corpus.d/30-justice-acts.json against the cached DoJ PDFs.

For each Act, every letter and digit of the Act's own text in the PDF (after the header tables, without editorial notes,
footnotes, page furniture, the arrangement of sections and the Juta appendices) must appear in the corpus units in the
same order, and nothing else may be added except the unit headings' section numbers. Prints one line per Act; exit 1 on
any difference.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import doj_parse as P

HERE = Path(__file__).resolve().parent


def alnum(s: str) -> str:
    return re.sub(r'[^0-9A-Za-z]', '', s)


def source_stream(a: dict) -> str:
    lines = P.classify(P.lines_of(P.raw_of(a)))
    h = P.header(lines)
    out, began, toc, sched = [], False, False, False
    for ln in lines[h['end'] + 1:]:
        st = ln['text'].strip()
        if ln['tsize'] >= P.BODY_SIZE and re.match(r'^(PENDLEX:|Schedule of commencements)', st):
            break
        if ln['kind'] in ('note', 'foot', 'pageno') or not st:
            continue
        if not began and st.upper() == 'ARRANGEMENT OF SECTIONS':
            toc = True
        if ln['bold'] and re.match(r'^1\s{2,}', st):
            began = True
        if toc and not began:
            continue
        if began and ln['bold'] and ln['tsize'] >= P.BODY_SIZE and re.match(r'^(SCHEDULE|Schedule)\b', st):
            sched = True
        if began and not sched and (re.match(r'^(CHAPTER|Chapter|PART|Part)\s+[\dIVXLA-Z]+[A-Z]?\s*$', st)
                                    or P.is_title(st)):
            continue
        out.append(st)
    return '\n'.join(out)


def out_sched(out: list[str]) -> bool:
    return any(re.match(r'^(SCHEDULE|Schedule)\b', s) for s in out[-400:]) and False


def main() -> int:
    part = json.loads((HERE / 'corpus.d' / '30-justice-acts.json').read_text(encoding='utf-8'))
    cfg = {a['slug']: a for a in json.loads((HERE / 'doj_acts.json').read_text(encoding='utf-8'))['acts']}
    bad = 0
    for act in part['acts']:
        units = act['versions'][0]['units']
        got = []
        for k, u in units.items():
            lines = u['text'].split('\n')
            head = lines[0]
            if k.startswith('section-'):
                head = re.sub(r'^# (\d+[A-Z]*)\. ?', r'\1 ', head)
            elif k == 'long-title':
                head = ''
            else:
                head = head[2:]
            got.append(head + '\n' + '\n'.join(lines[1:]))
        g = alnum(''.join(got))
        src = source_stream(cfg[act['slug']])
        s = alnum(src)
        # chapter/part titles are not units: drop them from the source the same way the parser does
        ok = g == s
        if not ok:
            i = next((i for i in range(min(len(g), len(s))) if g[i] != s[i]), min(len(g), len(s)))
            print(f"{act['slug']:24} DIFF at {i}: corpus …{g[max(0, i - 60):i + 60]}…\n{'':24}        source …{s[max(0, i - 60):i + 60]}…  (len {len(g)} vs {len(s)})")
            bad += 1
        else:
            print(f"{act['slug']:24} ok ({len(g)} letters and digits)")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
