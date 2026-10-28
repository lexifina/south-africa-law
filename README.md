# South Africa: law history

This repository will hold the legislation of South Africa (ZA) as a history: one file per provision and one commit per law taking effect, dated by the day it took force, with the law that made each change as the commit author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `za/` in the world tree.

**Status:** no law yet. This first commit records where the law of South Africa can be read and what a build would need.

**Can it be built?** Ready to build: an official source has past versions by date and an API or bulk download.

**This commit is a placeholder.** The first real build must replace this history from scratch and force-push. It must never append law commits on top of it: they are dated by when each law took effect, often decades earlier, so dates in `main` would run backwards and break every on-date lookup. Builders should refuse to append when the root commit is this placeholder (its subject ends "sources, before any law").

**Official sources**

- [SAFLII](https://www.saflii.org)
- [Laws.Africa](https://laws.africa): Content API at api.laws.africa/v3 with point-in-time versions and amendment metadata. The full legislation API is paid (from ZAR 42,000 per country per month); the free sandbox covers Cape Town by-laws. Content licence not confirmed as CC BY.
- [Acts (gov.za)](https://www.gov.za/documents/acts): Acts as passed. Consolidated, dated versions come from Laws.Africa and SAFLII.

All sources, with their status, are in [SOURCES.md](SOURCES.md). How these files were made is in [REPRODUCE.md](REPRODUCE.md).

This repository describes sources; it is not legal advice and holds no legal text yet.
