#!/usr/bin/env python
# — coding: utf-8 —
from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from editor import Editor
from conversion import new_date_time
import os

app = Flask(__name__, static_url_path='/pitcure')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
editor = Editor()

def content():
	text = open('status.txt', 'r')
	content = text.read()
	text.close()
	return content

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        student_id = request.form['username_field']
        return redirect(url_for('allToolList', student_id = student_id))

@app.route('/resetpassword')
def resetPassword():
    return "For user that forgot their password"

@app.route('/register')
def register():
    return "For new user"

@app.route('/user/<int:student_id>', methods = ['GET', 'POST'])
def allToolList(student_id):
    student = editor.get_student_by_id(str(student_id))
    lists = student.lists
    status = content()
    if request.method == 'GET':
        return render_template('mainmenu.html', student=student, lists=lists , status=status)
    elif request.method == 'POST':
        return 'aaa'

@app.route('/user/<int:student_id>/<int:toollist_id>/share')
def shareToolList(student_id, toollist_id):
    return  "{0} ใส่รหัสนักศึกษาเพื่อ Share tool list {1}".format(student_id, toollist_id)

@app.route('/user/<int:student_id>/new')
def createToolList(student_id):
    new_toollist = editor.get_student_by_id(student_id).create_new_list()
    return redirect(url_for('editToolList', student_id = student_id, toollist_id = str(new_toollist.id)))

@app.route('/user/<int:student_id>/<int:toollist_id>/delete')
def deleteToolList(student_id, toollist_id):
    editor.get_tool_list_by_id(toollist_id).remove()
    return redirect(url_for('allToolList', student_id = student_id))

# pitcure = os.path.join('static','P')
# app.config['UPLOAD_FOLDER'] = pitcure
@app.route('/user/<int:student_id>/<int:toollist_id>/edit')
def editToolList(student_id, toollist_id): #"Edit tool list and go to confirm"
    student = editor.get_student_by_id(str(student_id))
    # Pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'1.jpg')
    return render_template('edit_tool_list.html', student = student)

@app.route('/user/<int:student_id>/<int:toollist_id>/confirm')
def submitToollist(student_id,  toollist_id):
    return "Pick some additional suggested tool and submit"

@app.route('/admin')
def adminHome():
    return "Admin Home Page.\n Select between Approving & Editing"

@app.route('/admin/history')
def history():
    return "All History will be shown here by datetime or enter student's ID"

@app.route('/admin/history/approved')
def approvedHistory():
    return "All Approved lists history will be shown here by datetime"

@app.route('/admin/history/returned')
def returnedHistory():
    return "All returned lists history will be shown here by datetime"

@app.route('/admin/<int:student_id>')
def studentLists(student_id):
    return "All student's lists sorted by datetime"

@app.route('/admin/<int:student_id>/<int:toollist_id>/approve')
def approveList(studentLists, toollist_id):
    return "Edit selected list before approve"

@app.route('/admin/<int:student_id>/<int:toollist_id>/print')
def printList(studentLists, toollist_id):
    return "Print approved list"

@app.route('/user/<int:student_id>/PDF')
def allToolListPDF(student_id):
    student = editor.get_student_by_id(str(student_id))
    lists = student.lists
    if request.method == 'GET':
        date_time = new_date_time()
        date = date_time[0:2] + "-" + date_time[3:5] + "-" + date_time[6:8]
        time = date_time[9:11] + ":" + date_time[12:14]
        return render_template('PDF.html', student=student, lists=lists, date = date, time = time)
    elif request.method == 'POST':
        return 'aaa'

@app.route('/admin/stock')
def toolStock():
    return "Check stock of all tools"

@app.route('/admin/stock/<int:tool_id>')
def toolStatus(tool_id):
    return "Check specific tool status ว่าอยู่ที่ใครบ้าง ยืมไปตอนไหน"

@app.route('/admin/stock/new')
def createTool():
    return "Create new tool and redirect to editTool()"

@app.route('/admin/stock/<int:tool_id>/edit')
def editTool(tool_id):
    return "Edit tool's information and have link to edit tool's suggestion group"

@app.route('/admin/stock/<int:tool_id>/edit/group')
def editToolGroup(tool_id):
    return "Edit tool's group (เเสดง tools ทั้งหมดเลยยกเว้นตัวมันเอง)"

@app.route('/admin/stock/<int:tool_id>/delete')
def deleteTool(tool_id):
    return "Delete tool and auto redirect to toolStock()"



if __name__ == '__main__':
    # app.secret_key = "11111111"
    app.debug = True
    app.run(host='0.0.0.0', port=80)#Change port to 80 before deploying