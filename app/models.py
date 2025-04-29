from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class TripItinerary(Base):
    __tablename__ = 'trip_itineraries'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    region = Column(String)
    days = relationship("Day", back_populates="itinerary")

class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer)
    itinerary_id = Column(Integer, ForeignKey('trip_itineraries.id'))
    itinerary = relationship("TripItinerary", back_populates="days")
    hotel = relationship("HotelAccommodation", uselist=False, back_populates="day")
    transfers = relationship("Transfer", back_populates="day")
    activities = relationship("Activity", back_populates="day")

class HotelAccommodation(Base):
    __tablename__ = 'hotel_accommodations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    day_id = Column(Integer, ForeignKey('days.id'))
    day = relationship("Day", back_populates="hotel")

class Transfer(Base):
    __tablename__ = 'transfers'
    id = Column(Integer, primary_key=True)
    from_location = Column(String)
    to_location = Column(String)
    method = Column(String)
    day_id = Column(Integer, ForeignKey('days.id'))
    day = relationship("Day", back_populates="transfers")

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    location = Column(String)
    day_id = Column(Integer, ForeignKey('days.id'))
    day = relationship("Day", back_populates="activities")

class RecommendedItinerary(Base):
    __tablename__ = 'recommended_itineraries'
    id = Column(Integer, primary_key=True)
    nights = Column(Integer)
    itinerary_id = Column(Integer, ForeignKey('trip_itineraries.id'))
