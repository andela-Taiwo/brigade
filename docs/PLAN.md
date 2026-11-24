# Plan

Brigade is built in sessions, each with a clear success test. Later sessions build on
earlier ones. The hard parts run first, on a small hand-written country; the national-scale
generator comes once the engine is trusted.

## What keeps Brigade honest

Dispatch simulators are common. Two disciplines set this one apart, and every session keeps
them:

- **Exact checks.** Where theory gives an answer, the simulator must match it: a single station
  matches Erlang B and C; the move-up optimiser matches an exact optimiser on the toy country;
  the same seed gives a byte-identical event log.
- **Beat the baseline.** Every policy is run against nearest-engine dispatch on the same
  country, incidents and seeds, and reported side by side. No result is reported alone. If a
  policy does not beat the baseline, the report says so.

Every tie (equal event times, equal travel times, equal cover) is broken by a stated rule that
has a test and a written reason.

## Sessions

| # | Session | Success |
|---|---|---|
| 1 | Deterministic event engine on a toy country: simulated clock, event queue with stated tie-breaking, seeded incident arrivals, a full event log; a hand-written country of about a dozen stations and fifty zones with a fixed travel-time matrix | The same seed gives a byte-identical event log; changing the order events are inserted changes nothing; every tie-breaking rule has a test and a reason; time never goes backwards and every incident reaches an outcome |
| 2 | Nearest-engine dispatch and an independent rule checker: vehicle types per call type, queued calls when nothing is free, a checker that validates every dispatch from the event log without importing the engine | Every rule has a test that breaks it and is caught; for a single station, waits match Erlang C and losses match Erlang B within stated tolerances. This is the baseline for everything after |
| 3 | Cover-preserving dispatch and move-up: send a slightly further engine when the nearest would leave an area uncovered; move idle engines to fill gaps | On the toy country, move-up matches an exact optimiser; against the baseline on the same seeds, response-time percentiles and covered share are reported side by side |
| 4 | Disasters: multi-region scenarios, mutual aid, closed roads, crew shift limits and rest | No region lends its last cover; crews never exceed limits; the report shows who helped whom and the cost to the lender, next to the baseline |
| 5 | Synthetic country generator at national scale: regions, towns, roads, stations, vehicles and crews from a seed, with incident patterns by type, hour, day and season | Same seed gives an identical country; every zone is reachable; bad files list every error; the Erlang, optimiser and baseline results reproduce on generated countries |
| 6 | Live engine and web UI: clock, map, stations, engines, incidents, triggered scenarios and replay | Playwright covers triggering a flood scenario and watching mutual aid arrive, with the baseline comparison on screen |
| 7 | Scale: a country of 60 million people with about 1,500 stations, a 30-day disaster run, profiling and benchmarks | The large run finishes within a set budget; benchmarks fail the build on regression |

## Rules

- The toy country stays in the repo as a fixture. The hardest guarantees (determinism, the
  Erlang match, the optimiser against the exact answer) are always checked on it.
- The exact optimiser runs in a separate tool environment; `make check` never needs it.
- All randomness comes from named, seeded streams. Every run replays exactly.
- No learned or forecasting models. Incident rates come from the configuration.
- The country, its places and its people are made up.
