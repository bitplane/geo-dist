from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint

from .base import Base


class TrainingData(Base):
    __tablename__ = "training_data"
    __table_args__ = (UniqueConstraint("start_id", "end_id", name="unique_pair"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("geoname_enrich_job.id"), nullable=False)
    start_id = Column(Integer, ForeignKey("geonames.osm_id"), nullable=False)
    end_id = Column(Integer, ForeignKey("geonames.osm_id"), nullable=False)
    y1 = Column(Float, nullable=False)
    x1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    direction = Column(Float, nullable=False)
    distance = Column(Float, nullable=False)
