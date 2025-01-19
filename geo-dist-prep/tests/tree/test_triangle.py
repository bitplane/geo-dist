from geo_dist_prep.tree.triangle import Coords, Triangle

A = Coords(0, 2)
A_FLIPPED = Coords(0, -2)
B = Coords(-1, 0)
C = Coords(1, 0)
D = Coords(0, 0)
E = Coords(-0.5, 1)
F = Coords(0.5, 1)

T = Triangle(A, B, C)
FLIPPED = Triangle(A_FLIPPED, B, C)


def test_point_in_top_triangle():
    P = Coords(0, 1.9)
    result = T.point_location(P)

    assert P in result
    assert result.A == A
    assert result.B == E
    assert result.C == F


def test_point_in_top_triangle_flipped():
    P = Coords(0, -1.9)
    result = FLIPPED.point_location(P)

    assert P in result
    assert result.A == A_FLIPPED
    assert result.B == E
    assert result.C == F


def test_point_in_left_triangle():
    P = Coords(-0.9, 0.1)
    result = T.point_location(P)

    assert P in result
    assert result.A == B
    assert result.B == D
    assert result.C == E


def test_point_in_left_triangle_flipped():
    P = Coords(-0.9, -0.1)
    result = FLIPPED.point_location(P)

    assert P in result
    assert result.A == B
    assert result.B == D
    assert result.C == E


def test_point_in_right_triangle():
    P = Coords(0.9, 0.1)
    result = T.point_location(P)

    assert P in result
    assert result.A == C
    assert result.B == D
    assert result.C == F


def test_point_in_right_triangle_flipped():
    P = Coords(0.9, -0.1)
    result = FLIPPED.point_location(P)

    assert P in result
    assert result.A == C
    assert result.B == D
    assert result.C == F


def test_point_in_middle_triangle():
    P = Coords(0, 0.5)
    result = T.point_location(P)

    assert P in result
    assert result.A == D
    assert result.B == E
    assert result.C == F


def test_point_in_middle_triangle_flipped():
    P = Coords(0, -0.5)
    result = FLIPPED.point_location(P)

    assert P in result
    assert result.A == D
    assert result.B == E
    assert result.C == F
