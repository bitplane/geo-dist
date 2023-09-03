from enum import Enum


class Pos(Enum):
    """
    Positions for triangles in the tree.
    Used for both neighbours and children.
    """

    LEFT_POINT = "l"
    """Child in the left corner"""
    RIGHT_POINT = "r"
    """Child in the right corner"""
    TIP = "v"
    """Child at the tip of this one. Direction depdends on orientation"""
    CENTER = "c"
    """the child in the center, it'll be flipped upside down"""

    LEFT_EDGE = "L"
    """Neighbour on the left edge"""
    RIGHT_EDGE = "R"
    """Neighbour on the right edge"""
    BASE = "V"
    """The bottom of the triangle"""

    PARENT = "parent"
    """The parent of this node"""
