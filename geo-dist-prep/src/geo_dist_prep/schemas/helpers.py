from sqlalchemy import Integer, and_, func

from .geoname import GeoName


def km_to_lon(lat, km):
    return km / (111.32 * func.cos(func.radians(lat) * func.pi() / 180))


def km_to_lat(km):
    return km / 111.32


def lat_to_km(lat):
    return lat * 111.32


def lon_to_km(lat, lon):
    return lon * 111.32 * func.cos(func.radians(lat))


def distance(lat1, lon1, lat2, lon2):
    """
    Returns the distance in km between two points on the Earth's surface.
    Place should be a table or subquery.columns with `lat` and `lon`.
    """
    dist_lat_sq = func.pow(lat_to_km(lat1) - lat_to_km(lat2), 2)
    dist_lon_sq = func.pow(lon_to_km(lat1, lon1) - lon_to_km(lat2, lon2), 2)

    return func.sqrt(dist_lat_sq + dist_lon_sq).label("distance")


def nearby(lat, lon, km):
    in_box = and_(
        GeoName.lat >= lat - km_to_lat(km),
        GeoName.lat <= lat + km_to_lat(km),
        GeoName.lon >= lon - km_to_lon(lat, km),
        GeoName.lon <= lon + km_to_lon(lat, km),
    )
    in_circle = distance(GeoName.lat, GeoName.lon, lat, lon) < km

    return and_(in_box, in_circle)


def grid_coord(place, grid_size: float):
    """
    Returns a unique integer for each grid square of size `grid_size` km.
    place should be a table/subquery.columns with `lat` and `lon`. grid_size
    should be a float.
    """
    y = func.floor((lat_to_km(place.lat) + 90 * 111.32) / grid_size)
    lon_km = lon_to_km(place.lat, grid_size)
    x = func.floor((lon_to_km(place.lat, place.lon) + 180 * 111.32) / lon_km)
    max_y = int(180 * 111.32 / grid_size) + 1

    return func.cast(y * max_y + x, Integer)


# grid_size = 1.5
# place = session.query(GeoName).filter(GeoName.osm_id == bindparam('id')).subquery().c
# coord = session.query(GeoName).filter(grid_coord(GeoName, grid_size).label('grid_coord')).distinct()

# query = session.query(GeoName)#.filter(nearby_subquery(place)).params(id=southport, km=50)
# query = query.add_columns(grid_coord(GeoName, grid_size).label('grid_coord')).group_by('grid_coord').distinct()

# query = session.query(GeoName).filter(GeoName.osm_id.not_in(select(query.subquery().c.osm_id)))
# query.delete()
