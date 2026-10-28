# How this repository was made (South Africa)

This file is written by the build on 2026-10-28, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Department of Justice: Constitution consolidation | <https://www.justice.gov.za/legislation/constitution/SAConstitution-web-eng.pdf> | 2026-10-28 | 1 | justice.gov.za terms: non-commercial informational or reference use (see README); the text of the Constitution is not subject to copyright (Copyright Act 98 of 1978 s. 12(8)(a)). |
| gov.za / info.gov.za (GCIS), Wayback captures 1999-2012 | <https://web.archive.org/web/19991013161422/http://www.gov.za:80/constitution/1996/96cons.htm> | 2026-10-28 | 0 | gov.za terms: non-commercial informational or reference use. |
| LawLibrary (Laws.Africa), Wayback captures only | <https://lawlibrary.org.za/akn/za/act/1996/constitution/eng@1998-10-07> | 2026-10-28 | 9 | CC BY-NC 4.0; attribution: LawLibrary (lawlibrary.org.za) |
| Government Gazette 37067 (via gov.za) | <https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf> | 2026-10-28 | 1 | Official text of an Act; Copyright Act 98 of 1978 s. 12(8)(a): no copyright in official texts of a legislative nature. |
| Department of Justice consolidation of POPIA | <https://www.justice.gov.za/legislation/acts/2013-004.pdf> | 2026-10-28 | 1 | Used to check the text and for the commencement table only. |
| Information Regulator: Proc. R21 of 2020 (GG 43461) | <https://inforegulator.org.za/wp-content/uploads/2020/07/20200622-gg43461-rg11136-pr21-POPIAsections.pdf> | 2026-10-28 | 1 | Official text. |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the Republic of South Africa, 1996 | 21 | 1997-02-04 to 2026-06-26 |
| `popia` | Protection of Personal Information Act 4 of 2013 | 7 | 2014-04-11 to 2022-02-01 |

The build made 31 commits:

| Commits | Kind |
| ---: | --- |
| 2 | first version of an act |
| 29 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-28.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 24 laws in the record.
- 47 tags.

## Dates

