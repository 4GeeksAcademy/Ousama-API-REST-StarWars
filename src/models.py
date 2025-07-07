from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False) 
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False) 

    
    favorite_people: Mapped[List["FavoritePeople"]] = relationship("FavoritePeople", back_populates="user", cascade="all, delete-orphan")
    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    mass: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relación favoritos uno a muchos
    favorited_by_users: Mapped[List["FavoritePeople"]] = relationship("FavoritePeople", back_populates="people", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(50), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(50), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    climate: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(String(50), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relación favoritos uno a muchos
    favorited_by_users: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people' # Nombre de la tabla en la DB
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=False)

    # Relaciones con los modelos User y People
    user: Mapped["User"] = relationship("User", back_populates="favorite_people")
    people: Mapped["People"] = relationship("People", back_populates="favorited_by_users")

    __table_args__ = (UniqueConstraint('user_id', 'people_id', name='_user_people_uc'),)

    def __repr__(self):
        return f'<FavoritePeople User_ID: {self.user_id} People_ID: {self.people_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people_name": self.people.name if self.people else None 
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet' 
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)

    # Relaciones con los modelos User y Planet
    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorited_by_users")

    __table_args__ = (UniqueConstraint('user_id', 'planet_id', name='_user_planet_uc'),)

    def __repr__(self):
        return f'<FavoritePlanet User_ID: {self.user_id} Planet_ID: {self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet_name": self.planet.name if self.planet else None
        }