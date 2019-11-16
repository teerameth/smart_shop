#!/usr/bin/env python
# — coding: utf-8 —
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def find_lastest(datetimes):
    date = []
    for i in range(len(datetimes)):
        string = datetimes[i] # stored in format dd:mm:yy-hh:mm:ss
        buff = ""
        buff += string[6:8]+string[3:5]+string[:2]+string[9:11]+string[12:14]+string[15:]
        date.append(buff)
    maximum = max(date)
    return date.index(maximum)
def new_date_time():
    buff = str(datetime.datetime.now())
    return buff[2:4] + ":" + buff[5:7] + ":" + buff[8:10] + "-" + buff[11:13] + ":" + buff[14:16] + ":" + buff[17:19]
            
            
class Editor:
###### Tool ######
    def list_all_tool(self): #return list ของ tool ทั้งหมด
        return db.session.query(Tool).filter_by().all()
    def list_all_type_of_tool(self): #return ชื่อ type ของ tool ทั้งหมด
        types = []
        for tool in db.session.query(Tool).filter_by().all():
            if tool.tool_type not in types: types.append(tool.tool_type)
        return types
    def list_tool_by_type(self, selected_type): #return list ของ tools ที่มี type ตรงกับที่ป้อนเข้าไป
        return db.session.query(Tool).filter_by(tool_type=selected_type).all()
    def create_new_tool(self, name, tool_type, description, total, in_stock, picture): #สร้าง tool ใหม่โดยบังคับใส่เเค่ name, tool_type, total, in_stock ที่เหลือใส่เป็น None ไปก่อนได้
        tool = Tool(name=name, tool_type=tool_type, description=description, total=total, in_stock=in_stock, picture=picture)
        db.session.add(tool)
        db.session.commit()
        return tool
###### Student ######
    def list_all_student(self): #return list ของ students ทั้งหมด
        return db.session.query(Student).filter_by().all()
    def list_student_by_type(self, selected_type):
        return db.session.query(Student).filter_by(student_type = selected_type)
    def get_student_by_id(self, ID): #ใส่รหัสนักศึกษา(เป็น String ขนาด 11) เเล้ว return object Student
        print(type(ID))
        try:
            return db.session.query(Student).filter_by(student_university_ID=str(ID)).one()
        except:
            print("ID not found")
            return False
    def increase_student_year(self):
        all = db.query(Student).filter_by().all()
        for each_student in all:
            each_student.student_year += 1
        db.session.commit()
    def decrease_student_year(self):
        all = db.query(Student).filter_by().all()
        for each_student in all:
            each_student.student_year -= 1
        db.session.commit()
    def create_new_student(self, password, student_university_ID, name, surname, student_type, student_year, phone_number):
        new_student = Student(password=password, student_university_ID=student_university_ID, name=name, surname=surname, student_type=student_type, student_year=student_year, phone_number=phone_number)
        db.session.add(new_student)
        db.session.commit()
        return new_student
###### Tool_list ######
    def get_tool_list_by_id(self, id):
        return db.session.query(Tool_list).filter_by(id = id).one()
    def list_all_approved_lists(self):
        return db.session.query(Tool_list).filter_by(approved_status=1).all()
    def list_all_returned_lists(self):
        return db.session.query(Tool_list).filter_by(returned_status=1).all()
    def list_all_approved_but_not_returned_lists(self):
        return db.session.query(Tool_list).filter_by(approved_status=1, returned_status=0).all()
###### Tool_group ######
    def list_all_group(self):
        return db.session.query(Tool_group).filter_by().all()