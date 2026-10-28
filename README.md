# South African Constitution: the history in git

The Constitution of the Republic of South Africa, 1996, as a git repository. Each commit is an amending act taking
effect, dated the day it took effect, so `git log`, `git blame` and `git diff` answer a lawyer's questions about what
the Constitution said on a given day and which act wrote its words. One file per provision (`constitution/section-169.md`,
`constitution/schedule-1a.md`), one paragraph per line.

**The record starts on 2 April 2009.** That first commit is a baseline: the text in force that day, which no official
source publishes. It is derived from the Department of Justice's current consolidation by undoing the three amending
acts that took effect since. The fifteen amendments before 2009 are in the baseline's text but not in the history (see
"What it does not show").

| Commit date | Author | Change |
|---|---|---|
| 2009-04-02 | Department of Justice and Constitutional Development (consolidation) | baseline |
| 2009-04-03 | Constitution Sixteenth Amendment Act of 2009 | Schedule 1A (Merafong City moves to Gauteng) |
| 2013-08-23 | Constitution Seventeenth Amendment Act of 2012 | ss. 165-170, 172, 173, 175, 178: Chief Justice heads the judiciary, a single High Court of South Africa |
| 2026-06-26 | Constitution Eighteenth Amendment Act, 2023 (Act 3 of 2023) | s. 6: South African Sign Language becomes an official language |

## Questions and the commands that answer them

