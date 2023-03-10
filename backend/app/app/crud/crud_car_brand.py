from typing import Union, List

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, select

from app.crud.base import CRUDBase
from app.models.car_brand import CarBrand
from app.models.user import User
from app.models.car_brand import CarBrand
from app.schemas.car_brand import CarBrandCreate, CarBrandUpdateRestricted, CarBrandUpdate


class CRUDCarBrand(CRUDBase[CarBrand, CarBrandCreate, CarBrandUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: CarBrand,
        obj_in: Union[CarBrandUpdate, CarBrandUpdateRestricted]
    ) -> CarBrand:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000, keyword
    ) -> List[CarBrand]:

        return (
            db.query(self.model).filter(
            or_(
                func.lower(self.model.name).contains(keyword),
                func.lower(self.model.desciption).contains(keyword),
            )).order_by(self.model.id).offset(skip).limit(limit).all()
        )


car_brand = CRUDCarBrand(CarBrand)
