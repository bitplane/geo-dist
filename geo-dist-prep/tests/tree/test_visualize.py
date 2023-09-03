from geo_dist_prep.tree.globe import Globe
from geo_dist_prep.tree.pos import Pos
from pytest import mark


@mark.skip(reason="interactive")
def test_visualize_root():
    root = Globe().children

    i = Pos.CENTER
    root[6].add_child(i)
    root[6].children[i].add_child(i)
    root[6].children[i].children[i].add_child(i)

    from matplotlib import pyplot as plt

    plt.figure()

    for node in root:
        node.plot()

    plt.show()


@mark.skip(reason="interactive")
def test_visualize_address():
    globe = Globe()
    root = globe.children

    from matplotlib import pyplot as plt

    plt.figure()

    for node in root:
        node.plot()

    lons = [12, 123.1, 154, 45]
    lats = [17, 10.2, 18, 67]

    plt.scatter(lons, lats)

    for lon, lat in zip(lons, lats):
        address = list(globe.get_address(lat, lon))
        current = globe.children[address.pop(0)]
        for node in address:
            current.add_child(node)
            current = current.children[node]
            current.plot(1, "red")

    plt.show()
    pass
