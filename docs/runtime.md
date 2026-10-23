# Runtime guide

Python 3.9 or newer; no third-party packages required. Run commands from the repository root.

## Collect without an API key

```sh
python3 -m newsintel collect
```

Reads `config.json`, collects recent RSS/Atom items and current official Greenhouse listings concurrently, removes tracking parameters and duplicate URLs, filters roles and locations, and saves a dated `private/runs/YYYY-MM-DD/candidates.json`. Source failures are recorded independently. Missing dates are excluded from recent news. Feed candidates are not verified news claims; ATS publication is not proof that an application page accepts submissions.

Adjust `feeds`, `greenhouse_boards`, `job_keywords`, `locations`, `lookback_hours`, `timezone` and `profile` in your own config. Empty locations allows every location. The included profile is a generic topic configuration, not a claim about the operator's background. Treat feed URLs as trusted administrator configuration. Do not expose this CLI as an unauthenticated URL fetching service.

On macOS, if Python cannot locate its certificate bundle, configure a trusted CA bundle, for example `SSL_CERT_FILE=/etc/ssl/cert.pem` when that system bundle is available. Never disable certificate verification.

## AI-assisted research and drafting

Export `OPENAI_API_KEY` and `OPENAI_MODEL` in your shell using a model available to your account that supports Responses API web search. Do not paste secrets into GitHub. `.env.example` is documentation only; `.env` is not automatically loaded.

```sh
python3 -m newsintel run
```

The runner sends the master instructions, candidate packet, configured profile and last fourteen finalized editions to OpenAI, requests live web research, and locally validates the returned JSON. This incurs API and search usage charges. It makes one bounded request, with a 240 second timeout and 12,000 output token cap; it does not retry billable calls automatically. Credentials are sent only to the fixed OpenAI API endpoint. The model is deliberately configurable rather than hardcoded.

The response remains an unapproved draft. Format checks cannot establish that a quotation is authentic, that claims are true, or that a job page is accepting applications. A human must review evidence, originality and relevance. The collector does not infer salary or remote work status from incomplete data.

## Bring your own editorial input

Use `editorial.example.json` as the JSON contract. It contains fictional format examples, not a usable edition. Replace all fields with researched content and copy selected job identifiers and core fields exactly from the candidate packet.

```sh
python3 -m newsintel run --packet private/runs/YYYY-MM-DD/candidates.json --editorial private/editorial.json
```

Five distinct developments are required. Impact scores are six integers from zero to five, in this order: business, career, financial, transformation, professional relevance, evidence strength. Rendering ranks by total score. Jobs must match collected records; at most ten are accepted, and fewer requires an explanation. Each selected application page must have an explicit researcher verification note. Sources must be HTTP(S) URLs. The full draft must have sourced perspectives, a philosophical closing and a LinkedIn post without dash punctuation.

Outputs: `candidates.json`, `editorial.json`, `validation.json`, `briefing.md`, and `linkedin.txt`. Failed drafts retain their validation report but do not generate a new briefing. Run with a separate `--output` directory when preserving alternative drafts.

## Review and persistent history

Set `review.approved` to `true` and `review.reviewer` to your name only after checking the edition. Then:

```sh
python3 -m newsintel finalize --packet private/runs/YYYY-MM-DD/candidates.json --editorial private/editorial.json
```

Finalization inserts the edition into `private/history.sqlite`. The date is unique, so accidental duplicate finalization is rejected. Previously covered event IDs require `update_reason`. Semantic event identity and the significance of an update still need editorial judgment. Collection packets expire after 24 hours. Finalized means reviewed and recorded, not published to LinkedIn. Copy the reviewed post manually; no publishing endpoint exists.

Keep `private/` on persistent storage and back it up. `--state`, `--output`, `--config`, `--packet` and `--editorial` allow explicit paths. Private history never commits automatically.

## Scheduling

No recurring schedule is installed automatically. The included GitHub workflow is manual collection only: Actions → Collect research candidates → Run workflow. Its artifacts contain public candidate material; never add private profile details to a public workflow. Tests run on pushes and pull requests.

For recurring research, run `python3 -m newsintel run` using your existing timezone-aware scheduler with the repository as its working directory and persistent state storage. Start before 6:00 AM if that is the desired completion time; API latency cannot guarantee exact delivery. Configure secrets in the scheduler, prevent overlapping runs, and report nonzero exits. A GitHub hosted runner's temporary disk alone will not preserve review history across runs.

## Sources for integrations

* [Greenhouse Job Board API](https://docs.greenhouse.io/job-board.html)
* [OpenAI web search](https://developers.openai.com/api/docs/guides/tools-web-search)

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Tests cover draft rendering through finalization, review gating, duplicate events, URL normalization, recency filtering, fabricated job rejection, punctuation rules, and partial source failures. Tests use fictional data and make no API calls.
