from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add this middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React/Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/itineraries/")
def create_itinerary(itinerary: schemas.TripItineraryCreate, db: Session = Depends(get_db)):
    db_itinerary = models.TripItinerary(title=itinerary.title, region=itinerary.region)
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)

    for day_data in itinerary.days:
        db_day = models.Day(day_number=day_data.day_number, itinerary_id=db_itinerary.id)
        db.add(db_day)
        db.commit()
        db.refresh(db_day)

        db_hotel = models.HotelAccommodation(name=day_data.hotel.name, location=day_data.hotel.location, day_id=db_day.id)
        db.add(db_hotel)

        for t in day_data.transfers:
            db_transfer = models.Transfer(from_location=t.from_location, to_location=t.to_location, method=t.method, day_id=db_day.id)
            db.add(db_transfer)

        for a in day_data.activities:
            db_activity = models.Activity(name=a.name, description=a.description, location=a.location, day_id=db_day.id)
            db.add(db_activity)

    db.commit()
    return {"message": "Itinerary created"}

@app.get("/itineraries/")
def get_itineraries(db: Session = Depends(get_db)):
    itineraries = db.query(models.TripItinerary).options(
        joinedload(models.TripItinerary.days)
        .joinedload(models.Day.hotel),
        joinedload(models.TripItinerary.days)
        .joinedload(models.Day.transfers),
        joinedload(models.TripItinerary.days)
        .joinedload(models.Day.activities)
    ).all()
    return itineraries

@app.get("/recommendations/{nights}")
def get_recommendation(nights: int, db: Session = Depends(get_db)):
    result = db.query(models.RecommendedItinerary).filter_by(nights=nights).first()
    if not result:
        raise HTTPException(status_code=404, detail="No itinerary found")
    return {"recommended_itinerary_id": result.itinerary_id}