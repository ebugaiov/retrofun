from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from pygments.lexer import default
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy import Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from db import Model


ProductCountry = Table(
    'products_countries',
    Model.metadata,
    Column('product_id', ForeignKey('products.id'), primary_key=True,
            nullable=False),
    Column('country_id', ForeignKey('countries.id'), primary_key=True,
            nullable=False),
)


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


class Country(Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)

    products: Mapped[list['Product']] = relationship(
        secondary=ProductCountry, back_populates='countries'
    )

    def __repr__(self):
        return f'Country({self.id}, "{self.name}")'


class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[Optional[str]] = mapped_column(String(32))
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index=True
    )

    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates='products'
    )
    countries: Mapped[list['Country']] = relationship(
        secondary=ProductCountry, back_populates='products'
    )

    order_items: WriteOnlyMapped[list['OrderItem']] = relationship(back_populates='product')
    reviews: WriteOnlyMapped['ProductReview'] = relationship(back_populates='product')
    blog_articles: WriteOnlyMapped['BlogArticle'] = relationship(back_populates='product')

    def  __repr__(self):
        return f'Product({self.id}, "{self.name}")'


class Order(Model):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'), index=True)

    customer: Mapped['Customer'] = relationship(back_populates='orders')

    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order')

    def __repr__(self):
        return f'Order({self.id.hex})'


class Customer(Model):
    __tablename__ = 'customers'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(128))
    phone: Mapped[Optional[str]] = mapped_column(String(32))

    orders: WriteOnlyMapped['Order'] = relationship(back_populates='customer')
    product_reviews: WriteOnlyMapped['ProductReview'] = relationship(back_populates='customer')
    blog_users: WriteOnlyMapped['BlogUser'] = relationship(back_populates='customer')

    def __repr__(self):
        return f'Customer({self.id.hex}, "{self.name}")'


class OrderItem(Model):
    __tablename__ = 'order_items'

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), primary_key=True)
    unit_price: Mapped[float]
    quantity: Mapped[int]

    product: Mapped['Product'] = relationship(back_populates='order_items')
    order: Mapped['Order'] = relationship(back_populates='order_items')


class ProductReview(Model):
    __tablename__ = 'product_reviews'

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'), primary_key=True)

    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    rating: Mapped[int]
    comment: Mapped[Optional[str]] = mapped_column(Text)

    product: Mapped['Product'] = relationship(back_populates='reviews')
    customer: Mapped['Customer'] = relationship(back_populates='product_reviews')


class BlogArticle(Model):
    __tablename__ = 'blog_articles'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

    author_id: Mapped[int] = mapped_column(ForeignKey('blog_authors.id'), index=True)
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id'), index=True)

    author: Mapped['BlogAuthor'] = relationship(back_populates='articles')
    product: Mapped[Optional['Product']] = relationship(back_populates='blog_articles')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates='article')

    def __repr__(self):
        return f'BlogArticle({self.id}, "{self.title}")'


class BlogAuthor(Model):
    __tablename__ = 'blog_authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)

    articles: WriteOnlyMapped['BlogArticle'] = relationship(back_populates='author')

    def __repr__(self):
        return f'BlogAuthor({self.id}, "{self.name}")'


class BlogUser(Model):
    __tablename__ = 'blog_users'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    customer_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('customers.id'), index=True)

    customer: Mapped[Optional['Customer']] = relationship(back_populates='blog_users')
    sessions: WriteOnlyMapped['BlogSession'] = relationship(back_populates='user')

    def __repr__(self):
        return f'BlogUser({self.id.hex})'


class BlogSession(Model):
    __tablename__ = 'blog_sessions'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('blog_users.id'), index=True)

    user: Mapped['BlogUser'] = relationship(back_populates='sessions')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates='session')

    def __repr__(self):
        return f'BlogSession({self.id.hex})'


class BlogView(Model):
    __tablename__ = 'blog_views'

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

    article_id: Mapped[int] = mapped_column(ForeignKey('blog_articles.id'))
    session_id: Mapped[UUID] = mapped_column(ForeignKey('blog_sessions.id'))

    article: Mapped['BlogArticle'] = relationship(back_populates='views')
    session: Mapped['BlogSession'] = relationship(back_populates='views')