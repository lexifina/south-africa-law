# South Africa: law history in git

The law of South Africa as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a section; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `za/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the Republic of South Africa, 1996 | 21 | From its commencement (4 February 1997) through all 18 amendment Acts to the Eighteenth Amendment (South African Sign Language, in force 26 June 2026) |
| `popia/` | Protection of Personal Information Act 4 of 2013 | 7 | Each staged commencement: 11 April 2014, 1 July 2020, 30 June 2021, and the deferred application of s. 58(2) from 1 February 2022 |

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did s. 46 of the Constitution say on 1 January 2005? | `python tools/on.py 2005-01-01 constitution section-046` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2005-01-01T23:59:59Z" main -- constitution/section-046.md):constitution/section-046.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2005-01-01T23:59:59Z" main -- constitution/section-046.md; git show "$($r):constitution/section-046.md"` |
| Which amendment wrote each paragraph of s. 178? | `git blame constitution/section-178.md` |
| Every change to s. 47, word by word | `git log -p --word-diff constitution/section-047.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one amendment changed | `git show law/c17-2012` (tags `law/<key>` mark each law's commit) |
| The whole Constitution on a date | `python tools/on.py 2004-01-01 constitution` |
| Which POPIA sections were in force on 1 January 2018? | `python tools/on.py 2018-01-01 popia` |
| Laws passed but not yet in force | `git log main..future` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Africa/Johannesburg, on the day the change took effect** (the in-force date). Assent and publication dates are trailers (`Enacted:`, `Published:`); the in-force day is in `In-force:`, which the tools read.
- **Default rule.** Constitution s. 81: "A Bill assented to and signed by the President becomes an Act of Parliament, must be published promptly, and takes effect when published or on a date determined in terms of the Act." An amendment with no commencement clause is dated by its publication in the Government Gazette; one that commences by proclamation is dated by the proclamation.
- **Commencement dates of the amendments** come from the Department of Justice's list of amendments with their dates of commencement (justice.gov.za), the amendment Acts' own clauses, and the proclamations (Proc. R6 of 1997; R20, R21, R22 of 2009; R35 of 2013; Proclamation Notice 321 of 2026 and its erratum 324 of 2026).
- **Retroactive amendment.** The First Amendment (Act 35 of 1997, assented 28 August 1997) "must be regarded as having taken effect on 4 February 1997", so its commit is dated 4 February 1997, after the Constitution's own commit that day.
- **Staged commencement.** The Constitution: s. 160(1)(b) from 30 June 1997 (Proc. R6 of 1997); ss. 213-216, 218 and 226-230 from 1 January 1998 (s. 243(5)). The Seventh Amendment: 26 April 2002, its ss. 4 and 7 from 1 December 2003. The Twelfth: 1 March 2006, s. 103(3) on publication (23 December 2005). POPIA: 11 April 2014, 1 July 2020, 30 June 2021. A provision appears in its file on the day it commences.
- The Eighteenth Amendment (assented 19 July 2023) commenced "with immediate effect" by Proclamation Notice 321 of 2026, published 26 June 2026; the erratum (Notice 324 of 2026) gives the signing day, 26 March 2026. The commit is dated 26 June 2026.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version of every act is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- Health checks: no merge commits on `main`, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse.
- **Today's text against the official consolidation** (`tools/verify.py`, 28 October 2026): all 253 provisions of the Constitution match, word for word, the Department of Justice consolidation (up to the 17th Amendment) with the 18th Amendment applied from its gazette text. 114 of POPIA's 115 sections match the Department of Justice consolidation word for word; in s. 112(2)(f) the gazette text has no semicolon after "section 69(2)" and the consolidation adds one. We keep the gazette.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`c17-2012@gov-za.invalid`), so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come from the sources' amendment notes** ("[Sub-s. (1) amended by s. 1 of the Constitution Tenth Amendment Act of 2003 ...]"), in the Department of Justice and GCIS consolidations. The notes are not in the text.
- **Commencement is a commit too.** The proclamations that brought the Constitution and POPIA into force are commits that change no words (`Words-changed: no`), after the commit of the Act's words on the same day.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see which words each law changed.

## What it does not show

- **Wording no clean source gives.** The amendment Acts of 1997 to 2008 survive only as scanned gazettes, and this record uses no OCR. Where neither a government consolidation nor a LawLibrary point-in-time text (read from the Internet Archive) gives the wording in force for a period, the provision reads "[The source does not give the text in force on this date.]" for that period: Schedule 6 item 26 from 7 October 1998 to 21 November 2001, and the Eighth Amendment's Schedule 6A from 20 June 2002 to 20 March 2003. The commits still name the amending law and its date.
- **Typography of old versions.** Historical versions come from GCIS web pages and LawLibrary; wherever a line has the same words as today's official consolidation, its typography is used, so diffs show changes of words, but older lines that no longer exist keep their source's punctuation.
- **Section and Chapter headings, parts and Chapter titles** are not separate files. Each Schedule is one file.
- **Other acts.** The Companies Act 71 of 2008 is the next act planned.
- **Court orders.** Declarations of invalidity by the Constitutional Court are not commits unless an amendment Act changed the words.

## How it is built

`tools/fetch.py` downloads every source once through curl (one request per second per host, one per three seconds to the Internet Archive, cached by the sha256 of the URL), `tools/parse.py` turns the cache into `corpus.json` (`tools/gazette.py` reads born-digital gazette PDFs, `tools/constitution.py` and `tools/htmlblocks.py` the Constitution's sources), and the shared builder `tools/build.py` writes the history with `git fast-import`. The same corpus always gives the same hashes. `REPRODUCE.md` records every command, tool version, data hash and decision, and the result of a hash-for-hash rebuild.

No AI model wrote or changed legal text. Claude Opus 5.5 (`claude-opus-5-5`) wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Used for | Terms |
| --- | --- | --- |
| [Department of Justice](https://www.justice.gov.za/legislation/constitution/pdf.html): Constitution consolidation (born-digital PDF), list of amendments, amendment Acts, proclamations, POPIA consolidation | Today's text of the Constitution; dates; checking POPIA | Site terms: content may be viewed, copied, downloaded and distributed "only for non-commercial informational or reference purposes"; commercial use needs written permission (webmaster@justice.gov.za) |
| [gov.za](https://www.gov.za/documents/constitution-republic-south-africa-1996) (GCIS): the Constitution (1996 text on gov.za/constitution/1996, 1999-2003; consolidations on info.gov.za, 2004-2012, read from Internet Archive captures pinned by timestamp), the POPIA gazette (GG 37067), proclamations | The 1996 text; intermediate wordings; POPIA's text | Same wording as above (electronic@gcis.gov.za). GCIS: "It is not an official government publication" (its consolidation) |
| [Information Regulator](https://inforegulator.org.za): Proc. R21 of 2020 (GG 43461) | POPIA commencement | No terms page found |
| [LawLibrary](https://lawlibrary.org.za) (Laws.Africa and AfricanLII), read **only** from Internet Archive captures | Gaps: wordings in force between amendments that no government source gives | CC BY-NC 4.0. Attribution: LawLibrary (lawlibrary.org.za). The site itself was not fetched: it answers automated readers with a challenge, its robots.txt sets `ai-input=no`, and its terms forbid scraping |
| [SAFLII](https://www.saflii.org) | Not used | |

The legal texts themselves: Copyright Act 98 of 1978, s. 12(8)(a): "No copyright shall subsist in official texts of a legislative, administrative or legal nature".

## Licence

- **The law itself.** Copyright Act 98 of 1978, s. 12(8)(a): "No copyright shall subsist in official texts of a legislative, administrative or legal nature". The words of the Acts in this repository are free of copyright.
- **justice.gov.za** (Department of Justice and Constitutional Development) terms: users "may view, copy, download to a local drive, print and distribute the content of this website, or any part thereof only for non-commercial informational or reference purposes"; commercial use needs written permission (webmaster@justice.gov.za); notice "©Department of Justice and Constitutional Development: ALL RIGHTS RESERVED".
- **gov.za** (GCIS) terms: the same wording; permission from electronic@gcis.gov.za; notice "© GCIS2018: ALL RIGHTS RESERVED". This covers gov.za and info.gov.za pages read through the Internet Archive.
- **LawLibrary** (lawlibrary.org.za, Laws.Africa and AfricanLII): CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/). Attribution: LawLibrary (lawlibrary.org.za). Used only through pinned Internet Archive captures, only where no government source gives a wording; every use is listed in `REPRODUCE.md`.
- Lexifina's own contributions (the arrangement of the history, commit messages, tables and tools) are dedicated to the public domain under CC0 1.0. Full text in `LICENSE`.
