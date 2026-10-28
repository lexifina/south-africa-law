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


# ------------------------------------------------------------------ the Department of Justice consolidation (PDF)

JUSTICE_PDF = 'https://www.justice.gov.za/legislation/constitution/SAConstitution-web-eng.pdf'
PDF_LABEL = re.compile(r'^\((\d{1,2}[A-Z]?|[a-z]{1,2}|[ivx]{1,5}|[A-Z])\)\s')
PDF_SEC = re.compile(r'^(\d{1,3}[A-Z]?)\.\s')


def _pdf_lines(raw: bytes) -> list[dict]:
    import fitz
    doc = fitz.open(stream=raw, filetype='pdf')
    out = []
    for pn, page in enumerate(doc):
        rows: dict[int, list] = {}
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    if not s['text'].strip():
                        continue
                    y = round(s['bbox'][1])
                    key = next((k for k in rows if abs(k - y) <= 2), y)
                    rows.setdefault(key, []).append(s)
        for y in sorted(rows):
            spans = sorted(rows[y], key=lambda s: s['bbox'][0])
            f = spans[0]
            text = ''
            for s in spans:
                t = s['text'].replace('\t', ' ')
                text = (text + ' ' + t) if text and not text.endswith(' ') and not t.startswith(' ') else text + t
            out.append({'page': pn, 'y': y, 'x': spans[0]['bbox'][0], 'x1': spans[-1]['bbox'][2], 'font': f['font'],
                        'size': round(f['size'], 1), 'text': re.sub(r'\s+', ' ', text).strip()})
    return out


def _join_wrapped(parts: list[str], hyphenated: set[str]) -> str:
    s = ''
    for p in parts:
        if not s:
            s = p
            continue
        s = re.sub(r'­\s*$', '-', s)          # a soft hyphen at the end of a line is a line-break hyphen
        m = re.search(r'(\w+)-$', s)
        if m and re.match(r'[a-z]', p):
            nxt = re.match(r'[\w’\']+', p).group()
            if f'{m.group(1)}-{nxt}'.lower() in hyphenated:
                s = s + p
            else:
                s = s[:-1] + p
        elif s.endswith('—') or s.endswith('/'):
            s = s + p
        else:
            s = s + ' ' + p
    return s


