"""
Contains some debugging functions to visualize the tree.
"""
import math

from geo_dist_prep.tree.pos import Pos


def lat_lon_to_xyz(lat, lon, radius=1):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.cos(lat_rad) * math.sin(lon_rad)
    z = radius * math.sin(lat_rad)

    return x, y, z


def plot_node(node, depth: int = 6, colour="black"):
    """
    Draw this triangle and its children to the given depth.
    """
    import matplotlib.pyplot as plt
    from geo_dist_prep.tree.node import Node

    node: Node = node

    verts = node.vertices_2d

    # x, y, z = zip(*[lat_lon_to_xyz(lat, lon) for lon, lat in verts])

    x = [vert[0] for vert in verts] + [verts[0][0]]
    y = [vert[1] for vert in verts] + [verts[0][1]]

    plt.plot(x, y, color=colour)
    if node.data:
        plt.text(
            node.lon,
            node.lat + node.direction * node.width / 2,
            str(node),
            color=colour,
        )

    if depth > 1:
        for idx in [Pos.LEFT_POINT, Pos.RIGHT_POINT, Pos.TIP, Pos.CENTER]:
            child = node.relations.get(idx)
            if child:
                child.plot(depth - 1, colour)


def plot_globe(globe, depth: int = 1, colour="blue") -> None:
    import matplotlib.pyplot as plt
    from geo_dist_prep.tree.globe import Globe

    globe: Globe = globe

    plt.figure()

    for name in globe.relations:
        if name not in list(Pos):
            globe.relations[name].plot(depth, colour)
