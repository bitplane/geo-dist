class GeoNode:
    """
    A node in a geo-quadtree.
    """

    def __init__(self, lat=-30.0, lon=0.0, value=None, leaf=False):
        self.is_leaf = leaf  # false if we're a branch
        self.nodes: list[GeoNode] = [None, None, None, None]
        self.lat = lat
        self.lon = lon
        self.x, self.y = self.location_to_geonode(lat, lon)
        self.value = value
        self.needs_rebalance = False

    def balance(self):
        """
        Balance all the nodes under this one
        """
        # depth-first rebalance
        for node in self.nodes:
            if node and not node.is_leaf and node.needs_rebalance:
                node.balance()

        # get the average position of our children
        nodes = [node for node in self.nodes if node]
        self.lat = sum([node.lat for node in nodes]) / len(nodes)
        self.lon = sum([node.lon for node in nodes]) / len(nodes)
        self.x, self.y = self.location_to_geonode(self.lat, self.lon)

    def add(self, node):
        """
        Add a node internally
        """

        if self.is_leaf:
            # meh. copy in a hot loop. fixme?
            new_node = GeoNode(self.lat, self.lon, self.value, leaf=True)
            self.is_leaf = False
            self.x = self.y = self.value = None
            self.needs_rebalance = True
            self.add(new_node)

        pos_y = 0 if node.y < self.y else 2
        pos_x = 0 if node.x < self.x else 1
        idx = pos_y + pos_x

        if not self.nodes[idx]:
            self.nodes[idx] = node
        else:
            self.nodes[idx].add(node)

        # probably required. not sure though. electricity is cheaper than
        # brain cycles.
        self.balance()

    def location_to_geonode(lat, lon):
        """
        Normalize a latitude/longitude pair to [0, 1].
        We use -30 as the center of the map, which is the middle of the
        atlantic ocean and doesn't intersect any land masses other than
        greenland, which is mostly ice.
        """
        y = (lat + 90) / 180
        x = (lon + 150) / 360

        return y, x
