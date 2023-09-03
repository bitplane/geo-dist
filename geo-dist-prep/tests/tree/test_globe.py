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
