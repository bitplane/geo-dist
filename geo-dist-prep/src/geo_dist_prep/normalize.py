def normalize_coords(lat: float, lon: float) -> tuple[float, float]:
    """
    Normalize a latitude/longitude pair to [0, 1].
    We use -30 as the center of the map, which is the middle of the
    atlantic ocean and doesn't intersect any land masses other than
    greenland, which is mostly ice.
    """
    y = ((lat - 90) % 180.0) / 180.0
    x = ((lon - 150) % 360.0) / 360.0

    return y, x
