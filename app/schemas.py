from pydantic import BaseModel
from typing import List

class ActivityModel(BaseModel):
    name: str
    description: str
    location: str

class TransferModel(BaseModel):
    from_location: str
    to_location: str
    method: str

class HotelModel(BaseModel):
    name: str
    location: str

class DayModel(BaseModel):
    day_number: int
    hotel: HotelModel
    transfers: List[TransferModel]
    activities: List[ActivityModel]

class TripItineraryCreate(BaseModel):
    title: str
    region: str
    days: List[DayModel]
