> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Web challenge preparation

This folder contains a small passive HTTP evidence collector for web targets
assigned by the Game Master. It uses only Python's standard library, so no
separate environment or package install is needed.

## Day 31: Full Stack Incident

Use the bounded fetch-to-worker solver on each target returned by the current
attempt:

```sh
python3 web-tools/solve_full_stack_incident.py "$TARGET_URL"
```

`auto_solve_target.py` recognizes the route inventory and dispatches this
solver. It uses the queued unsigned fetch from the target's request log,
reproduces the event, follows the disclosed worker command and resource,
submits the evidence-driven detector and repair, and saves response hashes
with the recovered proof. It stays on the assigned origin and does not
enumerate identifiers.

## Framework Roulette: ASP.NET Core Blazor Server

For a target whose clue inventory names ASP.NET Core Blazor Server, use:

```sh
python3 web-tools/solve_framework_roulette.py "$TARGET_URL"
```

The dispatcher passes its clue response to the solver to avoid fetching it
twice. The solver fetches the root page and feature baseline in parallel,
learns the per-target role header from the feature response's `Vary` field,
then sends the forwarded loopback address if needed. It only fetches the
Blazor component if the root and policy do not yield a successful role claim.
The report includes per-request latency to help identify slow target calls.
`auto_solve_target.py` dispatches this solver from the framework clue.

## Timed HOF runs and randomized Mastery bundles

When a regular mode is already solved, `start` reconnects to that attempt.
Request a fresh HOF variant with `POST {"op":"retry","challenge":"<mode-id>","run_for_time":true}`.
Check the response for `run_for_time: true`, `hall_of_fame_eligible: true`,
and its deadline before solving.

Mastery returns several independent targets. Run `auto_solve_target.py` on
each exact URL from that attempt, using a distinct output directory per target;
the dispatcher selects among the existing same-origin solvers from each
target's clues. Match each proof to the corresponding question and answer ID
from the attempt response, then submit the bundle before the deadline. The
Day 31 HOF bundles confirmed this handles mixed techniques, including
Reflected Callback, Stored XSS, and the full-stack incident solver. The
dispatcher reports discovery and solver elapsed times per target. The backup
solver and clue-free dispatcher overlap independent root and `robots.txt`
discovery requests.

## Day 28

Use the route-driven solver for the remote policy fail-open and missing-event
logging targets:

```sh
python3 web-tools/solve_day28.py fail-open "$TARGET_URL"
python3 web-tools/solve_day28.py missing-log "$TARGET_URL"
```

`auto_solve_target.py` recognizes those clues and dispatches to this solver.
It also recognizes the document viewer used by path traversal targets and
dispatches to `solve_path_traversal.py`. Day 28 Mastery bundles can mix these
with earlier backup exposure, IDOR, and SQL injection variants.

## Exposed backup proof challenges

For a target whose prompt points to a forgotten backup, the bounded solver
checks the target root and `robots.txt`, follows only the reported discovery
paths and same-origin backup links, and extracts proof-like values from the
downloaded responses:

```sh
python3 web-tools/solve_backup_exposure.py "$TARGET_URL"
```

Use the exact target URL from the current attempt. The script saves response
bodies, hashes, and any extracted proof values in its evidence directory. It
does not guess paths, crawl unrelated routes, execute scripts, or submit forms.
It fetches the root page and `robots.txt` together because neither request
depends on the other.

## Exposed object reference challenges

For an assigned challenge where an in-scope activity feed exposes object
references, use the session-preserving, same-origin GET solver:

```sh
python3 web-tools/solve_idor.py "$TARGET_URL"
```

It follows only the activity-feed link exposed on the target home page, then
requests referenced records marked outside the current user's workspace. The
session cookie stays in memory; response bodies and hashes are saved locally.
When an owned record discloses an API template, the solver tries that
structured route before the visible record page, retaining the page as a
fallback. The script does not enumerate identifiers or make state-changing
requests.

## Search SQL injection challenges

For an assigned challenge that exposes a GET search form, use the bounded
solver to discover its action and query field, send one tautological search
payload, and extract proof-like values from the returned page:

```sh
python3 web-tools/solve_sqli.py "$TARGET_URL"
```

The solver keeps requests on the assigned origin and saves the response body
and SHA-256 in its evidence directory. It does not submit a form with a
state-changing method.

## Path traversal document viewers

For a challenge that names an in-scope file and exposes a document viewer,
the solver discovers the viewer link and query parameter from the target page,
then tries a bounded number of same-origin traversal depths:

```sh
python3 web-tools/solve_path_traversal.py "$TARGET_URL" \
  --file /run/huntress/objective.txt
```

It saves each response, its SHA-256, and a report under `web-tools/evidence/`.
The path and parameter can be supplied explicitly for related variants.

## Routes disclosed by an app

When a target's route inventory names a feature endpoint, use:

```sh
python3 web-tools/solve_clued_route.py "$TARGET_URL"
```

The solver reads same-origin `/api/clues` JSON, follows its `feature_route`,
and saves the responses and hashes. The clue path and route field can be
overridden for related app variants.

