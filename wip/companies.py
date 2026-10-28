"""Companies Act 71 of 2008: every version from 1 May 2011, built from the cache only.

Sources:
  enacted   the Act as published in Government Gazette 32121 of 9 April 2009 (gov.za, born-digital text layer)
  dates     the Department of Justice consolidation (justice.gov.za 2008-071.pdf): its commencement table and the
            "(wef <date>)" in each amendment note give the day each change took effect, and the notes name the
            amending Act, so they credit each change
  wordings  after each amendment: LawLibrary point-in-time expressions of the Act, read from pinned Internet Archive
            captures (complete captures exist for 2009-04-09, 2014-05-01, 2023-06-01 and 2024-12-27); lines with the
            same words as the gazette keep the gazette's typography
  check     today's text against the Department of Justice consolidation (verify)
"""
from __future__ import annotations

import collections
import hashlib
import re

import constitution as K
import fetch
import gazette
import htmlblocks

GAZ_URL = 'https://www.gov.za/sites/default/files/gcis_document/201409/321214210.pdf'
DOJ_URL = 'https://www.justice.gov.za/legislation/acts/2008-071.pdf'
LL = 'https://lawlibrary.org.za/akn/za/act/2008/71/eng@'
LL_CAPTURES = {'2009-04-09': '20240217005439', '2014-05-01': '20251126111808', '2023-06-01': '20260123233325',
               '2024-12-27': '20260312164844'}
PLACEHOLDER = K.PLACEHOLDER

# Department of Justice consolidation, "as amended by" table (with effect from)
AMENDING = {
    '3/2011': ('act-2011-3', 'Act 3 of 2011', 'Companies Amendment Act, 2011', '2011-04-20', '2011-04-26',
               'https://www.gov.za/documents/companies-amendment-act'),
    '19/2012': ('act-2012-19', 'Act 19 of 2012', 'Financial Markets Act, 2012', '2013-02-01', '2013-02-01', DOJ_URL),
    '22/2022': ('act-2022-22', 'Act 22 of 2022', 'General Laws (Anti-Money Laundering and Combating Terrorism Financing) '
                'Amendment Act, 2022', '2022-12-29', '2022-12-29', DOJ_URL),
    '23/2021': ('act-2021-23', 'Act 23 of 2021', 'Financial Sector Laws Amendment Act, 2021', None, None, DOJ_URL),
    '16/2024': ('act-2024-16', 'Act 16 of 2024', 'Companies Amendment Act, 2024', None, None, DOJ_URL),
    '17/2024': ('act-2024-17', 'Act 17 of 2024', 'Companies Second Amendment Act, 2024', None, None, DOJ_URL),
}
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], 1)}


def iso(d: str) -> str:
    m = re.match(r'(\d{1,2}) (\w+) (\d{4})', d)
    return f'{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}'


def skey(num: str) -> str:
    return K.skey(num)


# ------------------------------------------------------------------ the gazette (as enacted)

def gazette_units() -> tuple[dict[str, dict], bytes]:
    raw = fetch.fetch(GAZ_URL, offline=True)
    import fitz
    doc = fitz.open(stream=raw, filetype='pdf')
    first = next(i for i in range(len(doc)) if re.search(r'^1\. In this Act', doc[i].get_text(), re.M))
    ls = gazette.lines(raw, first, len(doc))
    units: dict[str, dict] = {}
    heading = None
    cur = None
    sched = None
    for text, l in gazette.paragraphs(ls):
        m = re.match(r'^SCHEDULE (\d+)\b', text)
        if l.bold and m:
            sched = m.group(1)
            cur = {'label': f'Schedule {sched}', 'num': f'Schedule {sched}', 'heading': f'Schedule {sched}',
                   'lines': [], 'notes': []}
            units['schedule-' + sched.zfill(2)] = cur
            continue
        if sched is not None:
            if cur is not None and not cur['lines'] and l.bold and cur['heading'] == f'Schedule {sched}':
                cur['heading'] = f'Schedule {sched}: {K.norm(text).capitalize()}'
                continue
            cur['lines'].append(K.norm(text))
            continue
        m = gazette.SECTION.match(text)
        if l.bold and m and l.x0 > 118:
            num = m.group(1)
            cur = {'label': f's. {num}', 'num': num, 'heading': heading or '', 'lines': [], 'notes': []}
            units[skey(num)] = cur
            rest = K.norm(text[m.end():])
            if rest:
                cur['lines'].append(rest)
            heading = None
            continue
        if l.bold and not text.startswith('‘‘'):
            if re.match(r'^(CHAPTER|Part [A-Z]\b|PART)', text):
                cur = None
                heading = None
                continue
            heading = K.norm(text)
            cur = None
            continue
        if cur is not None:
            cur['lines'].append(K.norm(text))
    return units, raw


