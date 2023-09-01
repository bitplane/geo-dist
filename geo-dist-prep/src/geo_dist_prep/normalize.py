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


def denormalize_coords(y: float, x: float) -> tuple[float, float]:
    """
    Denormalize a latitude/longitude pair from [0, 1] to [-90, 90], [-180, 180].
    """
    lat = y * 180.0 + 90
    lon = x * 360.0 + 150

    return lat, lon