def justice_units(hyphenated: set[str]) -> tuple[dict[str, dict], bytes]:
    raw = fetch.fetch(JUSTICE_PDF, offline=True)
    ls = _pdf_lines(raw)
    start = next(i for i, l in enumerate(ls) if l['text'].startswith('We, the people of South Africa') and l['page'] > 3)
    right: dict[int, float] = {}       # the right edge of the text block on each page (margins alternate)
    for l in ls:
        if l['size'] == 7.5 and 'Cond' in l['font']:
            right[l['page']] = max(right.get(l['page'], 0), l['x1'])
    units: dict[str, dict] = {}
    cur = None
    pending = None
    para: list[str] | None = None
    note: list[str] | None = None
    in_schedule = None
    prev = [None, None, False]     # x1 and page of the last body line, and whether it was bold

    def close_para():
        nonlocal para
        if para and cur is not None:
            cur['lines'].append(norm(_join_wrapped(para, hyphenated)))
        para = None

    def close_note():
        nonlocal note
        if note and cur is not None:
            cur['notes'].append(norm(_join_wrapped(note, hyphenated)))
        note = None

    cur = {'label': 'Preamble', 'num': 'Preamble', 'heading': 'Preamble', 'lines': [], 'notes': []}
    units['preamble'] = cur
    for l in ls[start:]:
        t, font, size = l['text'], l['font'], l['size']
        if size == 6.5 and 'Regular' in font:
            continue                      # running head
        if l['y'] > 380 and re.fullmatch(r'\d+', t):
            continue                      # page number
        if size == 6.0:
            close_para()
            if note is None:
                note = [t]
            else:
                note.append(t)
            if t.rstrip().endswith(']') or t.rstrip().endswith('].'):
                close_note()
            continue
        if note and note[0].startswith('[General Note'):
            note.append(t)
            if ']' in t:
                close_note()
            continue
        close_note()
        m = re.match(r'^SCHEDULE (\d+[A-Z]?)\b', t)
        if m and ('Bold' in font or font.startswith('Impact')):
            close_para()
            key = 'schedule-' + (m.group(1).zfill(2) if m.group(1).isdigit() else m.group(1)[:-1].zfill(2) + m.group(1)[-1].lower())
            part = 'sch' + m.group(1).lower()
            cur = {'label': f'Schedule {m.group(1)}', 'num': f'Schedule {m.group(1)}',
                   'heading': SCHEDULE_HEADINGS.get(part, f'Schedule {m.group(1)}'), 'lines': [], 'notes': []}
            units[key] = cur
            in_schedule = key
            continue
        if re.match(r'^Please note\W+the figures after the entries', t) or t.startswith('INDEX'):
            close_para()
            break                         # the index after Schedule 7 is not part of the Constitution
        if t.startswith('[General Note'):
            close_para()
            note = [t]
            if t.rstrip().endswith(']'):
                close_note()
            continue
        if font.startswith('Impact') or (font == 'MyriadPro-Bold' and size in (8.3, 8.0)):
            close_para()
            if t.startswith('CHAPTER'):
                cur = None
                in_schedule = None
            continue                      # chapter numbers and titles; schedule titles
        if in_schedule and font == 'MyriadPro-BoldCond' and size == 7.0 and not cur['lines']:
            continue                      # the schedule's title under "SCHEDULE N"
        if 'Semibold' in font or ('BoldCond' in font and size >= 7.9):
            close_para()
            if in_schedule:
                cur['lines'].append(norm(t))   # item headings stay in the schedule's text
                continue
            pending = norm(t) if pending is None or not para else pending
            pending = norm(t)
            continue
        if cur is not None and cur['label'] == 'Preamble' and font.startswith('MyriadPro-CondIt'):
            if para and prev[0] is not None and prev[0] >= right.get(prev[1], 270) - 22:
                para.append(t)
            else:
                close_para()
                para = [t]
            prev[0] = l['x1']
            continue
        m = PDF_SEC.match(t)
        if m and pending is not None and not in_schedule:
            close_para()
            num = m.group(1)
            key = 'section-' + f'{int(re.match(r"\d+", num).group()):03d}' + (f'-{num[-1].lower()}' if num[-1].isalpha() else '')
            cur = {'label': f's. {num}', 'num': num, 'heading': pending, 'lines': [], 'notes': []}
            units[key] = cur
            pending = None
            rest = t[m.end():].strip()
            prev[0], prev[1], prev[2] = l["x1"], l["page"], False
            if rest:
                para = [rest]
            continue
        if pending is not None and in_schedule is None and cur is not None and cur['label'] != 'Preamble':
            # a heading inside a section (e.g. "Table of Non-Derogable Rights")
            cur['lines'].append(pending)
            pending = None
        if cur is None:
            continue
        short = prev[0] is not None and prev[0] < right.get(prev[1], 270) - 22
        bold = 'Bold' in font
        if PDF_LABEL.match(t) or (in_schedule and re.match(r'^\d+[A-Z]?\.\s', t)) or t.startswith(('–', '•', '“', '"', 'Act No. ')) \
                or (short and not t[:1].islower()) or (bold and not prev[2]) or para is None:
            close_para()
            para = [t]
        else:
            para.append(t)
        prev[0], prev[1], prev[2] = l['x1'], l['page'], bold
    close_para()
    close_note()
    return units, raw


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


# ------------------------------------------------------------------ the amendments

