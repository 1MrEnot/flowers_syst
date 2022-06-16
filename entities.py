from typing import Iterable

from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gauge_id = Column(String(), nullable=True)
    name = Column(String(), nullable=False)
    average_cycle = Column(Float, nullable=True, default=None)
    min_moisture = Column(Float, default=0)
    next_watering = Column(DateTime, nullable=True, default=None)
    winter_mode = Column(Boolean(), nullable=False, default=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    winter_mode = Column(Boolean(), nullable=False, default=False)

    plants: Iterable[Plant] = relationship("Plant", primaryjoin="and_(User.id==Plant.owner_id)")


class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float(), nullable=False)


class Watering(Base):
    __tablename__ = "watering"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
