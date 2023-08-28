"""
SQLAlchemy queries that run server-side.
"""
from sqlalchemy import Integer, and_, func

from .geoname import GeoName


def km_to_lon(lat, km):
    """Converts kilometers to degrees longitude at a given latitude."""
    return km / (111.32 * func.cos(func.radians(lat) * func.pi() / 180))


def km_to_lat(km):
    """Converts kilometers to degrees latitude."""
    return km / 111.32


def lat_to_km(lat):
    """Converts degrees latitude to kilometers."""
    return lat * 111.32


def lon_to_km(lat, lon):
    """Converts degrees longitude to kilometers at a given latitude."""
    return lon * 111.32 * func.cos(func.radians(lat))


def distance(lat1, lon1, lat2, lon2):
    """
    Returns the distance in km between two points on the Earth's surface.
    Place should be a table or subquery.columns with `lat` and `lon`.
    """
    dist_lat_sq = func.pow(lat_to_km(lat1) - lat_to_km(lat2), 2)
    dist_lon_sq = func.pow(lon_to_km(lat1, lon1) - lon_to_km(lat2, lon2), 2)

    return func.sqrt(dist_lat_sq + dist_lon_sq).label("distance")


def direction(lat1, lon1, lat2, lon2):
    """
    Calculate symmetric direction based on latitude and longitude.

    Use normalized atan2 to get an angle in the range [0, 1).
    """
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    angle = func.atan2(delta_lat, delta_lon) + func.pi()
    return func.mod(angle, 2 * func.pi()) / (2 * func.pi())


def nearby(lat, lon, km):
    """Finds all places within `km` km of `lat`, `lon`."""
    in_box = and_(
        GeoName.lat >= lat - km_to_lat(km),
        GeoName.lat <= lat + km_to_lat(km),
        GeoName.lon >= lon - km_to_lon(lat, km),
        GeoName.lon <= lon + km_to_lon(lat, km),
    )
    in_circle = distance(GeoName.lat, GeoName.lon, lat, lon) < km

    return and_(in_box, in_circle)


def grid_coord(place, grid_size):
    """
    Returns a unique integer for each grid square of size `grid_size` km.
    place should be a table/subquery.columns with `lat` and `lon`. grid_size
    should be a float.
    """
    y_offset_km = 90 * 111.32  # 90 degrees * 111.32 km/degree
    y = func.floor((lat_to_km(place.lat) + y_offset_km) / grid_size)
    max_y = 180 * 111.32 / grid_size + 1

    x_km_degree = lon_to_km(place.lat, 1)  # km/degree at this latitude
    x_offset_km = 180 * x_km_degree  # deal with negative longitudes
    x = func.floor((lon_to_km(place.lat, place.lon) + x_offset_km) / grid_size)

    return func.cast(y * max_y + x, Integer)
