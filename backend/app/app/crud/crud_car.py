from typing import Union, List

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, select

from app.crud.base import CRUDBase
from app.models.car_brand import CarBrand
from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdateRestricted, CarUpdate


class CRUDCar(CRUDBase[Car, CarCreate, CarUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Car,
        obj_in: Union[CarUpdate, CarUpdateRestricted]
    ) -> Car:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000, keyword=''
    ) -> List[Car]:

        return (
            db.query(self.model).filter(
            or_(
                func.lower(self.model.name).contains(keyword),
                func.lower(self.model.desciption).contains(keyword),
            )).order_by(self.model.id).offset(skip).limit(limit).all()
        )


car = CRUDCar(Car)
