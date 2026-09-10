from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Float, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    full_name: Mapped[str]=mapped_column(String(120))
    phone: Mapped[str|None]=mapped_column(String(30), nullable=True)
    role: Mapped[str]=mapped_column(String(30), default='customer', index=True)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Restaurant(Base):
    __tablename__='restaurants_prod'
    id: Mapped[int]=mapped_column(primary_key=True)
    owner_id: Mapped[int|None]=mapped_column(ForeignKey('users.id'), nullable=True)
    name: Mapped[str]=mapped_column(String(160))
    cuisine: Mapped[str]=mapped_column(String(80))
    address: Mapped[str]=mapped_column(String(255))
    lat: Mapped[float|None]=mapped_column(Float, nullable=True)
    lng: Mapped[float|None]=mapped_column(Float, nullable=True)
    is_open: Mapped[bool]=mapped_column(Boolean, default=True)

class Driver(Base):
    __tablename__='drivers_prod'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'), unique=True)
    vehicle: Mapped[str]=mapped_column(String(80), default='Motorbike')
    status: Mapped[str]=mapped_column(String(30), default='offline')
    lat: Mapped[float|None]=mapped_column(Float, nullable=True)
    lng: Mapped[float|None]=mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__='orders_prod'
    id: Mapped[int]=mapped_column(primary_key=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey('users.id'))
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('restaurants_prod.id'))
    driver_id: Mapped[int|None]=mapped_column(ForeignKey('drivers_prod.id'), nullable=True)
    status: Mapped[str]=mapped_column(String(30), default='PENDING', index=True)
    total: Mapped[float]=mapped_column(Float)
    delivery_address: Mapped[str]=mapped_column(Text)
    lat: Mapped[float|None]=mapped_column(Float, nullable=True)
    lng: Mapped[float|None]=mapped_column(Float, nullable=True)
    payment_id: Mapped[str|None]=mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
