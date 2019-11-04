from flask import Flask,render_template,request,redirect,url_for
import pymysql
from flask_sqlalchemy import SQLAlchemy
from database_setup import *
from editor import Editor
from gen_student import * 
import sqlite3
from conversion import password_encode, password_verify

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:170243809@localhost/dbshop
# db = sqlalchemy(app)

# conn = pymysql.connect('localhost','root','170243809','dbshop')
editor = Editor()

@app.route("/")
def showData():
    # with conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM list")
    #     rows = cur.fetchall()
    return render_template('index.html',datas = rows)

@app.route("/add")
def showFrom():
    return render_template('add.html')

@app.route("/delete/<string:id_data>",methods=['GET'])
def delete(id_data):
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM `list` WHERE `order`=%s",(id_data))
        conn.commit()
    return redirect(url_for('showData'))

@app.route("/insert",methods=['POST'])
def insert():
    if request.method=="POST":
        namelist = request.form['list']
        num = request.form['num']
        with conn.cursor() as cursor:
            sql="INSERT INTO `list`(`list`, `num`) VALUES (%s,%s)"
            cursor.execute(sql,(namelist,num))
            conn.commit()
    return redirect(url_for('showData'))

if __name__ == "__main__":
    # app.debug = True
    # app.run(host='0.0.0.0', port=5000)
    st = editor.get_student_by_id("61340500068")
    print(st.name)
