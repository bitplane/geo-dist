from geo_dist_prep.utils import bisection_sort


def test_5():
    ordered = [1, 2, 3, 4, 5]
    result = bisection_sort(ordered)
    assert result == [3, 5, 2, 4, 1]


def test_lots():
    huge = range(1_000_000)
    result = bisection_sort(huge)

    assert len(set(result)) == 1_000_000
    assert result[0] == 500_000
