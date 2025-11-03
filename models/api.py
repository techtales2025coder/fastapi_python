from typing import Union
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    first_name: str
    second_name: str

class ParkingSpot(BaseModel):
    id: Union[int, None] = None
    reserved_at: Union[datetime, None] = None
    expires_at: Union[datetime, None] = None
    reserved_by: User

