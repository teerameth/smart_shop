#!/usr/bin/env python
# — coding: utf-8 —
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conversion import find_lastest #ใส่ list ของ datetimes เข้าไปเเล้วจะ return วันที่ล่าสุดออกมา
from conversion import new_date_time # Generate datetime ใน format ที่เราจะทำการเก็บ
from conversion import password_encode, password_verify #Password Hashing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Association(db.Model):
    __tablename__ = 'association'
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), primary_key=True)
    tool_group_id = db.Column(db.Integer, db.ForeignKey('tool_group.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    tool_group = db.relationship("Tool_group", back_populates="tools")
    tool = db.relationship("Tool", back_populates="tool_groups")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    student_university_ID = db.Column(db.String(11), nullable=False) # stored in format 613405000xx
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    student_type = db.Column(db.String(20), nullable=False) # 1=ป.ตรี, 2=ป.โท , 3=ป.เอก, 4=อาจารย์, 5=อื่นๆ
    student_year = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False) #stored in format 09xxxxxxxx
    lists = db.relationship('Tool_list', backref='owner')
    def verify_password(self, password): return password_verify(password, self.password)
    def edit_password(self, password):
        self.password = password_encode(password)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def get_id(self): return self.student_university_ID
    def edit_id(self, new_id):
        self.student_university_ID = new_id
        db.session.commit()
    def get_name(self): return self.name
    def edit_name(self, new_name):
        self.name = new_name
        db.session.commit()
    def get_surname(self): return self.surname
    def edit_surname(self, new_surname):
        self.surname = new_surname
        db.session.commit()
    def get_type(self): return self.student_type
    def edit_type(self, new_type):
        self.student_type = new_type
        db.session.commit()
    def get_year(self): return self.student_year
    def edit_year(self, new_year):
        self.student_year = new_year
        db.session.commit()
    def get_phone_number(self): return self.phone_number
    def edit_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number
        db.session.commit()
    def get_lists(self): return self.lists
    def get_lastest_list_by_create(self):
        datetimes = []
        for each_list in self.lists: datetimes.append(each_list.created_datetime)
        lastest = find_lastest(datetimes)
        return self.lists[lastest]
    def create_new_list(self): #Create new tool_list and auto fill datetime and return that tool_list
        new_list = Tool_list(owner = self, created_datetime = new_date_time(), stored = 0)
        db.session.add(new_list)
        db.session.commit()
        return new_list
    

    

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tool_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    total = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('tool_group.id'))
    tool_groups = db.relationship("Association", back_populates="tool")
    def edit_name(self, selected_tool, name):
        selected_tool.name = name
        db.session.commit()
    def edit_type(self, selected_tool, new_type):
        selected_tool.tool_type = new_type
        db.session.commit()
    def edit_description(self, selected_tool, new_description):
        selected_tool.description = new_description
        db.session.commit()
    def edit_total(self, selected_tool, new_total):
        selected_tool.total = new_total
        db.session.commit()
    def edit_stock(self, selected_tool, new_stock):
        selected_tool.in_stock = new_stock
        db.session.commit()
    def edit_picture(self, selected_tool, new_image_path):
        selected_tool.picture = new_image_path
        db.session.commit()
    def delete_tool(self, selected_tool):
        db.session.delete(selected_tool)
        db.session.commit()
    def add_suggestion(self, suggested_tool): #Add new suggestion tool and auto create group if didn't exist
        if self.group == None:
            group = Tool_group()
            self.group = group
        group = self.group
        # Check ว่ามี suggested_tool นั้นอยู่เเล้วมั้ยจะได้ไม่ใส่ซํ้า
        already = []
        for item in group.tools: already.append(item.tool) #group.tools เป็น Association ซึ่งมีสมาชิกที่เป็น Tool อยู่ด้านใน เรียกใช้ด้วย Association.tool
        if suggested_tool not in already: #To prevent duplication of suggested tool list
            a = Association()
            a.tool = suggested_tool
            group.tools.append(a) #เพื่ม Association ที่บรรจุ suggested_tool อันใหม่ไว้ใน group.tools
        else: print("Already has this tool in suggestion group")
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))
    tool = db.relationship("Tool")
    list_id = db.Column(db.Integer, db.ForeignKey('tool_list.id'))

