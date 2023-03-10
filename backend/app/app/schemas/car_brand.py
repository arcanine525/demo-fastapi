from pydantic import BaseModel, HttpUrl

from typing import Sequence


class CarBrandBase(BaseModel):
    name: str
    logo_url: str
    desciption: str
    status: int


class CarBrandCreate(CarBrandBase):
    name: str
    logo_url: str
    desciption: str
    status: int


class CarBrandUpdate(CarBrandBase):
    id: int


class CarBrandUpdateRestricted(BaseModel):
    id: int
    name: str


# Properties shared by models stored in DB
class CarBrandInDBBase(CarBrandBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class CarBrand(CarBrandInDBBase):
    pass


# Properties properties stored in DB
class CarBrandInDB(CarBrandInDBBase):
    pass


class CarBrandSearchResults(BaseModel):
    results: Sequence[CarBrand]