# ------------------------------------------------------------------ LawLibrary expressions

def ll_units(day: str) -> dict[str, dict]:
    raw = fetch.fetch(f'https://web.archive.org/web/{LL_CAPTURES[day]}id_/{LL}{day}', offline=True)
    root = htmlblocks.parse(raw.decode('utf-8', 'replace'))
    out: dict[str, dict] = {}
    stack = [root]
    while stack:
        n = stack.pop()
        if isinstance(n, str):
            continue
        i = n.attrs.get('id', '')
        if n.tag == 'section' and 'att_' not in i and re.search(r'(^|__)sec_\d+[A-Z]*$', i):
            num = i.rsplit('sec_', 1)[1]
            lines: list[str] = []
            K._akn_lines(n, lines, [])
            if lines:
                m = re.match(r'^(\d+[A-Z]*)\.\s+(.*)$', lines[0])
                out[skey(num)] = {'label': f's. {num}', 'num': num, 'heading': m.group(2) if m else lines[0],
                                  'lines': lines[1:], 'notes': []}
            continue
        if n.tag == 'div' and re.fullmatch(r'att_\d+', i):
            lines = []
            K._akn_lines(n, lines, [])
            m = re.match(r'^Schedule (\d+)$', lines[0]) if lines else None
            if m:
                out['schedule-' + m.group(1).zfill(2)] = {'label': f'Schedule {m.group(1)}', 'num': f'Schedule {m.group(1)}',
                                                         'heading': f'Schedule {m.group(1)}: {lines[1]}' if len(lines) > 1 else '',
                                                         'lines': lines[2:], 'notes': []}
            continue
        stack.extend(reversed(n.children))
    return {k: K._fix_label_space(u) for k, u in out.items()}


# ------------------------------------------------------------------ the DoJ consolidation: notes and dates

def doj_text() -> str:
    import fitz
    doc = fitz.open(stream=fetch.fetch(DOJ_URL, offline=True), filetype='pdf')
    t = '\n'.join(p.get_text() for p in doc)
    t = re.sub(r'© \d{4} Juta and Company \(Pty\) Ltd\.\nDownloaded:[^\n]*\n', '\n', t)
    return t


def doj_sections() -> dict[str, dict]:
    """{unit key: {'words': [...], 'notes': [...], 'events': {(act, day)}}} from the DoJ text."""
    t = doj_text()
    body = t[t.index('CHAPTER 1\nINTERPRETATION, PURPOSE AND APPLICATION (ss'):]
    out: dict[str, dict] = {}
    cur = None
    last = 0
    for line in body.split('\n'):
        m = re.match(r'^(\d+[A-Z]*)  (\S.*)$', line)
        if m and int(re.match(r'\d+', m.group(1)).group()) in (last, last + 1, last + 2, last + 3):
            last = int(re.match(r'\d+', m.group(1)).group())
            cur = out.setdefault(skey(m.group(1)), {'lines': [m.group(2)], 'notes_raw': []})
            continue
        m = re.match(r'^Schedule (\d+)\s*$', line.strip())
        if m:
            cur = out.setdefault('schedule-' + m.group(1).zfill(2), {'lines': [], 'notes_raw': []})
            continue
        if cur is not None:
            cur['lines'].append(line)
    for k, u in out.items():
        txt = re.sub(r'\s+', ' ', '\n'.join(u['lines']))
        notes = re.findall(r'\[(?!NB)[^\[\]]*\]', txt)
        u['notes'] = [n for n in notes if re.search(r'(amended|substituted|inserted|added|deleted|repealed|renumbered)', n)]
        u['pending'] = re.findall(r'\[NB:[^\[\]]*\]', txt)
        evs = set()
        for n in u['notes']:
            for m in re.finditer(r'Act (\d+) of (\d{4})(?: \(wef ([^)]+)\))?', n):
                key = f'{m.group(1)}/{m.group(2)}'
                if key in AMENDING and m.group(3):
                    for d in re.findall(r'\d{1,2} \w+ \d{4}', m.group(3)):
                        evs.add((AMENDING[key][0], iso(d)))
        u['events'] = evs
        body_txt = re.sub(r'\[[^\[\]]*\]', ' ', txt)
        u['text'] = body_txt
    return out


