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
    status = content()
    if request.method == 'GET':
        return render_template('login.html', status=status)
    elif request.method == 'POST':
        student_id = request.form['username_field']
        if student_id == "12345":
            return redirect(url_for('adminHome'))
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
    editor.get_tool_list_by_id(toollist_id).store()
    return redirect(url_for('allToolList', student_id = student_id))


@app.route('/user/<int:student_id>/<int:toollist_id>/edit')
def editToolList(student_id, toollist_id): #"Edit tool list and go to confirm"
    student = editor.get_student_by_id(str(student_id))
    status = content()
    alltool = editor.list_all_tool()
    toollist = editor.get_tool_list_by_id(toollist_id)
    toollist.update_datetime()
    basket = []
    have_stock = True
    for order in toollist.orders:
        basket.append(order.tool.id)
        if order.amount > order.tool.in_stock: have_stock = False #บอกวา่ของที่กดไว้ เกินจำนวนที่ยืมได้
    print(basket)
    return render_template('edit_tool_list.html', student = student , status=status , alltool=alltool , toollist=toollist, toollist_id = toollist_id, basket = basket, have_stock = have_stock)

@app.route('/user/<int:student_id>/<int:toollist_id>/<tool>/add_tool')
def add_tool(student_id, toollist_id,tool): #"add tool to list"
    toollist = editor.get_tool_list_by_id(toollist_id)
    this_tool = editor.get_tool_by_id(tool)
    basket = []
    for order in toollist.orders:
        basket.append(order.tool.id)
    if this_tool.id not in basket:
        toollist.add_new_tool(this_tool,1)
    return redirect(url_for('editToolList', student_id = student_id, toollist_id = toollist_id))

@app.route('/user/<int:student_id>/<int:toollist_id>/edit/<int:order_id>/<int:action>')
def edit_amount(student_id, toollist_id,order_id, action):
    toollist = editor.get_tool_list_by_id(toollist_id)
    for order in toollist.orders:
        if order.id == order_id:
            if action == 0: order.decrease() #minus
            elif action == 1: order.increase() #add
            elif action == 2: order.destroy() #destroy
            return redirect(url_for('editToolList', student_id = student_id, toollist_id = toollist_id))

@app.route('/user/<int:student_id>/<int:toollist_id>/confirm')
def submitToollist(student_id, toollist_id):
    student = editor.get_student_by_id(str(student_id))
    status = content()
    toollist = editor.get_tool_list_by_id(toollist_id)
    #return "Pick some additional suggested tool and submit"
    return render_template('submit_tool_list.html', student = student , status=status , toollist=toollist )

@app.route('/user/<int:student_id>/<int:toollist_id>/auto_adjust')
def auto_adjust(student_id, toollist_id):
    toollist = editor.get_tool_list_by_id(toollist_id)
    for order in toollist.orders: order.fit()
    return redirect(url_for('editToolList', student_id = student_id, toollist_id = toollist_id))
@app.route('/admin', methods = ['GET', 'POST'])
def adminHome(): #"Admin Home Page.\n Select between Approving & Editing"
    if request.method == 'GET':
        return render_template('adminhome.html')
    elif request.method == 'POST':
        student_id = request.form['username_field']
        return redirect(url_for('studentLists', student_id = student_id))

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
    #return "All student's lists sorted by datetime"
    student = editor.get_student_by_id(str(student_id))
    lists = student.lists
    status = content()
    return render_template('student_lists.html', student=student, lists=lists , status=status)

@app.route('/admin/<int:student_id>/<int:toollist_id>/approve')
def approveList(student_id, toollist_id):
    return "Edit selected list before approve"

@app.route('/admin/<int:student_id>/<int:toollist_id>/print')
def printList(student_id, toollist_id):
    return "Print approved list"

@app.route('/admin/<int:student_id>/<int:toollist_id>/PDF')
def allToolListPDF(student_id, toollist_id):
    student = editor.get_student_by_id(str(student_id))
    for item in student.lists:
        if item.id == toollist_id:
            tool_list = item
            break
    if request.method == 'GET':
        date_time = new_date_time()
        date = date_time[0:2] + "-" + date_time[3:5] + "-" + date_time[6:8]
        time = date_time[9:11] + ":" + date_time[12:14]
        return render_template('PDF.html', student=student, tool_list = tool_list, date = date, time = time)
    elif request.method == 'POST':
        return 'aaa'

@app.route('/admin/stock')
def toolStock():
    alltool = list(editor.list_all_tool())
    return render_template('managing_stock.html', alltool = alltool)
    # "Check stock of all tools"

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