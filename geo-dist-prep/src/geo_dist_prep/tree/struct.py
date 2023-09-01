from enum import IntEnum


class Position(IntEnum):
    LEFT = 0
    RIGHT = 1
    HORIZONTAL = 2
    GLOBAL = 3


class TreeNode:
    def __init__(
        self,
        pos: tuple[float],
        depth: int,
        flipped: bool,
        parent: "TreeNode" = None,
    ):
        # position of the tip of the triangle
        self.lat = pos[0]
        self.lon = pos[1]

        # direction into the triangle from the tip
        self.flipped = flipped

        # depth in the tree
        self.depth = depth

        self.parent = parent
        self.children = [None, None, None]

        if self.parent:
            pass
        else:
            # neighbours
            self.position = Position.GLOBAL
            self.neighbours = [None, None, None]

        # children

    def get_child(self, pos: Position):
        if not self._child_inner:
            self._child_inner = TreeNode(
                (self.lat + self.height * self.direction, self.lon),
                self.depth + 1,
                not self.flipped,
                self,
            )
        return self._child_inner

    @property
    def direction(self):
        return 1 if self.flipped else -1

    @property
    def width(self):
        return 360 / 5 / 2**self.depth

    @property
    def height(self):
        return 180 / 3 / 2**self.depth

    @property
    def tip_point(self):
        return self.lat, self.lon

    @property
    def left_point(self):
        return self.lat + self.height * self.direction, self.lon - self.width / 2

    @property
    def right_point(self):
        return self.lat + self.height * self.direction, self.lon + self.width / 2

    @property
    def child_tip(self):
        if not self._child_tip:
            self._child_tip = TreeNode(
                (self.lat, self.lon),
                self.depth + 1,
                self.flipped,
                self,
            )
        return self._child_tip

    @property
    def child_left(self):
        if not self._child_left:
            self._child_left = TreeNode(
                (
                    self.lat + self.height / 2 * self.direction,
                    self.lon - self.width / 4,
                ),
                self.depth + 1,
                self.flipped,
                self,
            )
        return self._child_left

    @property
    def child_right(self):
        if not self._child_right:
            self._child_right = TreeNode(
                (
                    self.lat + self.height / 2 * self.direction,
                    self.lon + self.width / 4,
                ),
                self.depth + 1,
                self.flipped,
                self,
            )
        return self._child_right


def build_top_level() -> list[TreeNode]:
    """
    Build the top level of the tree, which is a list of triangles that cover
    the entire globe as an icosahedron.
    """
    width = 360 / 5
    height = 180 / 3

    north_cap = [
        TreeNode((90, (i * width - 180) % 360), flipped=False) for i in range(5)
    ]
    north_belt = [
        TreeNode((height, (i * width - 180) % 360), flipped=True) for i in range(5)
    ]
    south_belt = [
        TreeNode((-height, (i * width - 180 + width / 2) % 360), flipped=False)
        for i in range(5)
    ]
    south_cap = [
        TreeNode((-90, (i * width - 180 + width / 2) % 360), flipped=True)
        for i in range(5)
    ]

    for i in range(5):
        left = (i - 1) % 5
        right = (i + 1) % 5
        north_cap[i]._left = north_cap[left]
        north_cap[i]._right = north_cap[right]
        north_cap[i]._base = north_belt[i]

        south_cap[i]._left = south_cap[left]
        south_cap[i]._right = south_cap[right]
        south_cap[i]._base = south_belt[i]

        north_belt[i]._left = south_belt[left]
        north_belt[i]._right = south_belt[right]
        north_belt[i]._base = north_cap[i]

        south_belt[left]._left = north_belt[i]
        south_belt[right]._right = north_belt[i]
        south_belt[i]._base = south_cap[i]

    return north_cap + north_belt + south_belt + south_cap
