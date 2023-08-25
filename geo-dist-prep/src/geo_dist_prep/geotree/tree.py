from geo_dist_prep.utils import bisection_sort

from .node import GeoNode, location_to_pos


class Tree:
    """
    A quadtree for storing geospatial data
    """

    def __init__(self):
        self.root = GeoNode()
        self.members = {}

    def add(self, lat, lon, value):
        """
        Collect a node from the input data
        """
        y, x = location_to_pos(lat, lon)
        self.members[(y, x)] = value

    def finalize(self):
        """
        Actually build the tree
        """
        # build the tree structure up-front so it's balanced
        # before doing any inserts
        y_coords = (y for y, _x in self.members.keys())
        x_coords = (x for _y, x in self.members.keys())
        sorted_y = bisection_sort(y_coords)
        sorted_x = bisection_sort(x_coords)
        branch_keys = set(zip(sorted_y, sorted_x))

        for y, x in branch_keys:
            node = GeoNode(y, x, leaf=False)
            self.root.add(node)

        for y, x in self.members.keys():
            node = GeoNode(y, x, value=self.members[(y, x)], leaf=True)
            self.root.add(node)

    def sample_data(self, max_distance, neighbours=10):
        """
        Sample data from the tree
        """
        for y, x in self.members.keys():
            nodes = self.root.get_levels(y, x)
            base = nodes.pop()
            if not base.value:
                continue
            group = {base}

            while nodes and len(group) < neighbours:
                parent = nodes.pop()
                for node in parent.nodes:
                    if not node or node in group:
                        continue
                    if node.distance(y, x) < max_distance:
                        group.add(node)

            for node in group:
                if node.value:
                    yield (
                        node.value["lon"],
                        node.value["lat"],
                        base.value["lon"],
                        base.value["lat"],
                    )
