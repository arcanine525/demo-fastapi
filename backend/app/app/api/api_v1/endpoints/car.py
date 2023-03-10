from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.car import (
    Car,
    CarCreate,
    CarSearchResults,
    CarUpdateRestricted,
)
from app.models.user import User

router = APIRouter()


@router.get("/{car_id}", status_code=200, response_model=Car)
def fetch_car(
    *,
    car_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single car by ID
    """
    result = crud.car.get(db=db, id=car_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Car with ID {car_id} not found"
        )

    return result

@router.get("/search/", status_code=200, response_model=CarSearchResults)
def search_cars(
    *,
    keyword: str = Query('', example="Honda"),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for cars based on name keyword
    """
    results = crud.car.get_multi(db=db, skip=skip, limit=limit, keyword=keyword)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Car)
def create_car(
    *,
    car_in: CarCreate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new car in the database.
    """
    car_brand = crud.car_brand.get(db=db, id=car_in.car_brand_id)
    if not car_brand:
        raise HTTPException(
            status_code=404, detail=f"Car Brand with ID {car_in.car_brand_id} not found"
        )

    car = crud.car.create(db=db, obj_in=car_in)

    return car


@router.put("/", status_code=201, response_model=Car)
def update_car(
    *,
    car_in: CarUpdateRestricted,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update car in the database.
    """

    car = crud.car.get(db, id=car_in.id)

    if not car:
        raise HTTPException(
            status_code=400, detail=f"Car with ID: {car_in.id} not found."
        )

    updated_car = crud.car.update(db=db, db_obj=car, obj_in=car_in)
    return updated_car