Each commit is dated at noon (Africa/Johannesburg) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution s. 81: "A Bill assented to and signed by the President becomes an Act of Parliament, must be published promptly, and takes effect when published or on a date determined in terms of the Act." https://www.justice.gov.za/legislation/constitution/SAConstitution-web-eng.pdf

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-28
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-28 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/south-africa-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `4d857fc20f03b85cf31f42377453309641ae23a3d68b717b21aac7d29a4e812d` (1115048 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `833a2433a3ea96fd87477ccc7a2ed47dc9e24b48` |
| check.py | `426d4cfb32ce103715be6a00865c0a7bca81a56a` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `05f4393cc3dbf602d53a02270021618c724cbce1` |
| parse.py | `d471f385734b8f027ed04bfab8a3bfa5cc26a691` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

Not yet run for this build.

Not yet run for this build.

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Constitution, sources: the 1996 text as adopted from gov.za (Wayback captures 1999-2000 of gov.za/constitution/1996/*.htm, a page GCIS never updated); intermediate wordings from GCIS consolidations on info.gov.za (Wayback captures 2004-2012) chosen by their amendment notes; the text from each provision's last amendment from the Department of Justice consolidation (justice.gov.za SAConstitution-web-eng.pdf, up to the 17th Amendment), with the 18th Amendment applied from its born-digital gazette text.
- Constitution: where no government source gives an intermediate wording, a LawLibrary (Laws.Africa) point-in-time expression read from a pinned Wayback capture fills it (allowed by the user for gaps; the site itself was never fetched). Licence CC BY-NC 4.0, attribution: LawLibrary (lawlibrary.org.za). Used for: schedule-01a @2006-03-01; schedule-01a @2007-12-14; schedule-02 @1997-02-04; schedule-03 @1999-03-19; schedule-03 @2001-11-21; schedule-06 @1997-02-04; section-103 @2005-12-23; section-157 @1998-10-30; section-178 @1998-10-07; section-221 @1999-03-19.
- Constitution: the amendment Acts of 1997-2008 on gov.za and justice.gov.za are scans whose text layers are OCR; under the no-OCR rule their wording is not used. Only the 16th, 17th and 18th Amendment Acts are born-digital.
- Constitution, dates: each amendment is dated by its commencement: its own clause, a proclamation, or publication (s. 81). Sources: the Department of Justice amendments poster (20yearsConstitution-Amendments_poster.pdf), Proc. R6 of 1997, Proc. R20, R21 and R22 of 2009, Proc. R35 of 2013, and Proclamation Notice 321 of 2026 with its erratum Notice 324 of 2026 (signed 26 March 2026, published 26 June 2026 "with immediate effect", so in force 26 June 2026).
- Constitution: the Seventh Amendment is in force from 26 April 2002 except its ss. 4 and 7 (ss. 163 and 221 of the Constitution, per the consolidation's notes), from 1 December 2003 (DoJ poster).
- Constitution: the Twelfth Amendment is in force from 1 March 2006, except s. 103(3) as inserted by its s. 1, in force on publication, 23 December 2005 (s. 5(2) of that Act).
- Constitution: s. 4 of the Second Amendment (Act 65 of 1998) substitutes "South African Human Rights Commission" for "Human Rights Commission" wherever it occurs; that substitution is applied by code on 7 October 1998.
- Constitution: the Eighth Amendment's Schedule 6A (municipal floor-crossing, 20 June 2002) was renumbered 6B by the Tenth Amendment (20 March 2003), which inserted a new Schedule 6A; both were repealed on 17 April 2009 (14th and 15th Amendments).
- Constitution: one file per section, the Preamble and each Schedule. A provision not yet in force is absent until it commences.
- Constitution, gaps (placeholder "[The source does not give the text in force on this date.]"): schedule-06 item 26 from 1998-10-07 (Second Amendment (1998)): no official text layer and no consolidation gives this wording; placeholder | schedule-06a from 2002-06-20 (Eighth Amendment (2002)): no official text layer and no consolidation gives this wording; placeholder
- Constitution: typography follows the Department of Justice consolidation wherever a historical line has the same words, so diffs show changes of words.
- Constitution: the 1999 and 2004-2012 GCIS web pages sometimes number lists differently from the DoJ consolidation; restarted lettered lists are renumbered by code, but a few label differences remain and show as changes inside amendment commits (s. 61(2)(b), s. 100, s. 168(3), s. 196).
- Constitution: the Citation of Constitutional Laws Act 5 of 2005 renamed the amendment Acts; it changed no words of the Constitution's provisions and has no commit.
- Constitution, provenance of every amended version: schedule-01a 2006-03-01: LawLibrary expression @2006-03-01 (Wayback 20231128162310) | schedule-01a 2007-12-14: LawLibrary expression @2007-12-14 (Wayback 20231128165721) | schedule-01a 2009-04-03: Department of Justice consolidation | schedule-02 1997-02-04: LawLibrary expression @1997-02-04 (Wayback 20231130142540) | schedule-02 2001-11-21: Department of Justice consolidation | schedule-03 1999-03-19: LawLibrary expression @1999-03-19 (Wayback 20231130134237) | schedule-03 2001-11-21: LawLibrary expression @2001-11-21 (Wayback 20231128161214) | schedule-03 2002-06-20: GCIS consolidation captured 2004-12-05 | schedule-03 2009-04-17: Department of Justice consolidation | schedule-06 1997-02-04: item 22 from LawLibrary expression @1997-02-04; other items unchanged | schedule-06 1998-10-07: Act 65 of 1998 s. 4 applied; item 26 (s. 5 of that Act): no text source, placeholder | schedule-06 2001-11-21: Department of Justice consolidation | schedule-06a 2002-06-20: no text source | schedule-06a 2003-03-20: GCIS consolidation captured 2004-12-09 | schedule-06a 2009-04-17: repealed | schedule-06b 2003-03-20: GCIS consolidation captured 2004-12-09 | schedule-06b 2009-04-17: repealed | section-006 2026-06-26: Eighteenth Amendment Act text applied to the consolidation | section-046 2003-03-20: GCIS consolidation captured 2004-12-09 | section-046 2009-04-17: Department of Justice consolidation | section-047 2003-03-20: GCIS consolidation captured 2004-12-09 | section-047 2009-04-17: Department of Justice consolidation | section-049 1999-03-19: Department of Justice consolidation | section-051 2001-11-21: Department of Justice consolidation | section-052 2001-11-21: Department of Justice consolidation | section-054 2001-11-21: Department of Justice consolidation | section-058 2001-11-21: Department of Justice consolidation | section-061 2002-06-20: GCIS consolidation captured 2004-12-09 | section-061 2009-04-17: Department of Justice consolidation | section-062 2002-06-20: GCIS consolidation captured 2004-12-09 | section-062 2009-04-17: Department of Justice consolidation | section-064 2001-11-21: Department of Justice consolidation | section-073 2002-04-26: Department of Justice consolidation | section-076 2003-07-11: Department of Justice consolidation | section-077 2002-04-26: Department of Justice consolidation | section-086 2001-11-21: Department of Justice consolidation | section-090 1997-02-04: Department of Justice consolidation | section-092 2001-11-21: Department of Justice consolidation | section-093 2001-11-21: Department of Justice consolidation | section-099 2003-07-11: Department of Justice consolidation | section-100 2003-07-11: Department of Justice consolidation | section-103 2003-07-11: GCIS consolidation captured 2004-12-09 | section-103 2005-12-23: LawLibrary expression @2005-12-23 (Wayback 20241007173431) | section-103 2006-03-01: Department of Justice consolidation | section-105 2003-03-20: GCIS consolidation captured 2004-12-09 | section-105 2009-04-17: Department of Justice consolidation | section-106 2003-03-20: GCIS consolidation captured 2004-12-09 | section-106 2009-04-17: Department of Justice consolidation | section-108 1999-03-19: Department of Justice consolidation | section-110 2001-11-21: Department of Justice consolidation | section-111 2001-11-21: Department of Justice consolidation | section-120 2002-04-26: Department of Justice consolidation | section-128 2001-11-21: Department of Justice consolidation | section-139 2003-07-11: Department of Justice consolidation | section-155 1998-10-30: GCIS consolidation captured 2004-12-09 | section-155 2006-03-01: Department of Justice consolidation | section-157 1998-10-30: LawLibrary expression @1998-10-30 (Wayback 20231130132356) | section-157 2002-06-20: GCIS consolidation captured 2004-12-09 | section-157 2006-03-01: GCIS consolidation captured 2008-06-22 | section-157 2009-04-17: Department of Justice consolidation | section-158 2009-04-17: Department of Justice consolidation | section-159 1998-10-07: Department of Justice consolidation | section-160 1997-06-30: s. 160(1)(b) commences | section-163 2003-12-01: Department of Justice consolidation | section-165 2013-08-23: Department of Justice consolidation | section-166 2013-08-23: Department of Justice consolidation | section-167 2001-11-21: GCIS consolidation captured 2004-12-05 | section-167 2013-08-23: Department of Justice consolidation | section-168 2001-11-21: GCIS consolidation captured 2004-12-05 | section-168 2013-08-23: Department of Justice consolidation | section-169 2013-08-23: Department of Justice consolidation | section-170 2013-08-23: Department of Justice consolidation | section-172 2013-08-23: Department of Justice consolidation | section-173 2013-08-23: Department of Justice consolidation | section-174 2001-11-21: Department of Justice consolidation | section-175 2001-11-21: GCIS consolidation captured 2004-12-05 | section-175 2013-08-23: Department of Justice consolidation | section-176 2001-11-21: Department of Justice consolidation | section-178 1998-10-07: LawLibrary expression @1998-10-07 (Wayback 20231130145427) | section-178 2001-11-21: GCIS consolidation captured 2004-12-05 | section-178 2013-08-23: Department of Justice consolidation | section-181 1998-10-07: Department of Justice consolidation | section-184 1998-10-07: Department of Justice consolidation | section-185 1998-10-07: Department of Justice consolidation | section-193 1998-10-07: Department of Justice consolidation | section-196 1998-10-07: Department of Justice consolidation | section-216 2002-04-26: Department of Justice consolidation | section-217 2002-04-26: Department of Justice consolidation | section-221 1999-03-19: LawLibrary expression @1999-03-19 (Wayback 20231130134237) | section-221 2003-12-01: Department of Justice consolidation | section-226 2002-04-26: Department of Justice consolidation | section-228 2002-04-26: Department of Justice consolidation | section-230 2002-04-26: Department of Justice consolidation | section-230-a 2001-11-21: Department of Justice consolidation
- POPIA text: the Act as published in Government Gazette 37067 of 26 November 2013 (gov.za PDF, born-digital text layer; no OCR). The Act has not been amended, so its words are the same in every version.
- POPIA commencement: each section is added on the day it commenced: 11 April 2014 (Proc. R25 of 2014: ss. 1, 39-54, 112, 113), 1 July 2020 (Proc. R21 of 2020: ss. 2-38, 55-109, 111, 114(1)-(3)) and 30 June 2021 (Proc. R21 of 2020: ss. 110, 114(4)). The commencement table of the Department of Justice consolidation (justice.gov.za/legislation/acts/2013-004.pdf) and the text of Proc. R21 (inforegulator.org.za) are the sources.
- POPIA s. 115 (short title and commencement) is not named in any proclamation; it is taken as in force from the first commencement, 11 April 2014, because the proclamations are made under it.
- POPIA: each commencement is two commits on the day: the sections, credited to the Act (so blame names Act 4 of 2013), then a no-words commit credited to the proclamation that brought them into force.
- POPIA s. 58(2): GN 297 of 2021 (as amended) made it apply to processing referred to in s. 57 only from 1 February 2022; that is a no-words commit on that day.
- POPIA Schedule: set as rows (law, short title, extent of amendment). Words in square brackets are the gazette's bold bracketed omissions; the underlining of inserted words is not reproduced. Chapter and Part headings are not separate files.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- None at data-build time: fetch.py and parse.py are deterministic code, written with Claude Code (claude-opus-5-5); no model reads, writes or summarises legal text.
