from math import atan2, cos, radians, sqrt

EARTH_RADIUS = 6371000


def s_to_radians(s):
    return radians(float(s))


def measure(row):
    lon1, lat1, lon2, lat2 = map(
        s_to_radians, [row["lon1"], row["lat1"], row["lon2"], row["lat2"]]
    )

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Scaling
    dlat_meters = dlat * EARTH_RADIUS
    dlon_meters = dlon * EARTH_RADIUS * cos(lat1)  # approximate

    # Euclidean distance and angle
    distance = sqrt(dlat_meters**2 + dlon_meters**2)
    angle = atan2(dlat_meters, dlon_meters)

    return distance, angle
