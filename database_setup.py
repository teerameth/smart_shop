#!/usr/bin/env python
# — coding: utf-8 —
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    student_university_ID = db.Column(db.String(11), nullable=False) # stored in format 613405000xx
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    student_type = db.Column(db.String(20), nullable=False) # 1=ป.ตรี, 2=ป.โท , 3=ป.เอก, 4=อาจารย์, 5=อื่นๆ
    student_year = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False) #stored in format 09xxxxxxxx
    lists = db.relationship('Tool_list', backref='owner')

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tool_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    total = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('tool_group.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.relationship('Tool')
    amount = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('tool_list.id'))

class Tool_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Order', backref='list')
    created_datetime = db.Column(db.String(27), nullable=False) # stored in format dd:mm:yy-hh:mm:ss
    approved_status = db.Column(db.Integer) # default = 0
    approved_datetime = db.Column(db.String(27))
    returned_status = db.Column(db.Integer) # default = 0
    returned_datetime = db.Column(db.String(27))
    shared = db.Column(db.Integer) # สร้างเอง = 0, ถูกshareมา = 1
    shared_from_ID = db.Column(db.String(11)) # stored in format 613405000xx
    owner_id = db.Column(db.Integer, db.ForeignKey('student.id'))

class Tool_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    tools = db.relationship('Tool', backref='group')

if __name__ == '__main__':
    db.create_all()
