import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Tool(Base):
    __tablename__ = 'tool'
    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable=False)
    description = Column(String(250))
    type = Column(String(80), nullable=False)
    total = Column(Integer)
    in_stock = Column(Integer)
    picture = Column(String(200))
    pair = Column(Integer, ForeignKey('tool.id'))


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    surname = Column(String(200))
    student_type = Column(String(50))
    student_year = Column(Integer)
    phone_number = Column(String(50))

class ToolList(Base):
    __tablename__ = 'tool_list'
    id = Column(Integer, nullable=False, primary_key=True)
    owner_id = Column(Integer, nullable=False)
    datetime_created = Column(String(30), nullable=False) #YYYY-MM-DD HH:MI:SS
    datetime_approved = Column(String(30))
    datetime_returned = Column(String(30))
    approved_status = Column(Integer)
    returned_status = Column(Integer)
    shared = Column(Integer)
    shared_from_id = Column(Integer)
    

engine = create_engine('sqlite:///shop.db')


Base.metadata.create_all(engine)