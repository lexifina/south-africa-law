# South Africa: law history in git

The law of South Africa as a git history: one file per provision (section or schedule), one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a section; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is South Africa's national law, which global-law reads at `south-africa/national/acts/`.

**What is in it now:** 195 acts with 229 versions: the Constitution of 1996 (21 versions, from 1997 to the Eighteenth Amendment in force on 26 June 2026), the Protection of Personal Information Act 4 of 2013 (7) and the Companies Act 71 of 2008 (9), each from its commencement through every amendment; 10 more Acts in the Department of Justice's current consolidation (the Criminal Procedure Act, the Promotion of Access to Information Act and others); and 182 principal Acts as enacted, from the Government Gazette on gov.za. [`REPRODUCE.md`](REPRODUCE.md) lists every act with its versions and the decisions made by hand; [`data/laws.csv`](data/laws.csv) lists the 366 laws the record names, with their dates and commits.

Each act is a folder `act/<year>/<number>/` with one file per provision and a `README.md` listing them (`act/2008/71/section-001.md` is section 1 of the Companies Act; `act/1995/66/` is the Labour Relations Act 66 of 1995, as enacted); the Constitution is in `constitution/constitution/`. `data/paths.json` maps each act id to its folder (12 folders keep a name in place of the number; before 11 November 2026 every folder was named by the id).

The text is in English, as the sources publish it; where the Gazette prints an Act in two languages, only the English pages are kept. Amendment notes are left out of the text and used only to credit changes.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to section 178 of the Constitution | `git log -p --word-diff --follow -- constitution/constitution/section-178.md` |
| Which law wrote each line of section 178? | `git blame constitution/constitution/section-178.md` |
| Every version of the Constitution, with the day each took effect | `git log --diff-filter=AMD --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- constitution ':!*/README.md'` |
| Section 178 as in force on 1 January 2005 | `python tools/on.py 2005-01-01 constitution section-178` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about South African law](https://global-law.lexifina.com/v1/try_claude?country=south-africa)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=south-africa)**: the same question in ChatGPT.
- **[Call the API in your browser](https://global-law.lexifina.com/v1/search_law?query=personal+information&jurisdictions=south-africa)**: a search of South African law for "personal information", returned as JSON. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add south-africa/national/acts
python3 tools/law.py show 2026-01-01 south-africa/national/acts/constitution/constitution/section-178.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Africa/Johannesburg, on the day the change took effect, and carries it in its `In-force:` trailer; the days enacted and published are trailers too:

- by default, Constitution s. 81: an Act "takes effect when published or on a date determined in terms of the Act", so an amendment with no commencement clause is dated by its publication in the Government Gazette, and one brought into force by proclamation by the proclamation; the Department of Justice's list of amendments, the Acts' own clauses and the proclamations give the days;
- a provision commenced in stages appears in its file on the day it commences (the Constitution in 1997 and 1998; POPIA on 11 April 2014, 1 July 2020 and 30 June 2021); the First Amendment, deemed in force from 4 February 1997, is dated that day;
- the 10 Department of Justice consolidations are dated by the latest "with effect from" day in each Act's amendment table; the Acts as enacted by the day the Gazette published them (the Global Minimum Tax Act 46 of 2024 by the retrospective commencement its s. 25(2) gives, 1 January 2024).

Each change is credited to the law the sources' amendment notes name (`Seventeenth Amendment (2012)`, `Act 16 of 2024`), with an address that cannot exist (`c17-2012@gov-za.invalid`); a proclamation that brings provisions into force is a commit of its own that changes no words. The Acts as enacted are credited to themselves; the 10 consolidations are the oldest version available, credited to the Department of Justice and Constitutional Development.

## How it is checked

- `tools/check_repo.py` reads every version back from git on the day it took effect and on the day before, and compares it with the corpus: 229 versions of 195 acts, 0 mismatches (see [`REPRODUCE.md`](REPRODUCE.md)).
- Today's text matches the Department of Justice consolidations word for word in all 253 provisions of the Constitution, 114 of POPIA's 115 sections and 228 of the Companies Act's 230 sections and schedules; in the three others the consolidation departs from the gazette without an amendment, and the gazette is kept.
- An Act from gov.za is published only if the letters and digits of its text equal those a second PDF reader gives for the same pages.
- History is append-only: no merge commits, no commit dated in the future, and every commit's trailers parse.

## What it does not show

- **Later changes to most Acts.** The 182 Acts from gov.za are their text as enacted: amendments, repeals and commencement by proclamation are not tracked, so an Act here may since have been amended or repealed. The 10 consolidations give only today's text.
- **Scanned Acts.** Gazettes without a clean text layer are left out (no OCR is used), and amending, appropriation and revenue Acts are not separate acts.
- **Some past wordings.** Where no clean source gives the wording in force, the file reads "[The source does not give the text in force on this date.]" for that period: the Constitution's Schedule 6 item 26 (1998 to 2001) and Schedule 6A (2002 to 2003), and ss. 5, 69, 116 and six definitions in s. 1 of the Companies Act (2011 to 2013). Provisions of Act 16 of 2024 not yet in operation are not shown.
- **Headings.** Chapter and Part headings are not files; each Schedule is one file.
- **Regulations, provincial law and case law** are not here; a declaration of invalidity by the Constitutional Court is not a commit unless an amendment Act changed the words.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Department of Justice and Constitutional Development](https://www.justice.gov.za) | Consolidated Acts; list of the Constitution's amendments; amendment Acts and proclamations | the current consolidation | Today's text of the Constitution, the Companies Act and 10 other Acts; the dates of amendments |
| [gov.za](https://www.gov.za/documents/acts) (GCIS) | Acts as published in the Government Gazette; the Constitution's 1996 text and consolidations of 1999 to 2012 | as enacted; the Constitution's as archived | The Acts as enacted, POPIA's and the Companies Act's text; older pages read through the Internet Archive |
| [Information Regulator](https://inforegulator.org.za) | Proc. R21 of 2020 | – | POPIA's commencement |
| [LawLibrary](https://lawlibrary.org.za) (Laws.Africa and AfricanLII) | Point-in-time texts, read only from [Internet Archive](https://web.archive.org/) captures | yes | Only where no government source gives a wording; every use is listed in `REPRODUCE.md` |

## Licence

See [`LICENSE`](LICENSE). Under the Copyright Act 98 of 1978, s. 12(8)(a), "No copyright shall subsist in official texts of a legislative, administrative or legal nature"; the terms of justice.gov.za and gov.za allow their content to be copied and distributed for non-commercial informational or reference purposes, and LawLibrary's content is CC BY-NC 4.0 (attribution: LawLibrary, lawlibrary.org.za). Lexifina's arrangement, commit messages, tables and tools are CC0 1.0.

No model wrote, translated or corrected legal text, and no model runs at build time; the scripts that read the sources and build this repository were written by an AI model (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
