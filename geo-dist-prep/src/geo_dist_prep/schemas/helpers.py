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


# # delete duplicate grid coords
# grid_size = 1
# grid_column = grid_coord(GeoName, grid_size).label('grid_coord')
# table_plus_grid = session.query(GeoName).add_columns(grid_column)
# distinct_by_grid = table_plus_grid.group_by('grid_coord').distinct()
# non_distinct_rows = table_plus_grid.except_(distinct_by_grid)
# ids_to_delete = [x[0] for x in non_distinct_rows.with_entities(GeoName.osm_id).all()]
# # delete in chunks
# chunk_size = 999
# for i in range(0, len(ids_to_delete), chunk_size):
#     chunk_ids = ids_to_delete[i:i+chunk_size]
#     session.query(GeoName).filter(GeoName.osm_id.in_(chunk_ids)).delete(synchronize_session='fetch')
# session.commit()
