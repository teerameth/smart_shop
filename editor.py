#!/usr/bin/env python
# — coding: utf-8 —
from database_setup import db, Tool_list, Student, Tool, Tool_group, Order
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
    def list_all(self):
        return db.session.query(Tool).filter_by().all()
    def list_by_type(self, selected_type):
        return db.session.query(Tool).filter_by(tool_type=selected_type).all()
    def get_name(self, selected_tool):
        return selected_tool.name
    def edit_name(self, selected_tool, name):
        try:
            selected_tool.name = name
            db.session.commit()
            return True
        except:
            print("Change name error. Not found in Database")
            return False
    def get_type(self, selected_tool):
        return selected_tool.tool_type
    def edit_type(self, selected_tool, new_type):
        try:
            selected_tool.tool_type = new_type
            db.session.commit()
            return True
        except:
            print("Change type error. Not found in Database")
            return False
    def get_description(self, selected_tool):
        return selected_tool.description
    def edit_description(self, selected_tool, new_description):
        try:
            selected_tool.description = new_description
            db.session.commit()
            return True
        except:
            print("Change description error. Not found in Database")
            return False
    def get_total(self, selected_tool):
        return selected_tool.total
    def edit_total(self, selected_tool, new_total):
        try:
            selected_tool.total = new_total
            db.session.commit()
            return True
        except:
            print("Change total error. Not found in Database")
            return False
    def get_stock(self, selected_tool):
        return selected_tool.in_stock
    def edit_stock(self, selected_tool, new_stock):
        try:
            selected_tool.in_stock = new_stock
            db.session.commit()
            return True
        except:
            print("Change stock error. Not found in Database")
            return False
    def get_picture(self, selected_tool):
        return selected_tool.picture
    def edit_picture(self, selected_tool, new_image_path):
        try:
            selected_tool.picture = new_image_path
            db.session.commit()
            return True
        except:
            print("Change image path error. Not found in Database")
            return False
    def create_new_tool(self, name, tool_type, description, total, in_stock, picture):
        tool = Tool(name=name, tool_type=tool_type, description=description, total=total, in_stock=in_stock, picture=picture)
        db.session.add(tool)
        db.session.commit()
        return tool
    def delete_tool(self, selected_tool):
        db.session.delete(selected_tool)
        db.session.commit()
    def get_group(self, selected_tool): #for suggestion system
        return selected_tool.group #return Tool_group
    def set_group_by_group_name(self, selected_tool, name):
        try:
            selected_tool.group = db.query(Tool_group).filter_by(name=name).one()
        except:
            print("Can't find group name: " + name + ".\n")

class Student_editor:
    def get_student_by_id(self, id):
        try:
            return db.query.filter_by(student_university_ID=id).one()
        except:
            print("ID not found")
            return False
    def get_id(self, selected_student):
        return selected_student.student_university_ID
    def edit_id(self, selected_student, new_student_university_ID):
        try:
            selected_student.student_university_ID = new_student_university_ID
            db.session.commit()
            return True
        except:
            print("Can't change student's ID")
            return False
    def get_name(self, selected_student):
        return selected_student.name
    def edit_name(self, selected_student, new_name):
        try:
            selected_student.name = new_name
            db.session.commit()
            return True
        except:
            print("Can't change student's name")
            return False
    def get_surname(self, selected_student):
        return selected_student.surname
    def edit_surname(self, selected_student, new_surname):
        try:
            selected_student.surname = new_surname
            db.session.commit()
            return True
        except:
            print("Can't change student's surname")
            return False
    def get_type(self, selected_student):
        return selected_student.student_type
    def edit_type(self, selected_student, new_type):
        try:
            selected_student.student_type = new_type
            db.session.commit()
            return True
        except:
            print("Can't change student's type")
            return False
    def get_year(self, selected_student):
        return selected_student.stuent_year
    def edit_year(self, selected_student, new_year):
        try:
            selected_student.student_year = new_year
            db.session.commit()
            return True
        except:
            print("Can't change student's year")
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
    def get_phone_number(self, selected_student):
        return selected_student.phone_number
    def edit_phone_number(self, selected_student, new_phone_number):
        try:
            selected_student.phone_number = new_phone_number
            db.session.commit()
            return True
        except:
            print("Can't change student's phone_number")
            return False
    def get_lists(self, selected_student):
        return selected_student.lists
    def get_lastest_list_by_create(self, selected_student):
        lists = selected_student.lists
        datetimes = []
        for each_list in lists:
            datetimes.append(each_list.created_datetime)
        lastest = find_lastest(datetimes)
        return lists[lastest]
    def create_new_student(self, password, student_university_ID, name, surname, student_type, student_year, phone_number):
        new_student = Student(password=password, student_university_ID=student_university_ID, name=name, surname=surname, student_type=student_type, student_year=student_year, phone_number=phone_number)
        db.session.add(new_student)
        db.session.commit()
        return new_student