# ------------------------------------------------------------------ history

def history():
    gaz, raw = gazette_units()
    ll = {d: ll_units(d) for d in LL_CAPTURES}
    doj = doj_sections()
    final = ll['2024-12-27']
    keys = sorted(set(gaz) | set(final))
    hist: dict[str, list] = {}
    gaps: list[str] = []
    obs_days = sorted(d for d in LL_CAPTURES if d > '2011-05-01')
    for k in keys:
        evs = sorted(doj.get(k, {}).get('events', set()), key=lambda x: x[1])
        dates = sorted({d for _, d in evs})
        base = gaz.get(k)
        ref_lines = {}
        if base is not None:
            for l in base['lines']:
                ref_lines.setdefault(K.wkey(l), l)

        def tidy(u):
            if u is None:
                return None
            lines = [ref_lines.get(K.wkey(l), l) for l in u['lines']]
            head = base['heading'] if base is not None and K.wkey(base['heading']) == K.wkey(u['heading']) else u['heading']
            return {**u, 'lines': lines, 'heading': head}

        h = []
        start = '2011-05-01'
        if base is not None:
            b = base
            if k == 'section-011':
                # s. 11(1)(a)(ii) and (iii) commence on 1 May 2014 (s. 225(2); DoJ commencement table)
                b = drop_lines(b, ['(ii) ', '(iii) '], within='(a) ')
            h.append((start, b, [], 'Government Gazette 32121 (as enacted)'))
        prev = h[-1][1] if h else None
        for i, d in enumerate(dates):
            group = sorted({a for a, dd in evs if dd == d})
            nxt = dates[i + 1] if i + 1 < len(dates) else None
            if nxt is None:
                cand, how = tidy(final.get(k)), f'LawLibrary @2024-12-27 (checked against the DoJ consolidation)'
            else:
                o = next((od for od in obs_days if d <= od < nxt), None)
                if o is not None and k in ll[o]:
                    cand, how = tidy(ll[o][k]), f'LawLibrary @{o} (Wayback {LL_CAPTURES[o]})'
                else:
                    tmpl = prev or final.get(k)
                    cand = {**tmpl, 'lines': [PLACEHOLDER]}
                    how = 'no text source'
                    gaps.append(f'{k} from {d} to {nxt}')
            h.append((d, cand, group, how))
            prev = cand
        if not dates and base is None and k in final:
            gaps.append(f'{k}: in today\'s text but not in the gazette, and no note names a law')
            h.append(('2011-05-01', tidy(final[k]), [], 'LawLibrary @2024-12-27'))
        if not dates and base is not None and k in final:
            # never amended: is today's text the gazette's?
            a = [w for l in base['lines'] for w in K.wkey(l)]
            b2 = [w for l in final[k]['lines'] for w in K.wkey(l)]
            if a != b2:
                gaps.append(f'{k}: today\'s text differs from the gazette but no note names a law')
        hist[k] = h
    return hist, gaps, raw, doj, gaz, final


def drop_lines(u: dict, prefixes: list[str], within: str) -> dict:
    out, inside = [], False
    for l in u['lines']:
        if l.startswith(within):
            inside = True
        elif re.match(r'^\([a-z]\) ', l) or re.match(r'^\(\d+\) ', l):
            inside = False
        if inside and any(l.startswith(p) for p in prefixes):
            continue
        out.append(l)
    return {**u, 'lines': out}
