from fastapi import FastAPI
from models.reservations import ParkingSpot
from datetime import datetime,timedelta

# intialization
app = FastAPI()

# Global variable for demoing post,get,update and delete
total = 200
parking_spots = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reservations")
async def get_all_reservations() -> list:
    print(f"Current available parking_spots: {parking_spots}")
    return parking_spots


@app.get("/reservations/{item_id}")
async def get_reservation(item_id: int) -> ParkingSpot | None:
    print(f"Current available parking_spots: {parking_spots}, parking_spot: {parking_spots[item_id]}")
    if item_id in parking_spots:
        return parking_spots[item_id]
    
    return None

@app.post("/reservations/")
async def create_reservation(parking_spot: ParkingSpot) -> ParkingSpot:
    curr_index = len(parking_spots)
    print(f"Inside create_reservations, parking_spot: {parking_spot}, parking_spots: {parking_spots}")
    parking_spots.append({
        "reserved_by": parking_spot.reserved_by,
        "id": curr_index,
        "reserved_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(minutes=10)
    })

    print(f"After create_reservations, parking_spot: {parking_spot}, parking_spots: {parking_spots}")
    return parking_spots[len(parking_spots) - 1]

@app.put("/reservations/{id}")
async def update_reservation(id: int, new_parking_spot: ParkingSpot) -> ParkingSpot:    
    parking_spots[id] = new_parking_spot 
    print(f"parking_spots after update: {parking_spots}")
    return parking_spots[id]

@app.delete("/reservations/{id}")
async def delete_reservation(id: int):
    if id not in parking_spots:
        raise LookupError(f"Error occured while deleting parking spot with id: {id}")
    
    del parking_spots[id]
