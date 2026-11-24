import pytest
from hypothesis import given
from hypothesis import strategies as st

from brigade.queueing import erlang_b, erlang_c, mean_wait, servers_needed


def test_erlang_b_by_hand() -> None:
    # A = 2, c = 2: (A^2 / 2!) / (1 + A + A^2 / 2!) = 2 / 5
    assert erlang_b(2, 2) == pytest.approx(0.4)


def test_erlang_b_single_server() -> None:
    # c = 1: A / (1 + A)
    assert erlang_b(3, 1) == pytest.approx(0.75)


def test_erlang_b_textbook_table_value() -> None:
    # Standard Erlang B table: 10 erlangs on 15 lines blocks about 3.65% of calls.
    assert erlang_b(10, 15) == pytest.approx(0.0365, abs=5e-5)


def test_erlang_b_stays_accurate_for_large_systems() -> None:
    b = erlang_b(900, 1000)
    assert 0 < b < 1e-3


def test_erlang_c_by_hand() -> None:
    # A = 2, c = 3: C = 3 B / (3 - 2 (1 - B)) with B = 4/19 -> 4/9
    assert erlang_c(2, 3) == pytest.approx(4 / 9)


@given(st.floats(0.01, 50), st.integers(1, 80))
def test_waiting_is_at_least_as_likely_as_loss(load: float, servers: int) -> None:
    if load >= servers:
        return
    assert erlang_c(load, servers) >= erlang_b(load, servers) - 1e-12


@given(st.floats(0.01, 40), st.integers(1, 60))
def test_more_servers_never_increase_blocking(load: float, servers: int) -> None:
    assert erlang_b(load, servers + 1) <= erlang_b(load, servers) + 1e-15


def test_unstable_queue_is_rejected() -> None:
    with pytest.raises(ValueError, match="stable"):
        erlang_c(3, 3)


def test_mean_wait_single_server_matches_mm1() -> None:
    # M/M/1: Wq = rho / (mu - lambda); lambda = 2/h, mu = 4/h -> 0.5 / 2 = 0.25 h
    assert mean_wait(2, 0.25, 1) == pytest.approx(0.25)


def test_no_calls_means_no_wait() -> None:
    assert mean_wait(0, 1, 2) == 0.0


def test_servers_needed() -> None:
    assert servers_needed(2, 0.5) == 3  # C(2, 3) = 0.444
    assert erlang_c(10, servers_needed(10, 0.05)) <= 0.05
    assert erlang_c(10, servers_needed(10, 0.05) - 1) > 0.05


@pytest.mark.parametrize(
    "call",
    [
        lambda: erlang_b(-1, 2),
        lambda: erlang_b(1, 0),
        lambda: mean_wait(1, 0, 2),
        lambda: servers_needed(2, 1.5),
    ],
)
def test_bad_inputs_are_rejected(call: object) -> None:
    with pytest.raises(ValueError):
        call()  # type: ignore[operator]
