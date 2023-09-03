from enum import IntEnum


class Pos(IntEnum):
    """
    Positions for triangles in the tree.
    Used for both neighbours and children.
    """

    LEFT = 0
    """To the left; bottom left corner child, or attached to left edge"""
    RIGHT = 1
    """To the right; bottom right corner child, or attached to right edge"""
    VERTICAL = 2
    """Either below this triangle's base, or the child at the tip of this one"""
    CENTER = 3
    """The parent of this triangle, or the child at the center"""
