from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .base import Base


class Job(Base):
    __tablename__ = "job"
    __mapper_args__ = {"polymorphic_identity": "job", "polymorphic_on": "type"}
    id = Column(Integer, primary_key=True)
    type = Column(String)
    started = Column(Integer)
    finished = Column(Integer)
    success = Column(Boolean, default=False)
    message = Column(String)


class GeoNamePairJob(Job):
    __tablename__ = "geoname_pair_job"
    __mapper_args__ = {"polymorphic_identity": "geoname_pair_job"}
    id = Column(Integer, ForeignKey("job.id"), primary_key=True)
    country_code = Column(String(3))