GOVDOC = 'https://www.gov.za/sites/default/files/gcis_document/'
JACTS = 'https://www.justice.gov.za/legislation/acts/'
# key: (label, title, act no., enacted (assent), published, in force, url)
AMENDMENTS = {
    'a35-1997': ('First Amendment (1997)', 'Constitution First Amendment Act of 1997', 'Act 35 of 1997',
                 '1997-08-28', '1997-08-29', '1997-02-04', JACTS + '1997-035.pdf'),
    'a65-1998': ('Second Amendment (1998)', 'Constitution Second Amendment Act of 1998', 'Act 65 of 1998',
                 '1998-09-28', '1998-10-07', '1998-10-07', JACTS + '1998-065.pdf'),
    'a87-1998': ('Third Amendment (1998)', 'Constitution Third Amendment Act of 1998', 'Act 87 of 1998',
                 None, '1998-10-30', '1998-10-30', JACTS + '1998-087.pdf'),
    'a3-1999': ('Fourth Amendment (1999)', 'Constitution Fourth Amendment Act of 1999', 'Act 3 of 1999',
                '1999-03-17', '1999-03-19', '1999-03-19', JACTS + 'const4th-1999.pdf'),
    'a2-1999': ('Fifth Amendment (1999)', 'Constitution Fifth Amendment Act of 1999', 'Act 2 of 1999',
                '1999-03-17', '1999-03-19', '1999-03-19', JACTS + 'const5th-1999.pdf'),
    'a34-2001': ('Sixth Amendment (2001)', 'Constitution Sixth Amendment Act of 2001', 'Act 34 of 2001',
                 '2001-11-20', '2001-11-21', '2001-11-21', JACTS + 'const6th-2001gg.pdf'),
    'a61-2001': ('Seventh Amendment (2001)', 'Constitution Seventh Amendment Act of 2001', 'Act 61 of 2001',
                 '2001-12-07', '2001-12-14', '2002-04-26', JACTS + 'const7th-2001gg.pdf'),
    'a18-2002': ('Eighth Amendment (2002)', 'Constitution Eighth Amendment Act of 2002', 'Act 18 of 2002',
                 '2002-06-19', '2002-06-20', '2002-06-20', JACTS + 'const8th-2002gg.pdf'),
    'a21-2002': ('Ninth Amendment (2002)', 'Constitution Ninth Amendment Act of 2002', 'Act 21 of 2002',
                 '2002-06-19', '2002-06-20', '2002-06-20', JACTS + 'const9th-2002gg.pdf'),
    'a2-2003': ('Tenth Amendment (2003)', 'Constitution Tenth Amendment Act of 2003', 'Act 2 of 2003',
                '2003-03-19', '2003-03-19', '2003-03-20', JACTS + 'const10th-2003gg.pdf'),
    'a3-2003': ('Eleventh Amendment (2003)', 'Constitution Eleventh Amendment Act of 2003', 'Act 3 of 2003',
                '2003-04-09', '2003-04-11', '2003-07-11', JACTS + 'const11th-2003gg.pdf'),
    'c12-2005': ('Twelfth Amendment (2005)', 'Constitution Twelfth Amendment Act of 2005', None,
                 '2005-12-22', '2005-12-23', '2006-03-01', JACTS + 'const12th-2005gg.pdf'),
    'a23-2007': ('Thirteenth Amendment (2007)', 'Constitution Thirteenth Amendment Act of 2007', 'Act 23 of 2007',
                 '2007-12-13', '2007-12-14', '2007-12-14', JACTS + 'const13th-2007gg.pdf'),
    'c14-2008': ('Fourteenth Amendment (2008)', 'Constitution Fourteenth Amendment Act of 2008', None,
                 '2009-01-06', '2009-01-09', '2009-04-17', JACTS + 'const14th_2008gg.pdf'),
    'c15-2008': ('Fifteenth Amendment (2008)', 'Constitution Fifteenth Amendment Act of 2008', None,
                 '2009-01-06', '2009-01-09', '2009-04-17', JACTS + 'const15th_2008gg.pdf'),
    'c16-2009': ('Sixteenth Amendment (2009)', 'Constitution Sixteenth Amendment Act of 2009', None,
                 '2009-03-25', '2009-03-26', '2009-04-03', JACTS + 'const16th_2009gg.pdf'),
    'c17-2012': ('Seventeenth Amendment (2012)', 'Constitution Seventeenth Amendment Act of 2012', None,
                 '2013-02-01', '2013-02-01', '2013-08-23', JACTS + 'const17th_2013gg36128no72.pdf'),
    'a3-2023': ('Eighteenth Amendment (2023)', 'Constitution Eighteenth Amendment Act, 2023', 'Act 3 of 2023',
                '2023-07-19', '2023-07-27', '2026-06-26',
                'https://www.justice.gov.za/constitution/docs/2023-003-Constitution18thAmendment-gg49041-GoN3730-27Jul2023.pdf'),
}
ORDINALS = {'first': 'a35-1997', 'second': 'a65-1998', 'third': 'a87-1998', 'fourth': 'a3-1999', 'fifth': 'a2-1999',
            'sixth': 'a34-2001', 'seventh': 'a61-2001', 'eighth': 'a18-2002', 'ninth': 'a21-2002',
            'tenth': 'a2-2003', 'eleventh': 'a3-2003', 'twelfth': 'c12-2005', 'thirteenth': 'a23-2007',
            'fourteenth': 'c14-2008', 'fifteenth': 'c15-2008', 'sixteenth': 'c16-2009', 'seventeenth': 'c17-2012',
            'eighteenth': 'a3-2023'}
BY_NUMBER = {(int(v[2].split()[1]), int(v[2].split()[3])): k for k, v in AMENDMENTS.items() if v[2]}


def note_events(note: str) -> list[str]:
    n = re.sub(r'Amend\s*ment', 'Amendment', note)
    out = []
    for m in re.finditer(r'Act (?:No\.? ?)?(\d+) of (\d{4})|Constitution ([A-Z][a-z]+) Amendment', n):
        if m.group(1):
            k = BY_NUMBER.get((int(m.group(1)), int(m.group(2))))
        else:
            k = ORDINALS.get(m.group(3).lower())
        if k and k not in out:
            out.append(k)
    return out


