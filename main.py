from fastapi import Depends,FastAPI,Query
from models.api import ParkingSpot
from datetime import datetime,timedelta
from dotenv import dotenv_values
from sqlmodel import create_engine,Session,select
from datetime import datetime
from models.dal import User
from typing import Annotated

# DB connection details
config = dotenv_values(".env")

# Connection url used to connect to mysql db
connection_url = f"mysql+mysqldb://{config["DB_USER"]}:{config["DB_PWD"]}@localhost:3306/{config["DB_NAME"]}"


# Create engine for manging connection pool
engine = create_engine(connection_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Adding metadata for session to indicate that it is coming from get_session method.
SessionDep = Annotated[Session, Depends(get_session)]

# intialization
app = FastAPI()

# Global variable for demoing post,get,update and delete
total = 200
parking_spots = []

@app.get("/users/")
def query_users(
    q: str,
    session: SessionDep,
    limit: Annotated[int, Query(le=100)] = 100
):
    users = session.exec(select(User).where(User.first_name == q or User.last_name == q).limit(limit)).all()
    print(f"Users returned from query_users: {users}")
    return users

@app.post("/users")
def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)


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
    return parking_spots[item_id]

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



