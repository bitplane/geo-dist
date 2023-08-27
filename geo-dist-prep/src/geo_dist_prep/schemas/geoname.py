from geo_dist_prep.schemas.base import Base
from sqlalchemy import Column, Float, Integer, String

dropped_columns = [
    "alternative_names",
    "street" "city",
    "county",
    "state",
    "country",
    "display_name",
    "west",
    "south",
    "east",
    "north",
    "wikidata",
    "wikipedia",
    "housenumbers",
]


class GeoName(Base):
    __tablename__ = "geonames"

    osm_id = Column(Integer, primary_key=True)
    name = Column(String)
    osm_type = Column(String)
    class_ = Column("class", String)
    type_ = Column("type", String)
    lon = Column(Float)
    lat = Column(Float)
    place_rank = Column(Integer)
    importance = Column(Float)
    country_code = Column(String)
