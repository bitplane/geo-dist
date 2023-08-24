from geo_dist_prep.utils import bisection_sort


def test_3():
    ordered = [1, 2, 3]
    assert bisection_sort(ordered) == [2, 1, 3]


def test_5():
    ordered = [1, 2, 3, 4, 5]
    result = bisection_sort(ordered)
    assert result == [3, 2, 5, 4, 1]
