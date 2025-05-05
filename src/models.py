from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    favorites: Mapped[List["Favorites"]] = relationship("Favorites", back_populates="user")
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class People(db.Model):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites = relationship('Favorites', back_populates='person')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites = relationship('Favorites', back_populates='vehicle')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites = relationship('Favorites', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    vehicles_id: Mapped[int] = mapped_column(ForeignKey('vehicles.id'), nullable=True)
    planets_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    person: Mapped[Optional["People"]] = relationship("People", back_populates="favorites")  
    planet: Mapped[Optional["Planets"]] = relationship("Planets", back_populates="favorites")  
    vehicle: Mapped[Optional["Vehicles"]] = relationship("Vehicles", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.people_id,
            "planet_id": self.planets_id,
            "vehicle_id": self.vehicles_id
        }