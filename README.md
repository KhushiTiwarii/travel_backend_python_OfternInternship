## Travel Itinerary Backend

### Run the app
```bash
uvicorn app.main:app --reload
```

### Seed the database
```bash
python -m app.seed
```

### Endpoints
- POST `/itineraries/` - Create itinerary
- GET `/itineraries/` - View itineraries
- GET `/recommendations/{nights}` - Get recommended itinerary
