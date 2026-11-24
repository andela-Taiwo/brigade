# Brigade

Simulate a country's fire and rescue service through ordinary days and a nationwide disaster:
which engine goes to which call, how to keep every area covered while the busiest regions are
stretched, and when to send help across regional borders.

> **Status: foundation only.** The project layout, tooling, Erlang queueing formulas, a
> coverage measure and seeded random streams exist and are tested. The synthetic country,
> incidents, dispatch, move-up, mutual aid and the web UI are not built yet. See
> [the plan](docs/PLAN.md).

## What it will do

- **A synthetic country**: regions, towns, fire stations, engines and specialist vehicles
  (aerial ladders, water carriers, rescue units), crews on shifts, and a road network with
  travel times.
- **Incidents**: everyday calls with realistic daily and weekly patterns, and disaster scenarios
  (widespread flooding, a heatwave with many grass and forest fires, a storm closing roads) that
  hit several regions at once.
- **Dispatch**: send the right vehicles to each call under clear, checked rules, and compare
  policies: nearest engine, cover-preserving dispatch, and moving idle engines to fill gaps.
- **Mutual aid**: when a region runs out, borrow engines from neighbours without leaving their
  own areas uncovered.
- **Crews**: shift limits and rest after long incidents, so the service does not run on
  exhausted crews.
- **Live view**: a map of stations, engines and incidents, scenarios you can trigger, and a
  timeline you can replay.

All randomness comes from a seed, so every run replays exactly. The country is made up.

## What exists today

| Module | What it does |
|---|---|
| `brigade.queueing` | Erlang B and C, mean wait in an M/M/c queue, and the fewest servers for a target |
| `brigade.coverage` | Share of demand an available set of stations reaches in time, backup cover, and uncovered zones |
| `brigade.rng` | Named, independent random streams from one run seed |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
make setup   # install locked dependencies
make check   # lint, format check, type check and tests
make help    # list every target
```

## Layout

```
src/brigade/   # the simulator package
tests/         # unit and property tests
docs/PLAN.md   # what is being built, in order
docs/adr/      # architecture decision records
```

## Licence

MIT. See [LICENSE](LICENSE).
