from sqlalchemy import CheckConstraint, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GeoTable(Base):
    __tablename__ = "data"

    osm_id = Column(Integer, primary_key=True)
    type = Column(
        String,
        CheckConstraint(
            """
            type IN (
                'borough',
                'city',
                'hamlet',
                'neighbourhood',
                'quarter',
                'suburb',
                'town',
                'village'
            )
            """
        ),
    )
    lon = Column(Float)
    lat = Column(Float)
    name = Column(String)
    country_code = Column(
        String,
        CheckConstraint(
            """
            country_code IN (
                'gb',
                'im',
                'ie',
                'gg',
                'je'
            )
            """
        ),
    )
