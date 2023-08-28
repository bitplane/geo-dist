from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint

from .base import Base


class GeoNamePair(Base):
    __tablename__ = "geoname_pair"
    __table_args__ = (UniqueConstraint("start_id", "end_id", name="unique_pair"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("geoname_pair_job.id"), nullable=False)
    start_id = Column(Integer, ForeignKey("geonames.osm_id"), nullable=False)
    end_id = Column(Integer, ForeignKey("geonames.osm_id"), nullable=False)
    distance = Column(Float, nullable=True)
    direction = Column(Float, nullable=True)
