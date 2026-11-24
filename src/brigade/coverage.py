"""How much of the country an available set of fire engines can reach in time.

``travel_min[s][z]`` is the travel time in minutes from station ``s`` to demand zone ``z``,
and ``demand[z]`` is how many calls the zone produces (or its population). A zone is covered
when at least one *available* station reaches it within the target time; it has backup cover
when at least two do. Dispatch and move-up decisions in later sessions are judged by what they
do to these numbers.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _validate(
    travel_min: ArrayLike, demand: ArrayLike, available: ArrayLike | None
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.bool_]]:
    t = np.asarray(travel_min, dtype=np.float64)
    d = np.asarray(demand, dtype=np.float64)
    if t.ndim != 2:
        raise ValueError("travel times must be a stations x zones matrix")
    if d.shape != (t.shape[1],):
        raise ValueError("demand must have one entry per zone")
    if np.isnan(t).any() or (t < 0).any():
        raise ValueError("travel times must be non-negative (use inf for unreachable)")
    if not np.isfinite(d).all() or (d < 0).any():
        raise ValueError("demand must be finite and non-negative")
    a = np.ones(t.shape[0], dtype=bool) if available is None else np.asarray(available, dtype=bool)
    if a.shape != (t.shape[0],):
        raise ValueError("availability must have one entry per station")
    return t, d, a


def cover_counts(
    travel_min: ArrayLike,
    demand: ArrayLike,
    target_min: float,
    available: ArrayLike | None = None,
) -> NDArray[np.int64]:
    """Return, for each zone, how many available stations reach it within the target."""
    t, _, a = _validate(travel_min, demand, available)
    if target_min < 0:
        raise ValueError("target time cannot be negative")
    counts: NDArray[np.int64] = (t[a] <= target_min).sum(axis=0).astype(np.int64)
    return counts


def covered_share(
    travel_min: ArrayLike,
    demand: ArrayLike,
    target_min: float,
    available: ArrayLike | None = None,
    min_stations: int = 1,
) -> float:
    """Share of demand reached within the target by at least ``min_stations`` stations."""
    if min_stations < 1:
        raise ValueError("min_stations must be at least 1")
    counts = cover_counts(travel_min, demand, target_min, available)
    d = np.asarray(demand, dtype=np.float64)
    total = float(d.sum())
    if total == 0:
        return 1.0
    return float(d[counts >= min_stations].sum()) / total


def uncovered_zones(
    travel_min: ArrayLike,
    demand: ArrayLike,
    target_min: float,
    available: ArrayLike | None = None,
) -> list[int]:
    """Zones with demand that no available station reaches in time, busiest first."""
    counts = cover_counts(travel_min, demand, target_min, available)
    d = np.asarray(demand, dtype=np.float64)
    zones = [int(z) for z in np.flatnonzero((counts == 0) & (d > 0))]
    return sorted(zones, key=lambda z: (-d[z], z))
