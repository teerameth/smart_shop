#!/usr/bin/env python
# — coding: utf-8 —
from flask import Flask, request, redirect, url_for, jsonify, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
from editor import Editor
from conversion import new_date_time, password_verify
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'  
UPLOAD_FOLDER = './static/picture' 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path='/picture')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
editor = Editor()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return editor.get_student_by_id(user_id)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def content():
	text = open('status.txt', 'r')
	status = text.read()
	text.close()
	return status

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    status = content()
    if request.method == 'GET':
        return render_template('login.html', status=status)
    elif request.method == 'POST':
        student_id = request.form['username_field']
        password = request.form['password_field']
        if student_id == "admin": return redirect(url_for('adminHome'))
        user = load_user(student_id)
        if password_verify(password, editor.get_student_by_id(student_id).password):
            login_user(user)
            print("Login")
            return redirect(url_for('allToolList', status = status, student_id = student_id))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/test')
def test():
    status = content()
    return render_template('test.html', status = status)

@app.route('/status')
def getUpdate():
    text = open('status.txt', 'r')
    status = text.read()
    text.close()
    return jsonify(status=status)

@app.route('/resetpassword')
def resetPassword():
    return "For user that forgot their password"

@app.route('/register')
def register():
    return "For new user"

@app.route('/user/<int:student_id>', methods = ['GET', 'POST'])
@login_required
def allToolList(student_id):
    if(current_user.is_authenticated and editor.get_student_by_id(student_id).id == current_user.id):
        student = editor.get_student_by_id(str(student_id))
        lists = student.lists
        status = content()
        if request.method == 'GET':
            return render_template('mainmenu.html', student=student, lists=lists , status=status)
        elif request.method == 'POST':
            return 'aaa'
    else: return redirect(url_for('logout'))

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

@app.route('/user/<int:student_id>/<int:toollist_id>/view')
def viewToolList(student_id, toollist_id): #"Edit tool list and go to confirm"
    student = editor.get_student_by_id(str(student_id))
    status = content()
    toollist = editor.get_tool_list_by_id(toollist_id)
    return render_template('view_tool_list.html', student = student , status=status, toollist=toollist, toollist_id = toollist_id)


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
    if request.method == 'GET':
        student = editor.get_student_by_id(str(student_id))
        for tool_list in student.lists:
            if tool_list.id == toollist_id:
                date_time = new_date_time()
                date = date_time[0:2] + "-" + date_time[3:5] + "-" + date_time[6:8]
                time = date_time[9:11] + ":" + date_time[12:14]
                return render_template('PDF.html', student=student, tool_list = tool_list, date = date, time = time)
        

@app.route('/admin/stock')
def toolStock():
    alltool = list(editor.list_all_tool())
    return render_template('managing_stock.html', alltool = alltool)
    # "Check stock of all tools"

@app.route('/admin/stock/<int:tool_id>')
def toolStatus(tool_id):
    return "Check specific tool status ว่าอยู่ที่ใครบ้าง ยืมไปตอนไหน"

@app.route('/admin/stock/new', methods=['GET', 'POST'])
def createTool():
    # typee=''
    # numm=''
    # tooll=list(editor.list_all_tool())
    # for i in range(0,len(tooll)) :
    #     if tooll[i].id==2 :
    #         typee+=str(i)
    # #return typee
    # ###########################################
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('xx.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''  
    #return "Create new tool and redirect to editTool()"
    
@app.route('/admin/stock/<int:tool_id>/edit', methods=['GET', 'POST'])
def editTool(tool_id):
    this_tool = editor.get_tool_by_id(tool_id)
    if request.method == 'GET':
        approved_lists = editor.list_all_approved_lists()
        table = [] #index: 0=datetime, 1=name&surname, 2=year, 3=number, 4=status
        for approved_list in approved_lists:
            buffer = []
            for order in approved_list.orders:
                if order.tool.id == tool_id:
                    buffer.append(approved_list.approved_datetime)
                    buffer.append(approved_list.owner.name + " " + approved_list.owner.surname)
                    buffer.append(approved_list.owner.student_university_ID)
                    buffer.append(order.amount)
                    if approved_list.returned_status == 1:
                        buffer.append("คืนแล้ว")
                    else:
                        buffer.append("ยังไม่คืน")
                    table.append(buffer)
                    continue
        return render_template('tool_id_edit.html', this_tool = this_tool, table = table)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(tool_id)+'.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('tool_id_edit.html', this_tool = this_tool)

@app.route('/admin/stock/<int:tool_id>/edit/group')
def editToolGroup(tool_id):
    return "Edit tool's group (เเสดง tools ทั้งหมดเลยยกเว้นตัวมันเอง)"

@app.route('/admin/stock/<int:tool_id>/delete')
def deleteTool(tool_id):
    return "Delete tool and auto redirect to toolStock()"



if __name__ == '__main__':
    app.secret_key = "11111111"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)#Change port to 80 before deploying