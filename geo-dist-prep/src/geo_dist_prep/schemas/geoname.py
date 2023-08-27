from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Float, Integer, String

from .base import Base


class PlaceType(PyEnum):
    BOROUGH = "borough"
    CITY = "city"
    HAMLET = "hamlet"
    NEIGHBOURHOOD = "neighbourhood"
    QUARTER = "quarter"
    SUBURB = "suburb"
    TOWN = "town"
    VILLAGE = "village"


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
