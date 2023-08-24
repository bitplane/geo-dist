class GeoNode:
    """
    A node in a geo-quadtree.
    """

    def __init__(self, y=0.5, x=0.5, value=None, leaf=False):
        self.is_leaf = leaf  # false if we're a branch
        self.nodes: list[GeoNode] = [None, None, None, None]
        self.x = x
        self.y = y
        self.value = value

    def add(self, node):
        """
        Add a node.
        """
        idx = self.get_idx(node.y, node.x)

        if not self.nodes[idx]:
            self.nodes[idx] = node
        else:
            if self.is_leaf:
                # copy the existing node into a new branch
                new_node = GeoNode(self.y, self.x, self.value, leaf=True)
                self.is_leaf = False
                self.nodes = [None, None, None, None]
                self.value = None
                self.x = (new_node.x + node.x) / 2
                self.y = (new_node.y + node.y) / 2

                self.add(new_node)
                self.add(node)
            else:
                self.nodes[idx].add(node)

    def get_idx(self, y, x):
        pos_y = 0 if y < self.y else 2
        pos_x = 0 if x < self.x else 1
        return pos_y + pos_x


def location_to_pos(lat, lon):
    """
    Normalize a latitude/longitude pair to [0, 1].
    We use -30 as the center of the map, which is the middle of the
    atlantic ocean and doesn't intersect any land masses other than
    greenland, which is mostly ice.
    """
    y = ((lat - 90) % 180.0) / 180.0
    x = ((lon - 150) % 360.0) / 360.0

    return y, x
