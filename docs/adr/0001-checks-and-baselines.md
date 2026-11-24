# 0001: How results are checked

## Status

Accepted

## Context

There is no industry-standard fire response simulator to compare against, and a dispatch
policy can look sensible on a map while being worse than the simplest rule. Brigade needs
checks that do not depend on trusting its own code.

## Decision

Three kinds of check, from exact to comparative:

- **Closed forms.** For one station with random calls and fixed engine counts, the simulator
  must match Erlang B and C (`brigade.queueing`) within a stated tolerance.
- **Exact optimisers on small cases.** Where to place or move engines is a covering problem.
  On small instances an exact solver, run in a separate tool environment, gives the best
  possible cover; Brigade's heuristics are measured against it.
- **Baselines on the same seeds.** Every policy is compared with nearest-engine dispatch on
  the same country, the same incidents and the same random streams, and results are reported
  side by side, never alone.

An independent rule checker reads the event log and validates every dispatch. It never imports
the dispatch engine.

These checks run first on a small hand-written country kept as a fixture, before the
national-scale generator exists, so the engine is trusted before it is scaled.

## Consequences

- A claim that a policy is better always comes with the baseline and the seeds it was run on.
- Statistical checks need many seeded runs; slow ones are marked so `make check` stays fast.
