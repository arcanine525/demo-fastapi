from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CarBrand(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    logo_url = Column(String(256), nullable=True)
    desciption = Column(String(256), nullable=True)
    status = Column(Integer, default=1)
