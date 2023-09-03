import sys

from .pos import Pos


class Node:
    def __init__(
        self,
        coords: tuple[float],
        flipped: bool,
        pos: Pos,
        depth: int = 0,
        parent: "Node" = None,
        data=None,
    ):
        # position of the tip of the triangle
        self.lat = coords[0]
        self.lon = coords[1]
        self.data = data

        # direction into the triangle from the tip
        self.flipped: bool = flipped

        # depth in the tree
        self.depth: int = depth

        # children and neighbours indexed by Pos
        self.relations: dict[Pos, Node] = {}
        self.relations[Pos.PARENT] = parent

    def add_child(self, pos: Pos, data=None) -> "Node":
        """
        Get or create a child of this node.
        """
        if pos not in self.relations:
            flipped = self.flipped if pos != Pos.CENTER else not self.flipped
            half_y = self.lat + self.height / 2.0 * self.direction
            base_y = self.lat + self.height * self.direction
            quarter_x = self.width / 4.0
            coords = {
                Pos.CENTER: (base_y, self.lon),
                Pos.TIP: (self.lat, self.lon),
                Pos.LEFT_POINT: (half_y, self.lon - quarter_x),
                Pos.RIGHT_POINT: (half_y, self.lon + quarter_x),
            }[pos]
            depth = self.depth + 1
            self.relations[pos] = Node(
                coords=coords,
                flipped=flipped,
                pos=pos,
                depth=depth,
                parent=self,
                data=data,
            )
            self.relations[pos]._update_neighbours(pos)

        return self.relations[pos]

    def _update_neighbours(self, my_pos: Pos):
        """
        Stitch this node into the tree by attaching to neighbours.

        This is called when a node is created, and because they can be created
        in any order, it has to do a local search to figure out what exists.
        """
        parent = self.parent

        if not parent:
            return

        if my_pos == Pos.LEFT_POINT:
            left = parent.find([Pos.LEFT_POINT, Pos.TIP])
            right = parent.relations[Pos.CENTER]
            vertical = parent.find([Pos.BASE, Pos.LEFT_POINT])
        elif my_pos == Pos.RIGHT_POINT:
            left = parent.relations[Pos.CENTER]
            right = parent.find([Pos.RIGHT_EDGE, Pos.TIP])
            vertical = parent.find([Pos.BASE, Pos.RIGHT_POINT])
        elif my_pos == Pos.TIP:
            left = parent.find([Pos.LEFT_EDGE, Pos.RIGHT_POINT])
            right = parent.find([Pos.RIGHT_EDGE, Pos.LEFT_POINT])
            vertical = parent.relations[Pos.CENTER]
        elif my_pos == Pos.CENTER:
            left = parent.relations[Pos.LEFT_POINT]
            right = parent.relations[Pos.RIGHT_POINT]
            vertical = parent.relations[Pos.TIP]
        else:
            raise ValueError(f"Invalid child position: {my_pos}")

        self.relations[Pos.LEFT_EDGE] = left
        self.relations[Pos.RIGHT_EDGE] = right
        self.relations[Pos.BASE] = vertical
        for neighbour, position in (
            (left, Pos.RIGHT_EDGE),
            (right, Pos.LEFT_EDGE),
            (vertical, Pos.BASE),
        ):
            if neighbour:
                neighbour.relations[position] = self

    def find(self, path: list[Pos]) -> "Node":
        """
        Follow a path of positions to find a child.
        Negative positions mean outwards; neighbours or parent (CENTER)
        positive ones mean inwards; children.

        If a node can't be found then it'll return None
        """
        node = self
        for pos in path:
            node = node.relations.get(pos, None)
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
        if self.data:
            plt.text(
                self.lon,
                self.lat + self.direction * self.width / 2,
                str(self),
                color=colour,
            )

        if depth := depth - 1:
            for child in self.relations.values():
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
    def parent(self) -> "Node":
        return self.relations[Pos.CENTER]

    @property
    def address(self) -> list[Pos]:
        """
        Return the path to this node in the tree.
        """
        return ([self.parent.address] if self.parent else []) + [self.pos]

    def __str__(self):
        return str(self.data) if self.data else repr(self)

    def __repr__(self):
        return "/".join(str(int(i)) for i in self.address)