class Tool_list_editor:
    def list_all_tools(self, selected_list):
        all = db.query(Order).filter_by().all()
        lists = []
        for each_order in all:
            lists.append((each_order.tool, amount))
        return selected_list.tools
    def add_new_tool(self, selected_list, selected_tool):
        new_order = Order(tool=selected_tool, amount=0)
        return new_order
    def create_new_list(self, student): #create new empty list + autoset created datetime and return that list
        new_list = Tool_list(owner=student, created_datetime=new_date_time())
        db.session.add(new_list)
        db.session.commit()
        return new_list
    def share_list(self, shared_list, student): #share shared_list to student + autoset shared datetime and return that list
        new_list = Tool_list(owner=student, tools=shared_list.tools ,created_datetime=new_date_time(), shared=1, shared_from_ID=shared_list.owner.student_university_ID)
        db.session.add(new_list)
        db.session.commit()
        return new_list
    def list_all_approved_lists(self):
        return db.query(Tool_list).filter_by(approved_status=1).all()
    def list_all_returned_lists(self):
        return db.query(Tool_list).filter_by(returned_status=1).all()
    def list_all_approved_but_not_returned_lists(self):
        return db.query(Tool_list).filter_by(approved_status=1, returned_status=0).all()
    def get_created_datetime(self, selected_list):
        return selected_list.created_datetime
    def set_created_datetime(self, selected_list, new_datetime):
        try:
            selected_list.created_datetime = new_datetime
            db.session.commit()
            return True
        except:
            print("Can't change created datetime")
            return False
    def get_approved_status(self, selected_list):
        return selected_list.approved_status
    def set_approved_status(self, selected_list):
        try:
            selected_list.approved_status = 1
            selected_list.approved_datetime = new_date_time()
            db.session.commit()
            return True
        except:
            print("Can't change approved status")
            return False
    def cancel_approved_status(self, selected_list):
        try:
            selected_list.approved_status = 0
            selected_list.approved_datetime = None
            db.session.commit()
            return True
        except:
            print("Can't change approved status")
            return False
    def get_returned_status(self, selected_list):
        return selected_list.returned_status
    def set_returned_status(self, selected_list):
        try:
            selected_list.returned_status = 1
            selected_list.returned_datetime = new_date_time()
            db.session.commit()
            return True
        except:
            print("Can't set returned status")
            return False
    def cancle_returned_status(self, selected_list):
        try:
            selected_list.returned_status = 0
            selected_list.returned_datetime = None
            db.session.commit()
            return True
        except:
            print("Can't cancle returned status")
            return False
    def if_shared(self, selected_list):
        return selected_list.shared
    def get_owner(self, selected_list):
        return selected_list.owner # return student object
    def get_owner_id(self, selected_list):
        return selected_list.owner.student_university_ID #return student id

class Tool_group_editor:
    def list_all_group(self):
        return db.query(Tool_group).filter_by().all()
    def find_group_by_name(self, name):
        return db.query(Tool_group),filter_by(name=name).one()
    def delete_group(self, selected_group):
        db.session.delete(selected_group)
        db.commit()
    def add_to_group(self, selected_tool, selected_group):
        selected_tool.group = selected_group
    def list_item_in_group(self, selected_group):
        return selected_group.tools
    def remove_from_group(selected_tool):
        selected_tool.group = None
    def create_new_group(self, name):
        new_group = Tool_group(name=name)
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