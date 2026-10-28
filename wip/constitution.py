"""The Constitution of the Republic of South Africa, 1996: every version from 4 February 1997, from the
government's own HTML text of it (no OCR).

Sources (all read from the cache):
  original   gov.za/constitution/1996/*.htm as captured by the Wayback Machine in 1999-2000: the text "As adopted on
             8 May 1996 and amended on 11 October 1996", which GCIS never updated on that site (s. 90(4), added in
             1997, is still absent in the 2003 captures).
  snapshots  info.gov.za/documents/constitution/1996/*.htm, Wayback captures 2004-2012: GCIS's consolidated text with
             an amendment note under each amended provision.
  today      gov.za/documents/constitution-republic-south-africa-1996-* (retrieved 2026-10-28): GCIS's consolidated
             text "up to and including the 17th Amendment", plus the Eighteenth Amendment Act (born-digital gazette).
  check      justice.gov.za SAConstitution-web-eng.pdf (Department of Justice, born-digital) for verify.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import fetch
import htmlblocks

HERE = Path(__file__).resolve().parent
GOVZA = 'https://www.gov.za/documents/'

# ------------------------------------------------------------------ the pages

ORIG_HOST = 'http://www.gov.za:80/constitution/1996/'
INFO_HOST = 'info.gov.za/documents/constitution/1996/'

# file name -> which units it holds
PAGES = {'96cons.htm': 'preamble', **{f'96cons{i}.htm': f'ch{i}' for i in range(1, 15)},
         **{f'96conssec{i}.htm': f'sch{i}' for i in range(1, 8)},
         '96conssec1a.htm': 'sch1a', '96conssec6a.htm': 'sch6a', '96conssec6b.htm': 'sch6b', '96preamble.htm': 'preamble'}

TODAY_PAGES = {
    'preamble': 'constitution-republic-south-africa-1996-preamble',
    'ch1': 'constitution/chapter-1-founding-provisions',
    'ch2': 'constitution/chapter-2-bill-rights',
    'ch3': 'constitution/chapter-3-co-operative-government',
    'ch4': 'constitution-republic-south-africa-1996-chapter-4-parliament',
    'ch5': 'constitution-republic-south-africa-1996-chapter-5-president-and-national-executive',
    'ch6': 'constitution-republic-south-africa-1996-chapter-6-provinces',
    'ch7': 'constitution-republic-south-africa-1996-chapter-7-local-government',
    'ch8': 'constitution-republic-south-africa-1996-chapter-8-courts-and-administration-justice',
    'ch9': 'constitution-republic-south-africa-1996-chapter-9-state-institutions-supporting',
    'ch10': 'constitution-republic-south-africa-1996-chapter-10-public-administration',
    'ch11': 'constitution-republic-south-africa-1996-chapter-11-security-services',
    'ch12': 'constitution-republic-south-africa-1996-chapter-12-traditional-leaders',
    'ch13': 'constitution-republic-south-africa-1996-chapter-13-finance',
    'ch14': 'constitution-republic-south-africa-1996-chapter-14-general-provisions',
    'sch1': 'constitution-republic-south-africa-1996-schedule-1-national-flag',
    'sch1a': 'constitution-republic-south-africa-1996-schedule-1a-geographical-areas-provinces',
    'sch2': 'constitution-republic-south-africa-1996-schedule-2-oaths-and-solemn-affirmations',
    'sch3': 'constitution-republic-south-africa-1996-schedule-3-election-procedures',
    'sch4': 'constitution-republic-south-africa-1996-schedule-4-functional-areas-concurrent-national',
    'sch5': 'constitution-republic-south-africa-1996-schedule-5-functional-areas-exclusive-provincial',
    'sch6': 'constitution-republic-south-africa-1996-schedule-6-transitional-arrangements',
    'sch7': 'constitution-republic-south-africa-1996-schedule-7-laws-repealed',
}

SCHEDULE_TITLES = {
    'sch1': 'Schedule 1', 'sch1a': 'Schedule 1A', 'sch2': 'Schedule 2', 'sch3': 'Schedule 3', 'sch4': 'Schedule 4',
    'sch5': 'Schedule 5', 'sch6': 'Schedule 6', 'sch6a': 'Schedule 6A', 'sch6b': 'Schedule 6B', 'sch7': 'Schedule 7',
}

SCHEDULE_HEADINGS = {
    'sch1': 'Schedule 1: National Flag', 'sch1a': 'Schedule 1A: Geographical areas of provinces',
    'sch2': 'Schedule 2: Oaths and Solemn Affirmations', 'sch3': 'Schedule 3: Election Procedures',
    'sch4': 'Schedule 4: Functional Areas of Concurrent National and Provincial Legislative Competence',
    'sch5': 'Schedule 5: Functional Areas of Exclusive Provincial Legislative Competence',
    'sch6': 'Schedule 6: Transitional Arrangements', 'sch6a': 'Schedule 6A', 'sch6b': 'Schedule 6B',
    'sch7': 'Schedule 7: Laws Repealed',
}

NOTE = re.compile(r'^\[[^\[\]]*\b(amended|substituted|inserted|added|deleted|omitted|repealed|renumbered|commencement)\b'
                  r'[^\[\]]*\]?\.?$', re.I)
END = ('Table of contents', 'Share this page', 'Disclaimer', 'Copyright ©', '| Home |', 'Back to top',
       'Next chapter', 'Previous chapter')


def decode(b: bytes) -> str:
    head = b[:3000].decode('ascii', 'replace').lower()
    if 'utf-8' in head:
        return b.decode('utf-8', 'replace')
    return b.decode('cp1252', 'replace')


def norm(s: str) -> str:
    s = s.replace(' ', ' ').replace('​', '')
    s = re.sub(r'\s*­\s*$', '—', s)                     # GCIS uses a soft hyphen as the dash before a list
    s = re.sub(r'\s+­\s+', ' — ', s)
    s = s.replace('­', '')
    s = re.sub(r'\s+-\s*$', '—', s)                          # "that -" at the end of an introduction
    s = re.sub(r'\s*[—–]\s*$', '—', s)
    s = s.replace('‘‘', '“').replace('’’', '”').replace('``', '“').replace("''", '”')
    s = s.replace('–', '—')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,;:.])(?=\s|$)', r'\1', s)
    s = re.sub(r'\(\s+', '(', s)
    s = re.sub(r'\s+\)', ')', s)
    return s


LIT_LABEL = re.compile(r'^(\d{1,2}[A-Z]?|[a-z]{1,2}|[ivx]{1,5})\.\s*(?=\S)')
LIT_LETTER = re.compile(r'^([a-z]{1,2}|[ivx]{1,5})\.\s*(?=\S)')
NUM_LABEL = re.compile(r'^\((\d{1,2}[A-Z]?|[a-z]{1,2}|[ivx]{1,5}|[A-Z])\)\s*')


def para_line(b: dict, literal_labels) -> str:
    text = norm(b['text'])
    label = b.get('label')
    if label is None and literal_labels:
        m = (LIT_LABEL if literal_labels is True else LIT_LETTER).match(text)
        if m and not re.match(r'^(e\.g|i\.e)\.', text):
            label = f'({m.group(1)})'
            text = text[m.end():]
    return norm(f'{label} {text}') if label else text


SEC_HEAD = re.compile(r'^(\d{1,3}[A-Z]?)\.?\s+(.+)$')
SEC_PARA = re.compile(r'^(\d{1,3}[A-Z]?)\.(?:\s+(.*))?$')


def units_of_page(doc: str, part: str, literal_labels: bool) -> dict[str, dict]:
    """{unit key: {'label', 'heading', 'lines': [...], 'notes': [...]}} for one page."""
    bl = htmlblocks.blocks(doc)
    out: dict[str, dict] = {}
    if part.startswith('sch'):
        return schedule_of_page(bl, part, 'letters' if literal_labels else False)
    if part == 'preamble':
        return preamble_of_page(bl, literal_labels)
    cur = None
    pending = None
    last = 0
    for b in bl:
        t = norm(b['text'])
        if any(t.startswith(e) or e in t[:40] for e in END) and cur is not None and not b.get('label'):
            if len(t) < 200:
                cur = None
                pending = None
                continue
        if b['heading']:
            m = SEC_HEAD.match(t)
            if m and _plausible(m.group(1), last):
                cur = _start(out, m.group(1), m.group(2))
                last = int(re.match(r'\d+', m.group(1)).group())
                pending = None
            else:
                pending = t
                cur = None if pending and not m else cur
            continue
        if NOTE.match(t):
            if cur is not None:
                cur['notes'].append(t)
            continue
        m = SEC_PARA.match(t)
        if m and b.get('label') is None and pending is not None and _plausible(m.group(1), last):
            cur = _start(out, m.group(1), pending)
            last = int(re.match(r'\d+', m.group(1)).group())
            pending = None
            rest = m.group(2)
            if rest:
                cur['lines'].append(para_line({'text': rest, 'label': None}, False))
            continue
        if cur is not None:
            line = para_line(b, literal_labels)
            if line:
                cur['lines'].append(line)
    return out


def _plausible(num: str, last: int) -> bool:
    n = int(re.match(r'\d+', num).group())
    return n == last + 1 or (n == last and num[-1:].isalpha()) or (last == 0 and n >= 1) or n == last + 2


def _start(out: dict, num: str, heading: str) -> dict:
    key = 'section-' + f'{int(re.match(r"\d+", num).group()):03d}' + (f'-{num[-1].lower()}' if num[-1].isalpha() else '')
    u = {'label': f's. {num}', 'num': num, 'heading': norm(heading), 'lines': [], 'notes': []}
    out[key] = u
    return u


def schedule_of_page(bl: list[dict], part: str, literal_labels: bool) -> dict[str, dict]:
    title = SCHEDULE_TITLES[part]
    start = None
    for i, b in enumerate(bl):
        t = norm(b['text'])
        if t.startswith('The text below includes all amendments'):
            start = i
            break
    if start is None:
        for i, b in enumerate(bl):
            t = norm(b['text'])
            if re.match(rf'^{re.escape(title)}\b(?![A-Z0-9])', t, re.I) and (b['heading'] or len(t) < 120):
                start = i
    if start is None:
        return {}
    head = SCHEDULE_HEADINGS.get(part, title)
    lines, notes = [], []
    in_toc = False
    seen_content = False
    for b in bl[start + 1:]:
        t = norm(b['text'])
        if any(t.startswith(e) for e in END) and len(t) < 200:
            break
        if NOTE.match(t):
            notes.append(t)
            continue
        if not seen_content:
            if b['heading'] and t in ('Sections', 'Items', 'Contents'):
                in_toc = True
                continue
            if in_toc and not b['heading']:
                continue
            in_toc = False
            if len(re.findall(r'(?:^|\s)\d+[A-Z]?\.\s+[A-Z]', t)) >= 2 and not b['heading']:
                continue          # the page's list of items
        seen_content = True
        line = para_line(b, literal_labels)
        if line:
            lines.append(line)
    key = 'schedule-' + re.sub(r'^sch', '', part).zfill(2 if part[-1].isdigit() else 3)
    return {key: {'label': title, 'num': title, 'heading': head, 'lines': lines, 'notes': notes}}


def preamble_of_page(bl: list[dict], literal_labels: bool) -> dict[str, dict]:
    hits = [i for i, b in enumerate(bl) if norm(b['text']).lower() in ('preamble',) or
            (b.get('anchor') or '').upper() == 'PREAMBLE' or norm(b['text']).startswith('The text below includes all')]
    if not hits:
        return {}
    start = hits[-1]
    lines = []
    for b in bl[start + 1:]:
        t = norm(b['text'])
        if any(t.startswith(e) for e in END) or t.startswith('Chapter 1'):
            break
        if b['heading']:
            break
        lines.append(t)
        if t.startswith('Mudzimu fhatutshedza'):
            break
    return {'preamble': {'label': 'Preamble', 'num': 'Preamble', 'heading': 'Preamble', 'lines': lines, 'notes': []}}


def unit_text(u: dict) -> str:
    head = f'# {u["num"]}. {u["heading"]}' if u['label'].startswith('s. ') else f'# {u["heading"]}'
    return '\n'.join([head, *u['lines']]) + '\n'


# ------------------------------------------------------------------ reading every source

def original() -> dict[str, dict]:
    """The 1996 text as adopted, from the earliest gov.za capture of each page."""
    out = {}
    for name, part in PAGES.items():
        if name in ('96conssec1a.htm', '96conssec6a.htm', '96conssec6b.htm', '96preamble.htm'):
            continue
        rows = [r for r in fetch.cdx('gov.za/constitution/1996/' + name, offline=True) if r[2] == '200']
        if not rows:
            continue
        r = min(rows, key=lambda r: r[0])
        doc = decode(fetch.wayback(r[0], r[1], offline=True))
        for k, u in units_of_page(doc, part, False).items():
            u['source'] = f'https://web.archive.org/web/{r[0]}/{r[1]}'
            u['captured'] = r[0]
            out[k] = u
    return out


def snapshots() -> list[tuple[str, str, dict[str, dict]]]:
    """(capture timestamp, url, units) for every distinct info.gov.za capture of every page."""
    out = []
    for name, part in PAGES.items():
        try:
            rows = [r for r in fetch.cdx(INFO_HOST + name, offline=True) if r[2] == '200']
        except FileNotFoundError:
            continue
        for r in sorted(rows):
            try:
                doc = decode(fetch.wayback(r[0], r[1], offline=True))
            except FileNotFoundError:
                continue
            out.append((r[0], f'https://web.archive.org/web/{r[0]}/{r[1]}', units_of_page(doc, part, False)))
    return out


def today() -> dict[str, dict]:
    out = {}
    for part, slug in TODAY_PAGES.items():
        url = GOVZA + slug
        doc = fetch.fetch(url, offline=True).decode('utf-8', 'replace')
        for k, u in units_of_page(doc, part, True).items():
            u['source'] = url
            out[k] = u
    return out
