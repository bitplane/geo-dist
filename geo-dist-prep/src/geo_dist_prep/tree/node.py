import sys

from .pos import Pos


class Node:
    def __init__(
        self,
        coords: tuple[float],
        flipped: bool,
        depth: int = 0,
        parent: "Node" = None,
    ):
        # position of the tip of the triangle
        self.lat = coords[0]
        self.lon = coords[1]

        # direction into the triangle from the tip
        self.flipped: bool = flipped

        # depth in the tree
        self.depth: int = depth

        # children and neighbours indexed by Pos
        self.children: list[Node] = [None, None, None, None]
        self.neighbours: list[Node] = [None, None, None, None]
        self.neighbours[Pos.CENTER] = parent

    def add_child(self, pos: Pos) -> "Node":
        """
        Get or create a child of this node.
        """
        if not self.children[pos]:
            flipped = self.flipped if pos != Pos.CENTER else not self.flipped
            half_y = self.lat + self.height / 2.0 * self.direction
            base_y = self.lat + self.height * self.direction
            quarter_x = self.width / 4.0
            coords = {
                Pos.CENTER: (base_y, self.lon),
                Pos.VERTICAL: (self.lat, self.lon),
                Pos.LEFT: (half_y, self.lon - quarter_x),
                Pos.RIGHT: (half_y, self.lon + quarter_x),
            }[pos]
            depth = self.depth + 1
            self.children[pos] = Node(coords, flipped, depth, self)
            self.children[pos]._update_neighbours(pos)

        return self.children[pos]

    def _update_neighbours(self, my_pos: Pos):
        """
        Stitch this node into the tree by attaching to neighbours.

        This is called when a node is created, and because they can be created
        in any order, it has to do a local search to figure out what exists.
        """
        parent = self.neighbours[Pos.CENTER]
        if my_pos == Pos.CENTER:
            left = parent.children[Pos.LEFT]
            right = parent.children[Pos.RIGHT]
            vertical = parent.children[Pos.VERTICAL]
        elif my_pos == Pos.VERTICAL:
            left = parent.find([-Pos.LEFT, Pos.RIGHT])
            right = parent.find([-Pos.RIGHT, Pos.LEFT])
            vertical = parent.children[Pos.CENTER]
        elif my_pos == Pos.LEFT:
            left = parent.find([-Pos.LEFT, Pos.CENTER])
            right = parent.children[Pos.CENTER]
            vertical = parent.find([-Pos.VERTICAL, Pos.LEFT])
        elif my_pos == Pos.RIGHT:
            left = parent.children[Pos.CENTER]
            right = parent.find([-Pos.RIGHT, Pos.CENTER])
            vertical = parent.find([-Pos.VERTICAL, Pos.RIGHT])
        else:
            raise ValueError(f"Invalid child position: {my_pos}")

        self.neighbours[Pos.LEFT] = left
        self.neighbours[Pos.RIGHT] = right
        self.neighbours[Pos.VERTICAL] = vertical
        for neighbour, position in (
            (left, Pos.RIGHT),
            (right, Pos.LEFT),
            (vertical, Pos.VERTICAL),
        ):
            if neighbour:
                neighbour.neighbours[position] = self

    def find(self, path: list[Pos]) -> "Node":
        """
        Follow a path of positions to find a child.
        Negative positions mean outwards; neighbours or parent (CENTER)
        positive ones mean inwards; children.

        If a node can't be found then it'll return None
        """
        node = self
        for pos in path:
            if pos < 0:
                node = node.neighbours[-pos]
            else:
                node = node.children[pos]
            if not node:
                return None
        return node

    def plot(self, depth: int = sys.maxsize, colour="black"):
        """
        Draw this triangle and its children.
        """
        # we only need matplotlib when debugging the tree
        # so import here as a soft dependency
        import matplotlib.pyplot as plt

        x, y = [], []
        a, b, c = self.vertices
        x = [a[0], b[0], c[0], a[0]]
        y = [a[1], b[1], c[1], a[1]]
        plt.plot(x, y, color=colour)

        if depth := depth - 1:
            for child in self.children:
                if child:
                    child.plot(depth, colour)

    @property
    def direction(self) -> float:
        """up is positive latitude direction"""
        return 1.0 if self.flipped else -1.0

    @property
    def width(self) -> float:
        return 360.0 / 5.0 / 2.0**self.depth

    @property
    def height(self) -> float:
        return 180.0 / 3.0 / 2.0**self.depth

    @property
    def vertices(self):
        """
        Return as x, y coordinates for rendering
        """
        tip = self.lon, self.lat
        left = self.lon - self.width / 2, self.lat + self.height * self.direction
        right = self.lon + self.width / 2, self.lat + self.height * self.direction

        return tip, left, right

    @property
    def parent(self):
        return self.neighbours[Pos.CENTER]

    @property
    def address(self):
        """
        Return the path to this node in the tree.
        """
        current = self
        if current.parent:
            yield self.parent.children.find(current)
            current = current.parent

    def __str__(self):
        return ",".join(str(i) for i in self.address)

    def __repr__(self):
        return ",".join(str(i) for i in self.address)
