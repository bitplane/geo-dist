from enum import Enum


class Pos(str, Enum):
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

    PARENT = "U"
    """The parent of this node"""

    ROOT = "root"
    """The root of the tree, special case for the top level"""

    # N_CAP_0 = "0"
    # N_CAP_1 = "1"
    # N_CAP_2 = "2"
    # N_CAP_3 = "3"
    # N_CAP_4 = "4"

    # N_MID_0 = "5"
    # N_MID_1 = "6"
    # N_MID_2 = "7"
    # N_MID_3 = "8"
    # N_MID_4 = "9"

    # S_MID_0 = "10"
    # S_MID_1 = "11"
    # S_MID_2 = "12"
    # S_MID_3 = "13"
    # S_MID_4 = "14"

    # S_CAP_0 = "15"
    # S_CAP_1 = "16"
    # S_CAP_2 = "17"
    # S_CAP_3 = "18"
    # S_CAP_4 = "19"