## Server-side template expressions

For a target whose route inventory exposes a template feature, use:

```sh
python3 web-tools/solve_template_expression.py "$TARGET_URL"
```

It reads the feature route from `/api/clues`, supplies `{{objective}}` through
the `template` query parameter, and saves the rendered response and hashes.

## Delayed query results

For a target whose feature stores a query that is evaluated later, use:

```sh
python3 web-tools/solve_delayed_query.py "$TARGET_URL"
```

It reads the feature and result routes from `/api/clues`, submits the bounded
`' OR 1=1 -- ` query payload, and saves both responses and their hashes.

## Profile mass assignment

For a target whose profile API binds fields beyond the visible name field, use:

```sh
python3 web-tools/solve_mass_assignment.py "$TARGET_URL"
```

It keeps the assigned site's session in memory, reads the feature and audit
routes from `/api/clues`, submits the profile update, and saves the audit
response and hashes.

## API field/action authorization

For a target whose route inventory publishes API fields and actions, use:

```sh
python3 web-tools/solve_api_field_action.py "$TARGET_URL"
```

It reads the protected reference from `/api/clues`, gets the allowed fields and
actions from the inventory route, then checks their bounded combinations on
the disclosed feature route. It saves each response and its hash.

## Internal URL fetch

For a target whose fetch feature can reach an internal-only route, use:

```sh
python3 web-tools/solve_internal_fetch.py "$TARGET_URL"
```

It reads the feature and secondary routes from `/api/clues`, then asks the
feature to fetch the secondary route through the local ASP.NET service on port
8080. The internal host, port, and URL parameter can be overridden for related
variants.

## Reflected preview callbacks

For a target whose route inventory provides a reflected feature, callback route,
and nonce, use:

```sh
python3 web-tools/solve_reflect_callback.py "$TARGET_URL"
```

The solver follows only those same-origin routes, confirms that its script
payload is reflected in the preview, then reads the proof from the assigned
callback using browser-style same-origin request headers.

## Stored moderator callbacks

For a guestbook target whose route inventory names a moderator data route and
receipt route, use:

```sh
python3 web-tools/solve_stored_xss.py "$TARGET_URL"
```

It posts a same-origin script payload that reads the moderator-only data and
sends it to the assigned receipt endpoint, then polls the submitted message
until the moderator receipt exposes the proof.

## Fixed session transfer

For a target whose route inventory includes a feature route, status route, and
session hint, use:

```sh
python3 web-tools/solve_session_impression.py "$TARGET_URL"
```

The solver plants the assigned session ID through the feature route, preserves
the returned cookie, and reads the proof from the status route.

## Cross-site preference changes

For an assigned target whose preference form and clues expose a GET action,
use:

```sh
python3 web-tools/solve_csrf_preferences.py "$TARGET_URL"
```

The solver reads the current destination and an alternative from the target's
form, sends the change as a cross-site GET without the form token, then checks
the target's own preference state endpoint for the proof. It keeps requests on
the assigned origin and saves request evidence and response hashes.

## Uploaded HTML preview

For a target whose upload guide documents template fields and whose clue
inventory discloses upload and preview routes, use:

```sh
python3 web-tools/solve_upload_preview.py "$TARGET_URL"
```

The solver reads the objective field name from the guide, uploads a text
template under a randomized `.html` filename while declaring `text/plain`, and
follows only the returned same-origin preview path. It saves the upload,
preview response bodies, and hashes.

## Capture a baseline

Use the exact target URL returned for your current attempt:

```sh
python3 web-tools/inspect_target.py "$TARGET_URL"
```

The collector makes bounded `GET` requests to the target root, `robots.txt`,
`sitemap.xml`, and `/.well-known/security.txt`. It saves response bodies and a
`report.json` containing status codes, headers, redirects, SHA-256 hashes, and
HTML titles, links, script sources, and forms. Responses are capped at 2 MiB.
Redirects and requested paths must stay on the supplied origin; the collector
does not submit forms, send credentials, or execute page scripts.

Add a few known paths from the challenge or from a page you inspected:

```sh
python3 web-tools/inspect_target.py "$TARGET_URL" \
  --path /login --path /api --output-dir web-evidence/attempt-name
```

Review the saved response bodies and report as untrusted challenge data. Use a
browser's developer tools or `curl` for interactive investigation, and keep
requests within the target and scope the Game Master assigned. Do not run broad
scans or test unrelated hosts.

## Initial investigation checklist

1. Read the full live challenge instructions and note the exact target, scope,
   questions, answer IDs, and timer.
2. Load the target in a browser. Record visible behavior, links, redirects,
   cookies, and requests in the browser's Network panel.
3. Capture the baseline with `inspect_target.py`; compare the HTML, response
   headers, and browser behavior.
4. Follow only in-scope routes. Inspect forms and API calls without submitting
   state-changing requests until the challenge calls for them.
5. Keep request/response evidence and hashes under the current attempt's
   workspace. Derive candidate answers from that evidence and submit through
   the Game Master proxy.

