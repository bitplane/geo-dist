from geo_dist_prep.tree.render import plot_globe

from .node import Node
from .pos import Pos

TILE_WIDTH = 360.0 / 5.0
TILE_HEIGHT = 180.0 / 3.0


class Globe(Node):
    def __init__(self):
        super().__init__(
            coords=(0.0, 0.0), flipped=False, pos=None, depth=0, parent=None, data=None
        )
        self.lat = self.lon = 0.0
        self.relations = {}
        self.relations[Pos.PARENT] = None
        self.relations[Pos.LEFT_EDGE] = self
        self.relations[Pos.RIGHT_EDGE] = self
        self.relations[Pos.BASE] = self
        self.build()

    def get_address(self, lat: float, lon: float, max_depth: int = 13) -> list[int]:
        """
        Get the address of the node that contains the given coordinates.

        :param lat: Latitude of the coordinates.
        :param lon: Longitude of the coordinates.
        :return: Address of the node that contains the coordinates.
        """
        if not max_depth:
            return

        lat = max(min(lat, 90.0), -90.0)
        lon = (lon + 180.0) % 360.0 - 180.0

        node_id = self._get_root_idx(lat, lon)
        yield node_id

        if max_depth == 1:
            return

        node = self.relations[node_id]

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
                yield Pos.TIP
            elif center:
                yield Pos.CENTER
                y += height * direction
                direction *= -1
            elif left:
                yield Pos.LEFT_POINT
                x -= width / 4
                y += height / 2 * direction
            else:
                yield Pos.RIGHT_POINT
                x += width / 4
                y += height / 2 * direction

            depth += 1
            width /= 2
            height /= 2

    def _get_root_idx(self, lat: float, lon: float) -> int:
        in_belt = lat <= 90.0 - TILE_HEIGHT
        in_south = lat <= -90.0 + TILE_HEIGHT
        row_idx = 10 if in_south else (5 if in_belt else 0)

        column = (lon + TILE_WIDTH / 2.0) // TILE_WIDTH
        if in_belt:
            center = column * TILE_WIDTH
            x_fraction = (lon - center) / (TILE_WIDTH / 2)
            y_fraction = (90 - TILE_HEIGHT - lat) / TILE_HEIGHT
            south_belt = 1 - abs(x_fraction) <= y_fraction
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
            north_cap.append(
                Node(
                    coords=(90, n_lon % 360 - 180),
                    pos=Pos.ROOT,
                    flipped=False,
                    parent=self,
                )
            )
            north_mid.append(
                Node(
                    coords=(90 - TILE_HEIGHT * 2, n_lon % 360 - 180),
                    pos=Pos.ROOT,
                    flipped=True,
                    parent=self,
                )
            )
            south_mid.append(
                Node(
                    coords=(-90 + TILE_HEIGHT * 2, s_lon % 360 - 180),
                    pos=Pos.ROOT,
                    flipped=False,
                    parent=self,
                )
            )
            south_cap.append(
                Node(
                    coords=(-90, s_lon % 360 - 180),
                    pos=Pos.ROOT,
                    flipped=True,
                    parent=self,
                )
            )

        for i in range(5):
            left = (i - 1) % 5
            right = (i + 1) % 5
            north_cap[i].relations[Pos.LEFT_EDGE] = north_cap[left]
            north_cap[i].relations[Pos.RIGHT_EDGE] = north_cap[right]
            north_cap[i].relations[Pos.BASE] = north_mid[i]

            south_cap[i].relations[Pos.LEFT_EDGE] = south_cap[left]
            south_cap[i].relations[Pos.RIGHT_EDGE] = south_cap[right]
            south_cap[i].relations[Pos.BASE] = south_mid[i]

            north_mid[i].relations[Pos.LEFT_EDGE] = south_mid[left]
            north_mid[i].relations[Pos.RIGHT_EDGE] = south_mid[right]
            north_mid[i].relations[Pos.BASE] = north_cap[i]

            south_mid[left].relations[Pos.LEFT_EDGE] = north_mid[i]
            south_mid[right].relations[Pos.RIGHT_EDGE] = north_mid[i]
            south_mid[i].relations[Pos.BASE] = south_cap[i]

        children = north_cap + north_mid + south_mid + south_cap
        for i, child in enumerate(children):
            self.relations[i] = child

    def plot(self, depth: int = 1, colour: str = "green"):
        plot_globe(self, depth, colour)

    def __repr__(self):
        return "Globe()"

    def __str__(self):
        return "Globe()"
