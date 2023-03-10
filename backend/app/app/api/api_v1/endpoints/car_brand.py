from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.car_brand import (
    CarBrand,
    CarBrandCreate,
    CarBrandSearchResults,
    CarBrandUpdateRestricted,
)
from app.models.user import User

router = APIRouter()


@router.get("/{car_brand_id}", status_code=200, response_model=CarBrand)
def fetch_car_brand(
    *,
    car_brand_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single car brand by ID
    """
    result = crud.car_brand.get(db=db, id=car_brand_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Car Brand with ID {car_brand_id} not found"
        )

    return result

@router.get("/search/", status_code=200, response_model=CarBrandSearchResults)
def search_car_brands(
    *,
    keyword: str = Query('None', example="Honda"),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for car brands based on name keyword
    """
    results = crud.car_brand.get_multi(db=db, skip=skip, limit=limit, keyword=keyword)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=CarBrand)
def create_car_brand(
    *,
    car_brand_in: CarBrandCreate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new car brand in the database.
    """
    car_brand = crud.car_brand.create(db=db, obj_in=car_brand_in)

    return car_brand


@router.put("/", status_code=201, response_model=CarBrand)
def update_car_brand(
    *,
    car_brand_in: CarBrandUpdateRestricted,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update car brand in the database.
    """
    car_brand = crud.car_brand.get(db, id=car_brand_in.id)
    if not car_brand:
        raise HTTPException(
            status_code=400, detail=f"Car brand with ID: {car_brand_in.id} not found."
        )

    updated_car_brand = crud.car_brand.update(db=db, db_obj=car_brand, obj_in=car_brand_in)
    return updated_car_brand
