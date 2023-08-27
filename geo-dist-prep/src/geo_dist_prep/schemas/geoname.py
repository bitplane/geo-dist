from enum import IntEnum

from sqlalchemy import Column, Enum, Float, Index, Integer, String

from .base import Base


class PlaceType(IntEnum):
    borough = 1
    city = 2
    hamlet = 3
    neighbourhood = 4
    quarter = 5
    suburb = 6
    town = 7
    village = 8


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
