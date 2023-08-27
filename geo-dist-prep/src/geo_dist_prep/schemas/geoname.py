from enum import IntEnum

from sqlalchemy import Column, Enum, Float, Index, Integer, String

from .base import Base


class PlaceType(IntEnum):
    BOROUGH = 1
    CITY = 2
    HAMLET = 3
    NEIGHBOURHOOD = 4
    QUARTER = 5
    SUBURB = 6
    TOWN = 7
    VILLAGE = 8


class GeoName(Base):
    __tablename__ = "geonames"

    osm_id = Column(Integer, primary_key=True)
    name = Column(String)
    type_ = Column(Enum(PlaceType))
    lon = Column(Float)
    lat = Column(Float)
    place_rank = Column(Integer)
    importance = Column(Float)
    country_code = Column(String)


Index("lat_index", GeoName.lat)
Index("lon_index", GeoName.lon)
