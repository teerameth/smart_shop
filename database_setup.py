#!/usr/bin/env python
# — coding: utf-8 —
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    password = db.Column(db.String(100), nullable=False)
    student_university_ID = db.Column(db.String(11), nullable=False) # stored in format 613405000xx
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    student_type = db.Column(db.String(20), nullable=False) # 1=ป.ตรี, 2=ป.โท , 3=ป.เอก, 4=อาจารย์, 5=อื่นๆ
    student_year = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False) #stored in format 09xxxxxxxx
    lists = db.relationship('Tool_list', backref='owner')
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

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
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    def edit_name(self, selected_tool, name):
        try:
            selected_tool.name = name
            db.session.commit()
            return True
        except: print("Change name error. Not found in Database")
    def edit_type(self, selected_tool, new_type):
        try:
            selected_tool.tool_type = new_type
            db.session.commit()
            return True
        except: print("Change type error. Not found in Database")
    def edit_description(self, selected_tool, new_description):
        try:
            selected_tool.description = new_description
            db.session.commit()
            return True
        except: print("Change description error. Not found in Database")
    def edit_total(self, selected_tool, new_total):
        try:
            selected_tool.total = new_total
            db.session.commit()
            return True
        except: print("Change total error. Not found in Database")
    def edit_stock(self, selected_tool, new_stock):
        try:
            selected_tool.in_stock = new_stock
            db.session.commit()
            return True
        except: print("Change stock error. Not found in Database")
    def edit_picture(self, selected_tool, new_image_path):
        try:
            selected_tool.picture = new_image_path
            db.session.commit()
            return True
        except: print("Change image path error. Not found in Database")
    def delete_tool(self, selected_tool):
        db.session.delete(selected_tool)
        db.session.commit()
    def add_suggestion(self, suggested_tool):
        if self.group == None:
            group = Tool_group()
            self.group = group
        group = self.group
        # Check ว่ามี suggested_tool นั้นอยู่เเล้วมั้ยจะได้ไม่ใส่ซํ้า
        already = []
        for item in group.tools: already.append(item.tool) #group.tools เป็น Association ซึ่งมีสมาชิกที่เป็น Tool อยู่ด้านใน เรียกใช้ด้วย Association.tool
        if suggested_tool not in already:
            a = Association()
            a.tool = suggested_tool
            group.tools.append(a) #เพื่ม Association ที่บรรจุ suggested_tool อันใหม่ไว้ใน group.tools
        else: print("Already has this tool in suggestion group")
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
    description = db.Column(db.String(1000))
    main_tool = db.relationship('Tool', backref='group')
    tools = db.relationship("Association", back_populates="tool_group")

if __name__ == '__main__':
    db.create_all()
