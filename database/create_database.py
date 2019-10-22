from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlite3
Base = declarative_base()
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key = True)
class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(8))
    restuarant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
### Insert at the end of file ###
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)