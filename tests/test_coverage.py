import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays

from brigade.coverage import cover_counts, covered_share, uncovered_zones

INF = float("inf")
# 3 stations x 4 zones, minutes
TRAVEL = [
    [4.0, 9.0, 15.0, INF],
    [12.0, 6.0, 7.0, 20.0],
    [30.0, 25.0, 8.0, 9.5],
]
DEMAND = [100.0, 50.0, 30.0, 20.0]


def test_cover_counts_by_hand() -> None:
    assert cover_counts(TRAVEL, DEMAND, 10).tolist() == [1, 2, 2, 1]


def test_covered_share_by_hand() -> None:
    assert covered_share(TRAVEL, DEMAND, 10) == 1.0
    assert covered_share(TRAVEL, DEMAND, 8) == pytest.approx(180 / 200)
    assert covered_share(TRAVEL, DEMAND, 10, min_stations=2) == pytest.approx(80 / 200)


def test_busy_station_loses_its_cover() -> None:
    share = covered_share(TRAVEL, DEMAND, 10, available=[True, True, False])
    assert share == pytest.approx(180 / 200)
    assert uncovered_zones(TRAVEL, DEMAND, 10, available=[True, True, False]) == [3]


def test_uncovered_zones_busiest_first() -> None:
    assert uncovered_zones(TRAVEL, DEMAND, 5) == [1, 2, 3]
    assert uncovered_zones(TRAVEL, DEMAND, 3) == [0, 1, 2, 3]


def test_zero_demand_is_fully_covered_and_never_listed() -> None:
    assert covered_share(TRAVEL, [0.0, 0.0, 0.0, 0.0], 1) == 1.0
    assert uncovered_zones(TRAVEL, [0.0, 0.0, 0.0, 5.0], 1) == [3]


@given(
    arrays(np.float64, (4, 6), elements=st.floats(0, 60)),
    arrays(np.float64, (6,), elements=st.floats(0, 1000)),
    arrays(np.bool_, (4,)),
    st.integers(0, 3),
    st.floats(0, 60),
)
def test_losing_a_station_never_increases_cover(
    travel: np.ndarray, demand: np.ndarray, available: np.ndarray, lost: int, target: float
) -> None:
    fewer = available.copy()
    fewer[lost] = False
    assert covered_share(travel, demand, target, fewer) <= covered_share(
        travel, demand, target, available
    )


@given(
    arrays(np.float64, (3, 5), elements=st.floats(0, 60)),
    arrays(np.float64, (5,), elements=st.floats(0, 1000)),
    st.floats(0, 60),
)
def test_backup_cover_never_exceeds_single_cover(
    travel: np.ndarray, demand: np.ndarray, target: float
) -> None:
    assert covered_share(travel, demand, target, min_stations=2) <= covered_share(
        travel, demand, target
    )


@pytest.mark.parametrize(
    ("travel", "demand", "available"),
    [
        ([1.0, 2.0], [1.0, 1.0], None),
        (TRAVEL, [1.0], None),
        ([[float("nan")]], [1.0], None),
        ([[-1.0]], [1.0], None),
        ([[1.0]], [-1.0], None),
        (TRAVEL, DEMAND, [True]),
    ],
)
def test_bad_inputs_are_rejected(travel: object, demand: object, available: object) -> None:
    with pytest.raises(ValueError):
        cover_counts(travel, demand, 10, available)  # type: ignore[arg-type]
