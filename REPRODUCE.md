# How this repository was made

Everything needed to rebuild this repository, hash for hash, and every decision that was made by hand.

## Sources

Retrieved on 2026-10-28 with curl (`fetch.py`: gzip, a User-Agent naming Lexifina, at most four requests at a time,
every answer cached, errors included). robots.txt of www.justice.gov.za and www.gov.za allow these paths and have no
rules for AI crawlers. The Laws.Africa sites (SAFLII, lawlibrary.org.za) disallow ClaudeBot and anthropic-ai and
were not used.

| URL | HTTP | Retrieved | Bytes | sha256 |
|---|---|---|---|---|
| https://www.gov.za/sites/default/files/gcis_document/201409/3209120rg9065.pdf | 200 | 2026-10-28 | 39230 | `0fef2cf71ae41018` |
| https://www.gov.za/sites/default/files/gcis_document/202607/54901gon321.pdf | 200 | 2026-10-28 | 98239 | `b9281d2a5042b3a2` |
| https://www.gov.za/sites/default/files/gcis_document/202607/54933proc324.pdf | 200 | 2026-10-28 | 35735 | `f44ae326d0b34c19` |
| https://www.gov.za/sites/default/files/images/a108-96.pdf | 200 | 2026-10-28 | 6543184 | `68c914519e50f814` |
| https://www.justice.gov.za/constitution/SAConstitution-web-eng-s-a-combined.pdf | 200 | 2026-10-28 | 198348 | `5c6928120f576d63` |
| https://www.justice.gov.za/constitution/chp01.html | 200 | 2026-10-28 | 13379 | `f2c1aba751e01ac6` |
| https://www.justice.gov.za/constitution/chp02.html | 200 | 2026-10-28 | 53530 | `0afc9397e9b514e6` |
| https://www.justice.gov.za/constitution/chp03.html | 200 | 2026-10-28 | 12087 | `6169a44e9a5fb117` |
| https://www.justice.gov.za/constitution/chp04.html | 200 | 2026-10-28 | 70620 | `efa0450dc996ec1a` |
| https://www.justice.gov.za/constitution/chp05.html | 200 | 2026-10-28 | 27533 | `a0e6ef564cfb1365` |
| https://www.justice.gov.za/constitution/chp06.html | 200 | 2026-10-28 | 66591 | `105768e4840eb4bd` |
| https://www.justice.gov.za/constitution/chp07.html | 200 | 2026-10-28 | 29694 | `2d305e8b75a1cfd1` |
| https://www.justice.gov.za/constitution/chp08.html | 200 | 2026-10-28 | 37154 | `e9e6b95bfacd5a3c` |
| https://www.justice.gov.za/constitution/chp09.html | 200 | 2026-10-28 | 25185 | `b5c12cb4674e4130` |
| https://www.justice.gov.za/constitution/chp10.html | 200 | 2026-10-28 | 20131 | `cecd5e188e61de07` |
| https://www.justice.gov.za/constitution/chp11.html | 200 | 2026-10-28 | 23888 | `c825463dc19f57ae` |
| https://www.justice.gov.za/constitution/chp12.html | 200 | 2026-10-28 | 10146 | `14fb3fc75638762b` |
| https://www.justice.gov.za/constitution/chp13.html | 200 | 2026-10-28 | 34461 | `d92deab7fe075a91` |
| https://www.justice.gov.za/constitution/chp14.html | 200 | 2026-10-28 | 16838 | `07e8687adbc44772` |
| https://www.justice.gov.za/constitution/docs/2023-003-Constitution18thAmendment-gg49041-GoN3730-27Jul2023.pdf | 200 | 2026-10-28 | 117276 | `01d0d7d9d04f2367` |
| https://www.justice.gov.za/constitution/preamble.html | 200 | 2026-10-28 | 10988 | `3d474296af4a28ec` |
| https://www.justice.gov.za/legislation/acts/const16th_2009gg.pdf | 200 | 2026-10-28 | 19468 | `545993f2bdc4c2c3` |
| https://www.justice.gov.za/legislation/acts/const17th_2013gg36128no72.pdf | 200 | 2026-10-28 | 160841 | `efc498c4df4fdf1a` |
| https://www.justice.gov.za/legislation/notices/2013/20130822-gg36774-nor35-const17th-commence.pdf | 200 | 2026-10-28 | 88933 | `a9f8214849e0bf56` |

24 documents are read by the build; 31 more were fetched while checking the
sources (robots.txt, terms, earlier amending acts) and are not used.

