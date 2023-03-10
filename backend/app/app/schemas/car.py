from pydantic import BaseModel, HttpUrl

from typing import Sequence


class CarBase(BaseModel):
    name: str
    logo_url: str
    desciption: str
    status: int


class CarCreate(CarBase):
    name: str
    logo_url: str
    desciption: str
    status: int
    car_brand_id: int


class CarUpdate(CarBase):
    id: int


class CarUpdateRestricted(BaseModel):
    id: int
    name: str
    logo_url: str
    desciption: str
    status: int


# Properties shared by models stored in DB
class CarInDBBase(CarBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Car(CarInDBBase):
    pass


# Properties properties stored in DB
class CarInDB(CarInDBBase):
    pass


class CarSearchResults(BaseModel):
    results: Sequence[Car]
