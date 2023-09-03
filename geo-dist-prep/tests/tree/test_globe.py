from geo_dist_prep.tree.globe import Globe
from geo_dist_prep.tree.pos import Pos


def test_caps_link():
    globe = Globe()
    nodes = globe.children

    for i in range(5):
        assert nodes[i].neighbours[Pos.LEFT] == nodes[(i - 1) % 5]
        assert nodes[i].neighbours[Pos.RIGHT] == nodes[(i + 1) % 5]
        assert nodes[i].neighbours[Pos.VERTICAL] == nodes[i + 5]

        assert nodes[i + 15].neighbours[Pos.LEFT] == nodes[(i - 1) % 5 + 15]
        assert nodes[i + 15].neighbours[Pos.RIGHT] == nodes[(i + 1) % 5 + 15]
        assert nodes[i + 15].neighbours[Pos.VERTICAL] == nodes[i + 10]


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
    assert list(globe.get_address(0, 0, 5)) == [5, 2, 3, 2, 2]


def test_add_child_matches_lookup():
    globe = Globe()

    t = (
        globe.children[0]
        .add_child(Pos.LEFT)
        .add_child(Pos.RIGHT)
        .add_child(Pos.VERTICAL)
        .add_child(Pos.CENTER)
    )
    assert list(globe.get_address(t.lat, t.lon, 5)) == [
        0,
        Pos.LEFT,
        Pos.RIGHT,
        Pos.VERTICAL,
        Pos.CENTER,
    ]


def test_repr():
    root = Globe()
    assert repr(root) == "Globe()"
