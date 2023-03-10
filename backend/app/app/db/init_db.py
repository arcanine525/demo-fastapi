import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


brands = [
    {
        "name": 'Toyota',
        "logo_url": "https://picsum.photos/200",
        "desciption": "Lorem ipsum dolor sit amet.",
        "status": 1
    },
    {
        "name": 'BMW',
        "logo_url": "https://picsum.photos/200",
        "desciption": "Fusce vestibulum ac mauris a.",
        "status": 1
    },
    {
        "name": 'Mazda',
        "logo_url": "https://picsum.photos/200",
        "desciption": "Phasellus vitae sem quam. Donec.",
        "status": 1
    },
    {
        "name": 'Honda',
        "logo_url": "https://picsum.photos/200",
        "desciption": "Mauris non aliquet purus, bibendum.",
        "status": 1
    }
]

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.db.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.db.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.db.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.db.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.db.FIRST_SUPERUSER} already exists. "
            )

    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.io"
        )

    ## Init car brands
    logger.info("Init car brands ... ")
    for brand in brands:
        car_brand_in = schemas.CarBrandCreate(**brand)
        car_brand = crud.car_brand.create(db, obj_in=car_brand_in)
