#!/usr/bin/env python
# — coding: utf-8 —
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from datetime import datetime
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
    def __init__(self):
        self.tool = Tool_editor()
        self.student = Student_editor()
        self.tool_list = Tool_list_editor()
        self.tool_group = Tool_group_editor()

class Tool_editor:
    def list_all(self): #return list ของ tool ทั้งหมด
        return db.session.query(Tool).filter_by().all()
    def list_all_type(self): #return ชื่อ type ของ tool ทั้งหมด
        types = []
        for tool in db.session.query(Tool).filter_by().all():
            if tool.tool_type not in types: types.append(tool.tool_type)
        return types
    def list_by_type(self, selected_type): #return list ของ tools ที่มี type ตรงกับที่ป้อนเข้าไป
        return db.session.query(Tool).filter_by(tool_type=selected_type).all()
    def create_new_tool(self, name, tool_type, description, total, in_stock, picture): สร้าง tool ใหม่โดยบังคับใส่เเค่ name, tool_type, total, in_stock ที่เหลือใส่เป็น None ไปก่อนได้
        tool = Tool(name=name, tool_type=tool_type, description=description, total=total, in_stock=in_stock, picture=picture)
        db.session.add(tool)
        db.session.commit()
        return tool

class Student_editor:
    def list_all(self): #return list ของ students ทั้งหมด
        return db.session.query(Student).filter_by().all()
    def get_student_by_id(self, ID): #ใส่รหัสนักศึกษา(เป็น String ขนาด 11) เเล้ว return object Student
        try:
            return db.session.query(Student).filter_by(student_university_ID=str(ID)).one()
        except:
            print("ID not found")
            return False
    
            selected_student.surname = new_surname
            db.session.commit()
            return True
        except:
            print("Can't change student's surname")
            return False
    def increase_year(self):
        all = db.query.filter_by().all()
        for each_student in all:
            each_student.student_year += 1
        db.session.commit()
    def decrease_year(self):
        all = db.query.filter_by().all()
        for each_student in all:
            each_student.student_year -= 1
        db.session.commit()
    def create_new_student(self, password, student_university_ID, name, surname, student_type, student_year, phone_number):
        new_student = Student(password=password, student_university_ID=student_university_ID, name=name, surname=surname, student_type=student_type, student_year=student_year, phone_number=phone_number)
        db.session.add(new_student)
        db.session.commit()
        return new_student
class Tool_list_editor:
    def list_all_approved_lists(self):
        return db.query(Tool_list).filter_by(approved_status=1).all()
    def list_all_returned_lists(self):
        return db.query(Tool_list).filter_by(returned_status=1).all()
    def list_all_approved_but_not_returned_lists(self):
        return db.query(Tool_list).filter_by(approved_status=1, returned_status=0).all()


class Tool_group_editor:
    def list_all_group(self):
        return db.query(Tool_group).filter_by().all()
    def find_group_by_name(self, name):
        return db.query(Tool_group).filter_by(name=name).one()
    def delete_group(self, selected_group):
        db.session.delete(selected_group)
        db.commit()
    def add_to_group(self, selected_tool, selected_group):
        selected_tool.group = selected_group
    def list_item_in_group(self, selected_group):
        return selected_group.tools
    def remove_from_group(self, selected_tool):
        selected_tool.group = None
    def create_new_group(self):
        new_group = Tool_group()
        db.session.add(new_group)
        db.session.commit()
        return new_group
    def get_name(self, selected_group):
        return selected_group.name
    def set_name(self, selected_group, new_name):
        try:
            selected_group.name = new_name
            db.session.commit()
            return True
        except:
            print("Can't change group's name")
            return False
    def get_description(self, selected_group):
        return selected_group.description
    def set_description(self, selected_group, new_description):
        try:
            selected_group.description = new_name
            db.session.commit()
            return True
        except:
            print("Can't change group's description")
            return False