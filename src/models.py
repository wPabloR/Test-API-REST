from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(unique=True, nullable=False)

    
    flights: Mapped[List["Flight"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

class Airport(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "code": self.code
        }
    
class Flight(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    airport_origin_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    flight_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    departure_date: Mapped[int] = mapped_column(unique=True, nullable=False)
    arrive_date: Mapped[int] = mapped_column(unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(unique=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="flights")


    def serialize(self):
        return {
            "id": self.id,
            "airport_origin_id": self.airport_origin_id,
            "fly_number": self.fly_number,
            "arrive_date": self.arrive_date,
            "capacity": self.capacity
        }
    
class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    flight: Mapped[int] = mapped_column(unique=True, nullable=False)
    seat: Mapped[int] = mapped_column(unique=True, nullable=False)
    book_date: Mapped[int] = mapped_column(unique=True, nullable=False)
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.airport_origuser_idin_id,
            "vuelo_id": self.vuelo_id,
            "seat": self.seat,
            "book_date": self.book_date
        }