# Brigade

Simulate a country's fire and rescue service through ordinary days and a nationwide disaster:
which engine goes to which call, how to keep every area covered while the busiest regions are
stretched, and when to send help across regional borders.

> **Status: foundation only.** The project layout, tooling, Erlang queueing formulas, a
> coverage measure and seeded random streams exist and are tested. The event engine,
> dispatch, move-up, mutual aid, the country generator and the web UI are not built yet. See
> [the plan](docs/PLAN.md).

## What it will do

- **A deterministic event engine**: a simulated clock, incidents arriving at random from a
  seed, and a full event log. The same seed always gives the same log, byte for byte.
- **Dispatch, checked**: nearest-engine dispatch as the baseline, and an independent checker
  that validates every dispatch from the log. For a single station, waits and losses match
  Erlang's formulas.
- **Keeping cover**: send a slightly further engine when the nearest one would leave an area
  uncovered, and move idle engines to fill gaps. Checked against an exact optimiser on a small
  country, and always reported next to the nearest-engine baseline on the same seeds.
- **Disasters**: floods, heatwave fires or storms hitting several regions at once, with mutual
  aid between regions, closed roads, and crew shift limits.
- **A whole country**: a seeded generator for a made-up country at national scale.
- **Live view**: a map of stations, engines and incidents, scenarios you can trigger, and a
  timeline you can replay.

Two rules run through all of it: where theory gives an exact answer, the simulator must match
it; and no policy is ever reported without the baseline beside it. The country is made up.

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
