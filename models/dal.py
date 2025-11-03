from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

# DB models
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str

class ParkingSpot(SQLModel, table=True):
    id: int | None = Field(default=True, primary_key=True)
    reserved_at: datetime | None
    expires_at: datetime | None
    reserved_by: int 

# def print_values(values):
#     for val in values:
#         print(val)

# with Session(engine) as session:
#     new_user = User(first_name="Tech", last_name="Tales2025")
#     statement = select(User.first_name,User.last_name)
    
#     # Select query output before insert
#     users = session.exec(statement)
#     # Validate data
#     print_values(users)

#     #Insert into db
#     session.add(new_user)
#     session.commit()

#     # select query after insert
#     users = session.exec(statement)
#     # Validate data
#     print_values(users)

# def get_users(first_name):
#     query = select(User).where(User.first_name == first_name)
#     return query








