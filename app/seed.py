from . import models, database
from sqlalchemy.orm import Session

def seed_data():
    db = Session(bind=database.engine)

    # Example: create 3-night itinerary
    itinerary = models.TripItinerary(title="Phuket Adventure", region="Phuket")
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)

    for i in range(1, 4):
        day = models.Day(day_number=i, itinerary_id=itinerary.id)
        db.add(day)
        db.commit()
        db.refresh(day)

        hotel = models.HotelAccommodation(name=f"Hotel {i}", location="Phuket", day_id=day.id)
        db.add(hotel)

        transfer = models.Transfer(from_location="Airport", to_location="Hotel", method="Car", day_id=day.id)
        db.add(transfer)

        activity = models.Activity(name="Beach Day", description="Relax on the beach", location="Patong", day_id=day.id)
        db.add(activity)

    # Add recommendation
    rec = models.RecommendedItinerary(nights=3, itinerary_id=itinerary.id)
    db.add(rec)
    db.commit()

if __name__ == "__main__":
    seed_data()