class Tool_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Order', backref='list')
    created_datetime = db.Column(db.String(27), nullable=False) # stored in format dd:mm:yy-hh:mm:ss
    approved_status = db.Column(db.Integer) # default = 0
    approved_datetime = db.Column(db.String(27))
    returned_status = db.Column(db.Integer) # default = 0
    returned_datetime = db.Column(db.String(27))
    last_edited_datetime = db.Column(db.String(27))
    shared = db.Column(db.Integer) # สร้างเอง = 0, ถูกshareมา = 1
    shared_from_ID = db.Column(db.String(11)) # stored in format 613405000xx
    owner_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    stored = db.Column(db.Integer) #0 = normal, 1 = store (not shown)
    def list_all_tools(self): #return ออกมาในรูป list ของ tuple (Tool, amount)
        lists = []
        for each_order in db.session.query(Order).filter_by().all(): lists.append((each_order.tool[0], each_order.amount))
        return lists
    def add_new_tool(self, new_tool, amount):
        new_order = Order(tool = new_tool, amount = amount, list = self)# สร้าง Order สำหรับ Tool อันใหม่ที่ใส่เข้า tool_list เเล้วบอกว่าเป็นของ tool_list อันนี้
        db.session.add(new_order)
        db.session.commit()
    def share(self, student_id):
        new_list = Tool_list(owner=db.session.query(Student).filter_by(student_university_ID=student_id), tools=self.tools ,created_datetime=new_date_time(), shared=1, shared_from_ID=self.owner.student_university_ID)
        db.session.add(new_list)
        db.session.commit()
        return new_list
    def get_created_time(self): return self.created_datetime
    def set_created_datetime(self, new_datetime):
        self.created_datetime = new_datetime
        db.session.commit()
    def get_approved_status(self): return self.approved_status
    def get_approved_datetime(self): return self.approved_datetime
    def set_approved_status(self):
        if self.approved_status == 1: return False #already approved
        self.approved_status = 1
        self.approved_datetime = new_date_time()
        tools = db.session.query(Tool).filter_by().all()
        for order in self.orders:
            order.tool.in_stock -= order.amount
        db.session.commit()
    def cancle_approved_status(self):
        if self.approved_status == 0: return False #didn't approved yet
        self.approved_status = 0
        self.approved_datetime = None
        for order in self.orders:
            order.tool.in_stock += order.amount
        db.session.commit()
    def get_returned_status(self): return self.returned_status
    def get_returned_datetime(self): return self.returned_datetime
    def set_returned_status(self):
        if self.returned_status == 1: return False #already returned
        self.returned_status = 1
        self.returned_datetime = new_date_time()
        for order in self.orders:
            order.tool.in_stock += order.amount
        db.session.commit()
    def cancle_returned_status(self):
        if self.returned_status == 0: return False #didn't returned yet
        self.returned_status = 0
        self.returned_datetime = None
        for order in self.orders:
            order.tool.in_stock -= order.amount
        db.session.commit()
    def if_shared(self): return self.shared
    def get_owner(self): return self.owner
    def get_owner_id(self): return self.owner.student_university_ID
    def remove(self):
        db.session.delete(self)
        db.session.commit()
    def store(self):
        self.stored = 1
        db.session.commit()
    def update_datetime(self):
        self.last_edited_datetime = new_date_time()
        db.session.commit()

class Tool_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    main_tool = db.relationship('Tool', backref='group') #เป็น list ของ Tool (เเต่มีสมาชิกเเค่ตัวเดียว) ***อย่าลืมใส่ [0]
    tools = db.relationship("Association", back_populates="tool_group") # เป็น list ของ Association -> มี Tool อยู่ด้านในอีกที เรียกใช้ได้จาก Association.tool
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def main_tool(self): return self.main_tool
    def list_item(self):
        items_list = []
        for assoc in self.tools: items_list.append(assoc.tool)
        return items_list
    def list_item_name(self):
        items_name = []
        for assoc in self.tools: items_name.append(assoc.tool.name)
        return items_name
    def remove_tool(self, remove):
        for assoc in self.tools:
            if assoc.tool == remove: self.remove(assoc)
    def get_description(self): return self.description
    def edit_description(self, new_description):
        self.description = new_description
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
