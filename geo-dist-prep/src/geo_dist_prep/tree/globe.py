from .node import Node
from .pos import Pos

TILE_WIDTH = 360.0 / 5.0
TILE_HEIGHT = 180.0 / 3.0


class Globe(Node):
    def __init__(self):
        self.neighbours = [None] * len(Pos)
        self.neighbours[Pos.CENTER] = None
        self.neighbours[Pos.LEFT] = self
        self.neighbours[Pos.RIGHT] = self
        self.neighbours[Pos.VERTICAL] = self
        self.children = []
        self.build()

    def get_address(self, lat: float, lon: float, max_depth: int = 15) -> list[int]:
        """
        Get the address of the node that contains the given coordinates.

        :param lat: Latitude of the coordinates.
        :param lon: Longitude of the coordinates.
        :return: Address of the node that contains the coordinates.
        """
        lat = max(min(lat, 90.0), -90.0)
        lon = (lon + 180.0) % 360.0 - 180.0
        if not max_depth:
            return

        node_id = self._get_root_idx(lat, lon)
        yield node_id

        node = self.children[node_id]

        width = node.width
        height = node.height
        direction = node.direction
        y = node.lat
        x = node.lon
        depth = 1

        while depth < max_depth:
            tip = abs(lat - y) <= height / 2

            ypos = -(lat - (y + height * direction)) / (height * direction / 2)
            xpos = abs((lon - x) / (width / 4))
            center = xpos <= ypos and 0 <= xpos <= 1 and 0 <= ypos <= 1

            left = lon < x

            if tip:
                yield Pos.VERTICAL
            elif center:
                yield Pos.CENTER
                y += height * direction
                direction *= -1
            elif left:
                yield Pos.LEFT
                x -= width / 4
                y += height / 2 * direction
            else:
                yield Pos.RIGHT
                x += width / 4
                y += height / 2 * direction

            depth += 1
            width /= 2
            height /= 2

    def _get_root_idx(self, lat: float, lon: float) -> int:
        in_belt = lat < 90.0 - TILE_HEIGHT
        in_south = lat < -90.0 + TILE_HEIGHT
        row_idx = 10 if in_south else (5 if in_belt else 0)

        column = (lon + TILE_WIDTH / 2.0) // TILE_WIDTH
        if in_belt:
            center = column * TILE_WIDTH
            x_fraction = (lon - center) / (TILE_WIDTH / 2)
            y_fraction = (90 - TILE_HEIGHT - lat) / TILE_HEIGHT
            south_belt = 1 - abs(x_fraction) < y_fraction
            if south_belt:
                row_idx += 5
                if x_fraction < 0:
                    column -= 1

        return row_idx + int(column) % 5

    def build(self):
        """
        Build the top level of the tree, which is a list of 20 triangles that cover
        the entire globe as an icosahedron.

        This layout is special, but after creating it everything else should
        naturally align. There's 4 rows of 5 triangles each, alternate rows are
        flipped, and the bottom two rows are shifted half a triangle to the right.
        """

        north_cap: list[Node] = []
        north_mid: list[Node] = []
        south_mid: list[Node] = []
        south_cap: list[Node] = []

        for i in range(5):
            n_lon = i * TILE_WIDTH + 180
            s_lon = n_lon + TILE_WIDTH / 2
            north_cap.append(Node((90, n_lon % 360 - 180), flipped=False, parent=self))
            north_mid.append(
                Node(
                    (90 - TILE_HEIGHT * 2, n_lon % 360 - 180), flipped=True, parent=self
                )
            )
            south_mid.append(
                Node(
                    (-90 + TILE_HEIGHT * 2, s_lon % 360 - 180),
                    flipped=False,
                    parent=self,
                )
            )
            south_cap.append(Node((-90, s_lon % 360 - 180), flipped=True))

        for i in range(5):
            left = (i - 1) % 5
            right = (i + 1) % 5
            north_cap[i].neighbours[Pos.LEFT] = north_cap[left]
            north_cap[i].neighbours[Pos.RIGHT] = north_cap[right]
            north_cap[i].neighbours[Pos.VERTICAL] = north_mid[i]

            south_cap[i].neighbours[Pos.LEFT] = south_cap[left]
            south_cap[i].neighbours[Pos.RIGHT] = south_cap[right]
            south_cap[i].neighbours[Pos.VERTICAL] = south_mid[i]

            north_mid[i].neighbours[Pos.LEFT] = south_mid[left]
            north_mid[i].neighbours[Pos.RIGHT] = south_mid[right]
            north_mid[i].neighbours[Pos.VERTICAL] = north_cap[i]

            south_mid[left].neighbours[Pos.LEFT] = north_mid[i]
            south_mid[right].neighbours[Pos.RIGHT] = north_mid[i]
            south_mid[i].neighbours[Pos.VERTICAL] = south_cap[i]

        self.children = north_cap + north_mid + south_mid + south_cap
