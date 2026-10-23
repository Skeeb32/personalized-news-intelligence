# Daily operating guide

## Preparation

Choose a local time zone and research cutoff. Start research early enough to aim for a 6:00 AM edition. Read previous editions and `history/coverage.csv`. A missing record means historical coverage is unknown, not that a story is new.

## Research and verification

1. Search current technology news across the sectors in the master prompt. Prefer original announcements, papers, filings, and government sources. Seek independent corroboration for material claims where practical.
2. Rank five distinct events by business impact, career implications, financial implications, industry transformation, professional relevance, and strength of evidence. Record uncertainty and disagreements.
3. Open each job's specific official listing or reputable ATS page. Record title, company, location, work arrangement, disclosed salary if any, verification date, and observed application status. An HTTP success code alone is not proof a job is open. Report fewer than ten with a limitation if necessary.
4. Verify speakers, their relevant roles at the time, exact wording, source context, and philosophical attribution. Use clearly identified paraphrases when original wording cannot be established.
5. Draft all seven sections using the template. Separate supporting research from the concise LinkedIn post. Apply the no-dash rule only to the post; preserve original quotations and URLs in notes.
6. Check evidence, dates, links, duplication, and personal claims manually. Run the post validator. Append verified coverage to the ledger only when the edition is finalized.

## Publication

Review the complete post and target account. This repository does not publish to LinkedIn. Copy the approved post into LinkedIn manually. Record the actual public post URL and timestamp only after successful publication. Do not label a draft as published.

If adding an integration later, require account-specific authorization, protect credentials in the runner's secret store, retain a draft review step, and record platform confirmation. Never expose tokens in this public repository.

## Scheduling

No schedule is active in this repository. Configure a timezone-aware external runner only after selecting a research provider, budget, credentials, and persistent storage. The runner must have web access; a timer alone cannot research or verify an edition. Local daylight saving time and delayed runs must be handled explicitly. If the runner fails or cannot verify enough information, report the limitation rather than filling gaps with invented content.

## Validator smoke checks

Run `python3 scripts/validate_post.py path/to/post.txt` with Python 3.9 or newer. Plain prose should exit 0; a hyphen, em dash, empty file, or unreadable file should exit 1. Review the reported line and column. The validator never rewrites quotations or URLs.
