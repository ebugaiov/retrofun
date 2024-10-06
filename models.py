from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Model


class Manufacturer(Model):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)

    products: Mapped[list['Product']] = relationship(
        cascade='all, delete-orphan',
        back_populates='manufacturer'
    )

    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'


class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    year: Mapped[int] = mapped_column(index=True)
    country: Mapped[Optional[str]] = mapped_column(String(32))
    cpu: Mapped[Optional[str]] = mapped_column(String(32))
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index=True
    )

    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates='products'
    )

    def  __repr__(self):
        return f'Product({self.id}, "{self.name}")'