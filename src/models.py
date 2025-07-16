from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(unique=True, nullable=False)

    books: Mapped[List["Book"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }
    
    def __str__(self):
        return self.name

class Airport(db.Model):
    __tablename__ = "airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    country: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)

    flights: Mapped[List["Flight"]] = relationship(back_populates="airport")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "code": self.code
        }
    
    def __str__(self):
        return self.name 
    
class Flight(db.Model):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    departure_date: Mapped[date] = mapped_column(Date, unique=False, nullable=False)
    arrive_date: Mapped[date] = mapped_column(Date, unique=False, nullable=False)
    capacity: Mapped[int] = mapped_column(unique=False, nullable=False)


    books: Mapped[List["Book"]] = relationship(back_populates="flight")

    airport_origin_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    airport: Mapped["Airport"] = relationship(back_populates="flights")



    def serialize(self):
        return {
            "id": self.id,
            "airport_origin_id": self.airport_origin_id,
            "flight_number": self.flight_number,
            "arrive_date": self.arrive_date.strftime("%d/%m/%Y"),
            "departure_date": self.departure_date.strftime("%d/%m/%Y"),
            "capacity": self.capacity
        }

    def __str__(self):
        return f"Flight {self.flight_number}"
        
class Book(db.Model):
    __tablename__ = "book"
    __table_args__ = (
        UniqueConstraint("seat", "flight_id", name="unique_seat_per_flight"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    seat: Mapped[int] = mapped_column(unique=False, nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, unique=False, nullable=False)

    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="books")

    flight_id: Mapped[int] = mapped_column(ForeignKey("flight.id"))
    flight: Mapped["Flight"] = relationship(back_populates="books")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "seat": self.seat,
            "booking_date": self.booking_date.strftime("%d/%m/%Y")
        }
    
    def __str__(self):
        return f"Booking {self.id}"
    