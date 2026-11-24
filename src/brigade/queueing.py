"""Erlang queueing formulas for fire stations and control rooms.

A station with ``c`` engines and calls arriving at random behaves, to a first approximation,
like an M/M/c queue. These closed forms give the share of calls that find every engine busy,
and how long a call waits for one. The simulator must reproduce them in the simple cases
where they apply, before it is trusted in the cases where they do not.

Load is in erlangs: arrival rate times mean time an engine is committed to a call.
"""

from __future__ import annotations


def _check(load_erlangs: float, servers: int) -> None:
    if load_erlangs < 0:
        raise ValueError("load cannot be negative")
    if servers < 1:
        raise ValueError("there must be at least one server")


def erlang_b(load_erlangs: float, servers: int) -> float:
    """Probability that a call finds all ``servers`` busy when blocked calls are lost.

    Uses the stable recursion B(k) = A B(k-1) / (k + A B(k-1)), B(0) = 1.
    """
    _check(load_erlangs, servers)
    b = 1.0
    for k in range(1, servers + 1):
        b = load_erlangs * b / (k + load_erlangs * b)
    return b


def erlang_c(load_erlangs: float, servers: int) -> float:
    """Probability that a call has to wait when calls queue for the next free server."""
    _check(load_erlangs, servers)
    if load_erlangs >= servers:
        raise ValueError(
            f"load {load_erlangs:g} erlangs needs more than {servers} servers to be stable"
        )
    b = erlang_b(load_erlangs, servers)
    return servers * b / (servers - load_erlangs * (1.0 - b))


def mean_wait(arrivals_per_hour: float, mean_service_hours: float, servers: int) -> float:
    """Mean time a call waits for a free server, in hours (M/M/c)."""
    if arrivals_per_hour < 0 or mean_service_hours <= 0:
        raise ValueError("arrival rate must be non-negative and service time positive")
    load = arrivals_per_hour * mean_service_hours
    if load == 0:
        return 0.0
    service_rate = 1.0 / mean_service_hours
    return erlang_c(load, servers) / (servers * service_rate - arrivals_per_hour)


def servers_needed(load_erlangs: float, max_wait_probability: float) -> int:
    """Fewest servers for which the chance of waiting is at most ``max_wait_probability``."""
    if not 0 < max_wait_probability < 1:
        raise ValueError("target probability must be between 0 and 1")
    if load_erlangs < 0:
        raise ValueError("load cannot be negative")
    servers = max(1, int(load_erlangs) + 1)
    while erlang_c(load_erlangs, servers) > max_wait_probability:
        servers += 1
    return servers
