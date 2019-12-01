from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from editor import Editor
editor = Editor()
from random import randint
from conversion import new_date_time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

students = editor.list_all_student()
tools = editor.list_all_tool()
print(tools[0].name)

def gen(mode):
    for student in students:
        print(student.name)
        print(student.student_university_ID)
        new_list = student.create_new_list()
        new_list.update_datetime()
        new_list.add_new_tool(tools[randint(0,30)], randint(1,3))
        new_list.add_new_tool(tools[randint(20,50)], randint(1,3))
        new_list.add_new_tool(tools[randint(31,60)], randint(1,3))
        if(mode == 1):
            new_list.approved_status = 1
            new_list.approved_datetime = new_date_time()
            new_list.returned_status = 1
            new_list.returned_datetime = new_date_time()
        else:
            new_list.approved_status = 0
            new_list.returned_status = 0


gen(1)
gen(0)
gen(0)

# student = editor.get_student_by_id(61340500032)
# db.session.query(Student).filter_by(student_university_ID=str(61340500032)).one()[0].name

# for lit in student.get_lists():
#     for order in lit.orders:
#         print(order.tool.name, order.amount)
# new_list = student.create_new_list()
# new_list.add_new_tool(tools[10], 3)

# #######################################
# for student in students:
#     print(student.name)
#     for lists in student.get_lists():
#         for order in lists.orders:
#             print(order.tool.name)
#             print(order.amount)
#             #print(order.tool[0])
