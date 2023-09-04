from geo_dist_prep.tree.globe import Globe
from geo_dist_prep.tree.pos import Pos


def test_root_node_links():
    # i eyeballed these and exported the positions afterwards
    globe = Globe()

    assert globe.relations[0].relations[Pos.LEFT_EDGE].pos == 4
    assert globe.relations[0].relations[Pos.RIGHT_EDGE].pos == 1
    assert globe.relations[0].relations[Pos.BASE].pos == 5

    assert globe.relations[1].relations[Pos.LEFT_EDGE].pos == 0
    assert globe.relations[1].relations[Pos.RIGHT_EDGE].pos == 2
    assert globe.relations[1].relations[Pos.BASE].pos == 6

    assert globe.relations[2].relations[Pos.LEFT_EDGE].pos == 1
    assert globe.relations[2].relations[Pos.RIGHT_EDGE].pos == 3
    assert globe.relations[2].relations[Pos.BASE].pos == 7

    assert globe.relations[3].relations[Pos.LEFT_EDGE].pos == 2
    assert globe.relations[3].relations[Pos.RIGHT_EDGE].pos == 4
    assert globe.relations[3].relations[Pos.BASE].pos == 8

    assert globe.relations[4].relations[Pos.LEFT_EDGE].pos == 3
    assert globe.relations[4].relations[Pos.RIGHT_EDGE].pos == 0
    assert globe.relations[4].relations[Pos.BASE].pos == 9

    assert globe.relations[5].relations[Pos.LEFT_EDGE].pos == 14
    assert globe.relations[5].relations[Pos.RIGHT_EDGE].pos == 10
    assert globe.relations[5].relations[Pos.BASE].pos == 0

    assert globe.relations[6].relations[Pos.LEFT_EDGE].pos == 10
    assert globe.relations[6].relations[Pos.RIGHT_EDGE].pos == 11
    assert globe.relations[6].relations[Pos.BASE].pos == 1

    assert globe.relations[7].relations[Pos.LEFT_EDGE].pos == 11
    assert globe.relations[7].relations[Pos.RIGHT_EDGE].pos == 12
    assert globe.relations[7].relations[Pos.BASE].pos == 2

    assert globe.relations[8].relations[Pos.LEFT_EDGE].pos == 12
    assert globe.relations[8].relations[Pos.RIGHT_EDGE].pos == 13
    assert globe.relations[8].relations[Pos.BASE].pos == 3

    assert globe.relations[9].relations[Pos.LEFT_EDGE].pos == 13
    assert globe.relations[9].relations[Pos.RIGHT_EDGE].pos == 14
    assert globe.relations[9].relations[Pos.BASE].pos == 4

    assert globe.relations[10].relations[Pos.LEFT_EDGE].pos == 5
    assert globe.relations[10].relations[Pos.RIGHT_EDGE].pos == 6
    assert globe.relations[10].relations[Pos.BASE].pos == 15

    assert globe.relations[11].relations[Pos.LEFT_EDGE].pos == 6
    assert globe.relations[11].relations[Pos.RIGHT_EDGE].pos == 7
    assert globe.relations[11].relations[Pos.BASE].pos == 16

    assert globe.relations[12].relations[Pos.LEFT_EDGE].pos == 7
    assert globe.relations[12].relations[Pos.RIGHT_EDGE].pos == 8
    assert globe.relations[12].relations[Pos.BASE].pos == 17

    assert globe.relations[13].relations[Pos.LEFT_EDGE].pos == 8
    assert globe.relations[13].relations[Pos.RIGHT_EDGE].pos == 9
    assert globe.relations[13].relations[Pos.BASE].pos == 18

    assert globe.relations[14].relations[Pos.LEFT_EDGE].pos == 9
    assert globe.relations[14].relations[Pos.RIGHT_EDGE].pos == 5
    assert globe.relations[14].relations[Pos.BASE].pos == 19

    assert globe.relations[15].relations[Pos.LEFT_EDGE].pos == 19
    assert globe.relations[15].relations[Pos.RIGHT_EDGE].pos == 16
    assert globe.relations[15].relations[Pos.BASE].pos == 10

    assert globe.relations[16].relations[Pos.LEFT_EDGE].pos == 15
    assert globe.relations[16].relations[Pos.RIGHT_EDGE].pos == 17
    assert globe.relations[16].relations[Pos.BASE].pos == 11

    assert globe.relations[17].relations[Pos.LEFT_EDGE].pos == 16
    assert globe.relations[17].relations[Pos.RIGHT_EDGE].pos == 18
    assert globe.relations[17].relations[Pos.BASE].pos == 12

    assert globe.relations[18].relations[Pos.LEFT_EDGE].pos == 17
    assert globe.relations[18].relations[Pos.RIGHT_EDGE].pos == 19
    assert globe.relations[18].relations[Pos.BASE].pos == 13

    assert globe.relations[19].relations[Pos.LEFT_EDGE].pos == 18
    assert globe.relations[19].relations[Pos.RIGHT_EDGE].pos == 15
    assert globe.relations[19].relations[Pos.BASE].pos == 14


def test__get_root_idx():
    globe = Globe()

    assert globe._get_root_idx(0, 179) == 12
    assert globe._get_root_idx(15, 160) == 7
    assert globe._get_root_idx(0, 0) == 5
    assert globe._get_root_idx(80, 0) == 0
    assert globe._get_root_idx(-80, 0) == 15


def test_get_address():
    globe = Globe()

    # empty address when doing 0 deep
    assert list(globe.get_address(0, 0, 0)) == []

    # should only get first one when doing 1 deep
    assert list(globe.get_address(0, 0, 1)) == [5]

    # drill in at the top
    assert list(globe.get_address(0, 0, 5)) == [5, "v", "c", "v", "v"]


def test_add_child_matches_lookup():
    globe = Globe()

    t = (
        globe.relations[0]
        .add_child(Pos.LEFT_POINT)
        .add_child(Pos.RIGHT_POINT)
        .add_child(Pos.TIP)
        .add_child(Pos.CENTER)
    )
    assert list(globe.get_address(t.lat, t.lon, 5)) == [
        0,
        Pos.LEFT_POINT,
        Pos.RIGHT_POINT,
        Pos.TIP,
        Pos.CENTER,
    ]


def test_repr():
    root = Globe()
    assert repr(root) == "Globe()"