# ------------------------------------------------------------------ assembling the history

PLACEHOLDER = '[The source does not give the text in force on this date.]'
WORDS_RE = re.compile(r'[\w]+')


def wkey(line: str) -> tuple:
    s = line.replace('\u00ad', '').replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    s = re.sub(r'^\((\w{1,5})\)\s+\(\1\)', r'(\1)', s)        # "(b) (b) ..." in the 1999 pages
    return tuple(w.lower() for w in WORDS_RE.findall(s))


def hyphen_vocab(*unit_sets) -> set[str]:
    out = set()
    for units in unit_sets:
        for u in units.values():
            for line in u['lines']:
                out.update(w.lower() for w in re.findall(r'\b\w+-\w+\b', line))
    return out


def eighteenth(units: dict) -> dict:
    """Section 6 as amended by the Eighteenth Amendment Act (born-digital gazette text)."""
    import fitz
    raw = fetch.fetch(AMENDMENTS['a3-2023'][6], offline=True)
    doc = fitz.open(stream=raw, filetype='pdf')
    t = '\n'.join(p.get_text() for p in doc)
    t = t[t.index('Amendment of section 6 of Constitution'):t.index('Short title and commencement')]
    quotes = re.findall(r'‘‘(.*?)’’', t, re.S)
    sub1 = norm(re.sub(r'\s+', ' ', quotes[0]))
    sub5a = re.sub(r'\[[^\]]*\]', '', quotes[1])          # words in bold square brackets are omitted
    parts = [norm(p) for p in re.split(r'\n(?=\((?:i|ii|iii)\)\n)', sub5a)]
    lines5a = []
    for p in parts:
        p = norm(re.sub(r'^\((i|ii|iii)\)\s*', r'(\1) ', p.replace('\n', ' ')))
        if p:
            lines5a.append(p)
    u = units['section-006']
    new = []
    skip = False
    for line in u['lines']:
        if line.startswith('(1) '):
            new.append(sub1)
            continue
        if line.startswith('(5) '):
            new.append(line)
            new.extend(lines5a)
            skip = True
            continue
        if skip and line.startswith('(b) '):
            skip = False
        if skip:
            continue
        new.append(line)
    return {**u, 'lines': new}


COMMENCE_1998 = ['213', '214', '215', '216', '218', '226', '227', '228', '229', '230']   # s. 243(5)
SEVENTH_LATE = {'section-163', 'section-229'}       # ss. 4 and 7 of Act 61 of 2001: in force 1 December 2003


def skey(num: str) -> str:
    return 'section-' + f'{int(re.match(r"\d+", num).group()):03d}' + (f'-{num[-1].lower()}' if num[-1].isalpha() else '')


def event_date(ev: str, unit: str) -> str:
    if ev == 'a61-2001' and unit in SEVENTH_LATE:
        return '2003-12-01'
    return AMENDMENTS[ev][5]


def gather():
    orig = original()
    snaps = snapshots()
    vocab = hyphen_vocab(orig, *[u for _, _, u in snaps])
    final, raw = justice_units(vocab)
    final = {k: u for k, u in final.items() if u['lines']}
    return orig, snaps, final, raw


def unit_events(key: str, orig: dict, snaps: list, final: dict) -> set[str]:
    evs = set()
    for _, _, units in snaps:
        if key in units:
            for n in units[key]['notes']:
                evs.update(note_events(n))
    if key in final:
        for n in final[key]['notes']:
            evs.update(note_events(n))
    if key in orig and any(re.search(r'(?<!South African )Human Rights Commission', l) for l in orig[key]['lines'] + [orig[key]['heading']]):
        evs.add('a65-1998')            # s. 4 of Act 65 of 1998: "South African Human Rights Commission" wherever it occurs
    if key == 'section-006':
        evs.add('a3-2023')
    return evs


def observations(key: str, snaps: list, final: dict) -> list[tuple[str, set, dict, str]]:
    """(day, events named in its notes, unit, source url) for every capture of the unit, oldest first."""
    out = []
    for ts, url, units in snaps:
        if key in units and units[key]['lines']:
            u = units[key]
            evs = set()
            for n in u['notes']:
                evs.update(note_events(n))
            out.append((f'{ts[:4]}-{ts[4:6]}-{ts[6:8]}', evs, u, url))
    out.sort(key=lambda x: x[0])
    return out