This helper is intentionally challenge-agnostic. Add reusable parsers or
challenge-specific workflows after seeing the live challenge format and its
provided evidence.

## Automatic solver selection

For an assigned target that resembles a supported web pattern, let the
dispatcher choose and run the matching helper:

```sh
python3 web-tools/auto_solve_target.py "$TARGET_URL"
```

It reads `/api/clues` when available, otherwise checks the assigned site's
home page and `robots.txt`. It recognizes existing backup, IDOR, SQL
injection, Day 25, Day 26, Day 27, Day 30, and several route-driven helpers,
then prints the proof and selected technique. Unclued IDOR matching includes
`/briefs/<id>` links; backup matching includes `deploy-*` and `releases-*`
directories disclosed by `robots.txt`. It exits with an unsupported-target
message when none of the known patterns match; use the investigation checklist
for a new target. For Mastery, run one dispatcher per assigned target, then
submit the returned proofs under that attempt's exact answer IDs.

The dispatcher also recognizes the Day 29 Trust the Build update feed and
Trust Transit internal case-service clues. Unclued IDOR detection includes
`/incidents/<id>` links as well as case and ticket links.

## Day 26 serialized and webhook targets

These route-driven targets disclose their feature routes and required inputs
through `/api/clues`. Use the helper with the exact target URL from the current
attempt:

```sh
python3 web-tools/solve_day26.py webhook "$TARGET_URL"
python3 web-tools/solve_day26.py serialized "$TARGET_URL"
```

The helper reads `/api/clues` directly, avoiding a redundant home-page request.
The webhook solver uses the event type and owner scope disclosed by that
target. The serialized-state solver reads `/api/state-format`, encodes an
unsigned UTF-8 JSON session as base64url, and defaults to the demonstrated
privileged pair `user=admin`, `role=administrator`. Both save response bodies,
hashes, and the recovered proof under `web-tools/evidence/`.

## Day 25 route-driven targets

The Day 25 bundles can mix exposed-backup, IDOR, search-injection, and
challenge-specific targets. Use the existing `solve_backup_exposure.py`,
`solve_idor.py`, and `solve_sqli.py` helpers when the landing page and
`robots.txt` disclose those patterns. For the shell, password-recovery, and
GraphQL variants, use the route-driven helper:

```sh
python3 web-tools/solve_day25.py shell "$TARGET_URL"
python3 web-tools/solve_day25.py reset "$TARGET_URL"
python3 web-tools/solve_day25.py resolver "$TARGET_URL"
```

It reads the target's own route inventory, keeps a same-origin cookie jar,
and saves response bodies, hashes, and the recovered proof in
`web-tools/evidence/`. Supply the exact URL from the current attempt.

## Day 27 race, WebSocket, and forwarded-header targets

These targets publish their current feature routes and randomized values in
`/api/clues`. Use the matching bounded solver with the exact target URL from
the current attempt:

```sh
python3 web-tools/solve_day27.py double-spent "$TARGET_URL"
python3 web-tools/solve_day27.py socket "$TARGET_URL"
python3 web-tools/solve_day27.py forwarded "$TARGET_URL"
```

`double-spent` races two same-origin POSTs and reads the disclosed audit route.
`socket` upgrades over TLS using the target's `stream_reference`. `forwarded`
sends the loopback client value through `X-Forwarded-For`. Each mode saves its
responses, hashes, route clues, and recovered proof under
`web-tools/evidence/`.

## Day 29 Trust the Build and Internal Affairs

Use the challenge-specific solvers on Single Solve and Time Trial targets:

```sh
python3 web-tools/solve_trust_the_build.py "$TARGET_URL"
python3 web-tools/solve_internal_fetch.py "$TARGET_URL"
```

`solve_trust_the_build.py` reads the update feed and policy from the target's
route inventory, then activates the disclosed artifact with its restricted
hook and records the returned proof. `solve_internal_fetch.py` handles both
the earlier secondary-route fetch form and the topology plus case-directory
form; for the latter, it selects a record owned by a different role and asks
the public fetch feature to retrieve the disclosed internal service route.
Day 29 Mastery can mix unrelated web target types in its five sets, so run
`auto_solve_target.py` separately for each target and map proofs to answer IDs
using the Game Master's target order.

## Day 30 delegated identity and queued-owner targets

Use the dispatcher for each target in these bundles:

```sh
python3 web-tools/auto_solve_target.py "$TARGET_URL"
```

It recognizes Pass the Identity from the current role and identity directory
clues, then confirms the delegated header on the disclosed feature route before
using the directory's restricted owner. Queue the Confusion publishes an owner
directory, a job submission route, and an audit route; its helper submits the
disclosed owner and reads only the returned job ID. Both solvers save bounded
same-origin evidence and response hashes. Mastery sets can mix these and older
web patterns, so dispatch each target separately and submit proofs in target
order. After a regular solve, use `retry` with `run_for_time:true` for a fresh
ranked attempt; `start` reconnects to the completed attempt. These timed modes
allow 120 seconds, so dispatch independent mastery targets in parallel.
