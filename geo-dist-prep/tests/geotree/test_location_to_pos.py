import math

from geo_dist_prep.geotree.node import location_to_pos

thirty_degrees = 30 / 360


def is_about(value, expected):
    return math.isclose(value, expected, abs_tol=1e-5)


def test_lat():
    lat = -89.999999
    y, _x = location_to_pos(lat, 0)
    assert is_about(y, 0)


def test_max_lat():
    lat = 89.999999
    y, x = location_to_pos(lat, 0)
    assert is_about(y, 1)


def test_mid_lon():
    _y, x = location_to_pos(0, -30)
    assert x == 0.5


def test_wrap_max_lon():
    _y, x = location_to_pos(0, 180 + 360)
    assert x == thirty_degrees


def test_center_lat_lon():
    lat, lon = 0, -30
    y, x = location_to_pos(lat, lon)
    assert (y, x) == (0.5, 0.5)
