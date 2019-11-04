from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Association(db.Model):
    __tablename__ = 'association'
    left_id = db.Column(db.Integer, db.ForeignKey('left.id'), primary_key=True)
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    child = db.relationship("Child", back_populates="parents")
    parent = db.relationship("Parent", back_populates="children")

class Parent(db.Model):
    __tablename__ = 'left'
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Association", back_populates="parent")

class Child(db.Model):
    __tablename__ = 'right'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parents = db.relationship("Association", back_populates="child")
    

p1 = Parent()
p2 = Parent()
c1 = Child(name="aaa")
c2 = Child(name="bbb")
a = Association(extra_data="some data")
a.child = c1
p1.children.append(a)
b = Association(extra_data="some data")
b.child = c2
p1.children.append(b)
c = Association(extra_data="some data")
c.child = c2
p2.children.append(c)

for assoc in p1.children:
    print(assoc.extra_data)
    print(assoc.child.name)
for assoc in p2.children:
    print(assoc.child.name)