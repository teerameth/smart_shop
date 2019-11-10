from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from editor import Editor
editor = Editor()
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

students = editor.list_all_student()
tools = editor.list_all_tool()
print(tools[0].name)
for student in students:
    print(student.name)
    new_list = student.create_new_list()
    new_list.add_new_tool(tools[0], 1)

student = editor.get_student_by_id(61340500032)

for lit in student.get_lists():
    for order in lit.orders:
        print(order.tool[0].name)
new_list = student.create_new_list()
new_list.add_new_tool(tools[10], 2)

#######################################
for student in students:
    print(student.name)
    for lists in student.get_lists():
        for order in lists.orders:
            print(len(order.tool))
            #print(order.tool[0])
