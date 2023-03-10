# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.car_brand import CarBrand  # noqa
from app.models.car import Car # noqa