| Question | Command |
|---|---|
| What did s. 169 say on 22 August 2013? | `python tools/zalaw.py 2013-08-22 constitution 169` |
| The whole Constitution on 1 July 2026 | `python tools/zalaw.py 2026-07-01 constitution` |
| When did s. 6 change, and by which act? | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- constitution/section-006.md` |
| Which act wrote each line of s. 175? | `git blame constitution/section-175.md` |
| Which words changed? | `git log -p --word-diff constitution/section-169.md` |
| Everything the Seventeenth Amendment changed | `git show --stat constitution/2013-08-23` |
| The text in force on a day, raw git (bash) | `git show $(git rev-list -1 --before="2013-08-22T23:59:59+02:00" main):constitution/section-169.md` |
| The same in PowerShell | `$r = git rev-list -1 --before="2013-08-22T23:59:59+02:00" main; git show "$($r):constitution/section-169.md"` |

Give `--before` a full time and zone as above: a bare date is read at the current time of day in your own zone. The
tool reads the `In-force:` trailer instead and is independent of both. Tags `constitution/<date>` mark each state.
After this repository is rebuilt, existing clones need `git fetch --force --tags` (git does not move existing tags).

## Dates

- The commit date (author and committer) is the day the act took effect, at 12:00 South African Standard Time
  (UTC+2, no summer time), so the day reads the same in every zone. It is repeated in the `In-force:` trailer.
- Other dates are trailers: `Assented:` (the President's assent), `Published:` (the Government Gazette),
  `Commencement:` (the proclamation that fixed the day). All three acts came into operation on a day fixed by the
  President by proclamation. The Eighteenth Amendment was assented to on 19 July 2023 but took effect only on 26 June
  2026 (Proclamation Notice 321 of 2026, "with immediate effect").
- The baseline carries `Consolidated: 2026-05-07`, the "text as at" date of the consolidation it was derived from.
- The two documentation commits are dated 2026-10-28, the day the sources were retrieved.

## What "author" means

The author of a law commit is the amending act, at an address that cannot exist
(`constitution-seventeenth-amendment-2012@gazette.invalid`), so `git blame` names the act that wrote each line. The
committer is always Lexifina. The baseline's author is the publisher of the consolidation it was derived from: its
lines were written by the 1996 Constitution or by one of the fifteen amendments before 2009, and blame cannot tell
which. Blame credits whole paragraphs; use `--word-diff` to see the words an act changed.

## How the history was made, and how it is checked

1. **Today's text**: the Department of Justice and Constitutional Development's consolidation
   (https://www.justice.gov.za/constitution/), sections from the chapter pages, the Schedules and Annexures from the
   combined Schedules PDF. The Department's editorial notes ("[Sub-s. (3) substituted by ...]") are not law text and are
   left out.
2. **Undoing the acts**: South African amending acts print the words they remove in bold square brackets and the
   words they insert underlined. Both survive in the born-digital PDFs of the three acts (brackets as characters,
   underlines as drawn lines), so each change can be read in both directions from the act itself.
3. **Checking the old text**: the consolidation had not yet applied the Eighteenth Amendment, so the old text of s. 6
   was compared with it directly: identical. The old text of every provision the Seventeenth replaced was compared,
   letter for letter and comma for comma, with Juta's 2003 consolidation (a scanned copy on gov.za: those provisions
   did not change between 2003 and 2013). Where the Government Printer's markup turned out to be incomplete, the old
   text was corrected to the 2003 text; every correction, with its reason, is in `data/derivation.json`:
- Seventeenth Amendment of 2012, s. 3(a) (section-167.md): the Printer underlines "Republic;" whole, so the markup drops the semicolon the old text had.
- Seventeenth Amendment of 2012, s. 3(b) (section-167.md): the Printer underlines "Africa," whole, so the markup drops the comma the old text had.
- Seventeenth Amendment of 2012, s. 4 (section-168.md): the act prints the new subsection (3) without marking the words it removes ("It is the highest court of appeal except in constitutional matters") or the renumbering of (a)-(c); the old subsection is read from the 2003 consolidation.
- Seventeenth Amendment of 2012, s. 5 (section-169.md): the act underlines only the first line of the new subsection (2) and none of (3), and underlines "167(6)(a);" and "Africa;" whole; the old section ends at paragraph (b).
- Seventeenth Amendment of 2012, s. 9 (section-175.md): the act does not bracket the "a" it removes before "man", and keeps the comma that the inserted words need where the old text had a full stop.
- Seventeenth Amendment of 2012, s. 10 (section-178.md): the Printer underlines "Africa," whole, so the markup drops the comma the old text had.
4. **Redoing the acts**: each commit applies the act's new words as the act prints them.
5. **Check** (`check_repo.py`, in the build folder): every file of the last commit before the Eighteenth Amendment
   equals the consolidation, byte for byte and word for word, except the words listed below; the last commit equals it
   except s. 6, which the consolidation has not yet amended. Every change is checked on its day: the act's new words
   are in the file on the day it took effect and its old words the day before.

### Where the Department's consolidation differs from the act

The consolidation prints these words differently from the act that wrote them. This record follows the act:

| File | Act | The act reads | The consolidation reads |
|---|---|---|---|
| constitution/section-167.md | Constitution Seventeenth Amendment Act of 2012 | that Court; and | that Court, and |
| constitution/section-168.md | Constitution Seventeenth Amendment Act of 2012 | such extent | such an extent |
| constitution/section-169.md | Constitution Seventeenth Amendment Act of 2012 | or more | or two more |
| constitution/section-169.md | Constitution Seventeenth Amendment Act of 2012 | seat within a | seat with a |
| constitution/section-175.md | Constitution Seventeenth Amendment Act of 2012 | or man | or a man |
| constitution/section-175.md | Constitution Seventeenth Amendment Act of 2012 | those offices, or | those offices , or |

## What it does not show

- **Anything before 2 April 2009.** The 1996 Constitution and the fifteen amendments of 1997-2008 are published only
  as page scans with an unreliable text layer, so their changes are part of the baseline, not separate commits.
- **Laws that change the law without changing the text**: proclamations transferring functions under s. 97, national
  legislation the Constitution calls for, and court orders (for example declarations of invalidity) are not here.
- **Other languages.** The text is English. The signed text of each of these acts is English.
- **Layout.** Tables in Schedules 6 and 7 are flattened into lines. Schedules 6A and 6B were repealed before 2009
  and appear only as headings, as in the consolidation.

## How it is built

`scripts/south-africa-law/build.py` in the Lexifina repository (a copy of its blob hashes and every command is in
REPRODUCE.md). It fetches each source once through a cache, at most four requests at a time, then streams the commits
into `git fast-import`. Two builds from the same data give the same commit hashes. No model runs at build time. The
AI agent that wrote the builder typed the six corrections listed above from the 2003 scan; code checks each against
that scan on every build (REPRODUCE.md).

## Licence

The law has no copyright in South Africa (Copyright Act 98 of 1978, s. 12(8)(a)). The source sites allow copying for
non-commercial informational or reference purposes. See LICENSE for the exact terms and attribution.
