from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm  import relationship
from sqlalchemy import ForeignKey
from typing import List
from sqlalchemy.orm import Mapped, mapped_column



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class initaitive(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(unique=True)
    Tag: Mapped[str]
    Latitude: Mapped[float]
    Logitude: Mapped[float]
    Date: Mapped[str]
    OverView: Mapped[str]
    #MileStones
    additional_notes: Mapped[str]
    owner:Mapped["user"] = relationship(back_populates ="initaitive")
    owner_ID:Mapped[int] = mapped_column(ForeignKey("user.id"),nullable = False) 
    photos: Mapped[List["Photo"]] = relationship(back_populates="parent_initiative", cascade="all, delete-orphan")

class Photo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    image_filename: Mapped[str] = mapped_column(nullable=False)
    initiative_id: Mapped[int] = mapped_column(ForeignKey("initaitive.id"))
    parent_initiative: Mapped["initaitive"] = relationship(back_populates="photos")


class   user(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    FirstName: Mapped[str]
    LastName: Mapped[str]
    initaitive: Mapped[List["initaitive"]]=relationship(back_populates ="owner")