## Commands

    cd lexifina/scripts/south-africa-law
    python -X utf8 build.py --docs-date 2026-10-28 --repo ../../../south-africa-law         # fetches, then builds
    python -X utf8 check_repo.py ../../../south-africa-law                                   # the check
    python -X utf8 build.py --docs-date 2026-10-28 --offline --verify-rebuild --repo ../../../south-africa-law
    python -X utf8 test_repo.py ../../../south-africa-law
    python -X utf8 ../test_corpus.py ../../../south-africa-law tools/zalaw.py
    python -X utf8 ../test_noon.py ../../../south-africa-law

## Tools

- Python 3.12.10, PyMuPDF 2.0
- git version 2.46.0.windows.1
- curl (Windows build)

## Build scripts (git blob hashes)

| File | Blob |
|---|---|
| actmarkup.py | `4b512a1291b27f1bacfe8711b461f9cb7dd0d515` |
| amendments.py | `528a21d39953a7cf176925f52d2d9b29d46a03a3` |
| build.py | `c4443358cdc68fcf6ebf2503cd0a429cd94a987c` |
| check_repo.py | `acc92d0dd1e5a593fa48eee67fb34e5b67227002` |
| consolidation.py | `052c853fc29c9e97b9f4ddec3e2819d3d6f9c031` |
| docs.py | `3c68d8e279592ac557f2f21d24ea29c362de3726` |
| fetch.py | `e19b501938ce396382c434717216fe4055305373` |
| test_repo.py | `324eeee15211cd3bae562e5a95d2e5d9947cc648` |

## Rebuild check

`build.py --verify-rebuild` on 2026-10-28: a fresh build from the cache gave the same hashes for 6 of 6 commits. Law commits:

- `65b4f4980804ef3ec06264b36a800617ca26dca9` Constitution as in force on 2 April 2009 (baseline)
- `6930f4d1c77eb72cc890e9c2090c9d9ab02e27e9` Sch. 1A: Sixteenth Amendment of 2009
- `e34708dda87e6a536179d7727421a4c5a1498f6d` ss. 165-170, 172, 173, 175, 178: Seventeenth Amendment of 2012
- `6ae5a8546a118406b11ecbcbf67dc7631b1cf066` s. 6: Eighteenth Amendment, Act 3 of 2023

## Decisions made by hand

- **Scope**: the Constitution only, from 2 April 2009. Earlier amendments are in scanned PDFs only.
- **Baseline**: derived by undoing the Eighteenth, Seventeenth and Sixteenth Amendment Acts from the consolidation
  (text as at 7 May 2026). The baseline commit is authored by the consolidation's publisher, not by a law.
- **Which passage belongs to which provision**: listed in `amendments.py` (one entry per quoted passage of each act).
- **Corrections of the Printer's markup** (each checked against the 2003 consolidation scan, see data/derivation.json):
  Seventeenth Amendment of 2012 s. 3(a) (section-167); Seventeenth Amendment of 2012 s. 3(b) (section-167); Seventeenth Amendment of 2012 s. 4 (section-168); Seventeenth Amendment of 2012 s. 5 (section-169); Seventeenth Amendment of 2012 s. 9 (section-175); Seventeenth Amendment of 2012 s. 10 (section-178).
  Five are small (a missing "a", semicolon, comma or full stop, or the end of s. 169); the sixth is the whole old
  s. 168(3), which the Seventeenth Amendment replaced without printing the words it removed.
- **Misreadings of the 2003 scan's text layer** (letters and column order), listed per provision under `ocr` in
  data/derivation.json. They are used only for the check.
- **Where the consolidation and the act differ**, the act is followed (README table).
- **The Eighteenth Amendment's day**: Proclamation Notice 321 of 2026 (Government Gazette 54901, 26 June 2026)
  commences the act "with immediate effect"; the gazette date is the in-force date.

## AI

The builder, the checks and this documentation were written by an AI agent: Claude Opus 5.5 (claude-opus-5-5) in Claude Code, with no
sub-agents and no other model. It read the sources, chose the approach and wrote the code; a person set the task and
the scope. No AI wrote legal text. Almost every word in the law files comes from the sources above by code; the
exceptions are the corrections listed above, which the agent typed into `amendments.py` from the 2003 scan (the old
s. 168(3), and five one-word or punctuation corrections). Code checks each of them against that scan, letter
for letter and comma for comma, on every build. No model runs at build time or at data-build time.
