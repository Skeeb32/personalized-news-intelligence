# Personalized News Intelligence

An evidence-first workflow for daily technology research, career discovery, and thoughtful LinkedIn writing.

## What is included

* The complete research and editorial instructions in [the master prompt](prompts/daily-intelligence.txt).
* A seven-part [daily edition template](templates/edition.md).
* A [source and coverage ledger](history/coverage.csv) to support fact checking and avoid repetition.
* A dependency-free Python validator for the LinkedIn post's strict punctuation rules.
* A practical [operating guide](docs/workflow.md) for research, review, and manual publication.

## Quick start

1. Give a research assistant with current web access the master prompt and your role, location, interests, and recent editions. Keep private career preferences outside this public repository.
2. Copy `templates/edition.md` to `editions/YYYY-MM-DD.md` and research the day's developments. Select exactly five supported stories and aim for ten verified jobs. Disclose any shortfall rather than inventing entries.
3. Save the final LinkedIn text separately as `editions/YYYY-MM-DD.linkedin.txt`.
4. Run `python3 scripts/validate_post.py editions/YYYY-MM-DD.linkedin.txt`.
5. Complete the human publishing checklist, record covered stories and job URLs in the ledger, and publish manually after reviewing the full post.

## Project status

This is a research workflow and editorial toolkit, not an autonomous news service. No daily edition has been researched or published by installing this repository. There are no API keys, paid services, LinkedIn integrations, or active daily schedules included.

The target delivery time is 6:00 AM in the operator's local time zone. Scheduling requires a separately configured research runner with current web access and persistent history. See the operating guide before enabling automation.

## Editorial principles

Verify material facts, link original evidence, separate interpretation from fact, and preserve exact quotations in research notes. Include publication and event dates. Never invent jobs, salaries, quotes, personal experience, or publishing success.

The final LinkedIn post must contain no hyphens or dash punctuation, including in URLs and hashtags. Do not modify a source URL or a direct quotation to make it pass: move it to the companion research notes, or use a clearly labeled paraphrase where appropriate. Only reference companion resources that actually exist.

The validator checks text formatting only. A passing result does not verify facts, links, job availability, quotations, originality, or permission to publish.

## Contributing

Keep changes focused, document editorial behavior changes, and run the validator smoke checks described in `docs/workflow.md`. Never commit credentials, resumes, private messages, or personal application details.
