"""Read an amending act's PDF with its typographic markup.

South African amending acts print words omitted from the existing text in bold inside square brackets, and words
inserted into it underlined with a solid line. Both survive in born-digital PDFs: brackets as characters, underlines as
vector line drawings just below the words.

quoted_blocks(pdf) returns every passage the act quotes (the text it puts into the Constitution), in order, as printed
lines of tokens. Each token carries two flags: `omitted` (inside square brackets) and `inserted` (underlined).
Margin line numbers and running heads are dropped. A space is kept where the PDF has a space glyph or where two
characters stand more than a quarter of the font size apart (some PDFs leave out the space glyph: "SouthAfrica").
"""
from __future__ import annotations

import re
import sys

import pymupdf

LIGATURES = {'\ufb01': 'fi', '\ufb02': 'fl', '\ufb00': 'ff', '\ufb03': 'ffi', '\ufb04': 'ffl'}
OPEN = ('\u2018\u2018', '\u201c', '``')
CLOSE = ('\u2019\u2019', '\u201d', "''")


def _underlines(page):
    out = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l' and abs(it[1].y - it[2].y) < 0.6 and abs(it[2].x - it[1].x) > 2:
                out.append((min(it[1].x, it[2].x), max(it[1].x, it[2].x), it[1].y))
            elif it[0] == 're' and it[1].height < 1.2 and it[1].width > 2:
                out.append((it[1].x0, it[1].x1, (it[1].y0 + it[1].y1) / 2))
    return out


def chars(pdf_path: str, pages, text_right: float = 470, top: float = 70, bottom: float = 790):
    """[(page, line_no, char, underlined, bold)] with spaces made explicit, for the given page indexes."""
    doc = pymupdf.open(pdf_path)
    out = []
    line_no = 0
    for pno in pages:
        page = doc[pno]
        uls = _underlines(page)
        lines = []
        for b in page.get_text('rawdict')['blocks']:
            for ln in b.get('lines', []):
                for sp in ln['spans']:
                    bold = bool(sp['flags'] & 16) or 'Bold' in sp['font']
                    for ch in sp['chars']:
                        x0, y0, x1, y1 = ch['bbox']
                        if x0 > text_right or y1 < top or y0 > bottom:
                            continue
                        lines.append((round(ch['origin'][1], 0), x0, x1, ch['c'], bold, sp['size'], y1))
        lines.sort(key=lambda c: (c[0], c[1]))
        prev = None
        for base, x0, x1, c, bold, size, y1 in lines:
            if prev is None or abs(base - prev[0]) > 2:
                line_no += 1
                prev = None
            elif c != ' ' and prev[3] != ' ' and x0 - prev[2] > 0.25 * size:
                out.append((pno, line_no, ' ', False, False))
            mid = (x0 + x1) / 2
            ul = c.strip() != '' and any(a <= mid <= b and -1.0 <= y - base <= 4.0 for a, b, y in uls)
            for cc in LIGATURES.get(c, c):
                out.append((pno, line_no, cc, ul, bold))
            prev = (base, x0, x1, c)
    return out


def quoted_blocks(pdf_path: str, pages):
    """The quoted passages, each a list of printed lines, each a list of tokens
    {'t': text, 'inserted': bool, 'omitted': bool}."""
    cs = chars(pdf_path, pages)
    text = ''.join(c[2] for c in cs)
    blocks = []
    i = 0
    while True:
        starts = [(text.find(o, i), o) for o in OPEN if text.find(o, i) >= 0]
        if not starts:
            break
        s, o = min(starts)
        ends = [(text.find(c, s + len(o)), c) for c in CLOSE if text.find(c, s + len(o)) >= 0]
        e, c = min(ends)
        blocks.append(_tokens(cs[s + len(o):e]))
        i = e + len(c)
    return blocks


def _tokens(cs):
    """Tokens split at spaces and at brackets. 'sp' says whether whitespace (or a line break) came before the token."""
    lines = []
    cur_line = None
    depth = 0
    word = None
    space = True
    for pno, line_no, c, ul, bold in cs:
        if line_no != cur_line:
            word = None
            lines.append([])
            cur_line = line_no
            space = True
        if c.isspace():
            word = None
            space = True
            continue
        if c in '[]':
            depth += 1 if c == '[' else -1
            word = None
            continue
        if word is None:
            word = {'t': '', 'ul': 0, 'n': 0, 'pul': 0, 'pn': 0, 'omitted': depth > 0, 'sp': space}
            lines[-1].append(word)
            space = False
        word['t'] += c
        if c.isalnum():
            word['n'] += 1
            word['ul'] += ul
        else:
            word['pn'] += 1
            word['pul'] += ul
    for ln in lines:
        for w in ln:
            if w['n']:
                w['inserted'] = w['ul'] * 2 > w['n']
            else:                # punctuation alone: underlined or not by its own characters
                w['inserted'] = w['pul'] * 2 > w['pn']
    # a line holding only a number is a margin line number or a page number
    return [ln for ln in lines if ln and not (len(ln) == 1 and ln[0]['t'].isdigit())]


def render(block) -> str:
    out = []
    for ln in block:
        out.append(' '.join(('[' + w['t'] + ']') if w['omitted'] else ('_' + w['t'] + '_') if w['inserted'] else w['t']
                            for w in ln))
    return '\n'.join(out)


if __name__ == '__main__':
    pages = [int(p) for p in sys.argv[2].split(',')]
    for n, b in enumerate(quoted_blocks(sys.argv[1], pages)):
        print(f'--- block {n}')
        print(render(b))
