from flask import Flask,render_template,request,redirect,url_for
import pymysql

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:170243809@localhost/dbshop
# db = sqlalchemy(app)

conn = pymysql.connect('localhost','root','170243809','dbshop')

@app.route("/")
def showData():
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM list")
        rows = cur.fetchall()
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
    app.run(debug=True)