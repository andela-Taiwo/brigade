# Plan

Brigade is built in sessions, each with a clear success test. Later sessions build on
earlier ones.

| # | Session | Success |
|---|---|---|
| 1 | Synthetic country: regions, towns and demand zones, a road network with travel times, stations, vehicles by type and crews, from a seeded configuration, with validation | Same seed gives an identical country; every zone is reachable; a bad file lists every error with its location; summary numbers fall in configured ranges |
| 2 | Incidents: everyday calls by type with daily, weekly and seasonal patterns, how long each type commits each vehicle, and disaster scenarios across several regions | Generated call counts and durations match the configured rates statistically; scenarios replay exactly; a scenario file with errors lists every one |
| 3 | Dispatch engine and an independent rule checker: the right vehicle types for each call, nearest available first, queued calls, and a full event log | Every rule has a test that breaks it and is caught by the checker; for one station with random calls, the share of calls that wait matches Erlang C within a stated tolerance |
| 4 | Cover-preserving dispatch and move-up: send a slightly further engine when the nearest one would leave an area uncovered; move idle engines to fill gaps | On the same seeds, compared with nearest-engine dispatch: response-time percentiles and covered share reported side by side; on small cases move-up matches an exact optimiser |
| 5 | Disasters at scale: mutual aid between regions, closed roads, crew shift limits and rest | In each scenario, no region lends its last cover; crews never exceed shift limits; the report shows who helped whom and the cost to the lender |
| 6 | Live engine and web UI: clock, map, stations, engines, incidents, triggered scenarios and replay | Playwright covers triggering a flood scenario and watching mutual aid arrive |
| 7 | Scale: a country of 60 million people with about 1,500 stations, a 30-day disaster run, profiling and benchmarks | The large run finishes within a set budget; benchmarks fail the build on regression |

## Rules

- The checks are closed-form queueing results (Erlang) in the simple cases, an exact optimiser
  on small cover problems, and a nearest-engine baseline on the same seeds for everything else.
- All randomness comes from named, seeded streams. Every run replays exactly.
- No learned or forecasting models. Incident rates come from the configuration.
- The country, its places and its people are made up.
