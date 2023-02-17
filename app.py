from flask import Flask, render_template, request, redirect # 導入模組Flask
from datetime import datetime
app = Flask(__name__)  # 呼叫Flask的固定用法


# Connect MySQL
import mysql.connector
mydb = mysql.connector.connect(
  host = "127.0.0.1",
  user = "allen",
  password = "Tw746201",
  database = "CUSTOMER",
  )
cursor=mydb.cursor()

@app.route("/")
def customerTable():
    sqlStuff = "select * from Customer"
    cursor.execute(sqlStuff)
    customerInfo=cursor.fetchall()

    return render_template('table.html',customerInfo=customerInfo)

@app.route("/create")
def create():
    customerInfo=[]
    return render_template('index.html',customerInfo=customerInfo)

@app.route("/edit/<serial_no>")
def edit(serial_no):
    sqlStuff = "select * from Customer where serial_no = " + serial_no
    cursor.execute(sqlStuff)
    customerInfo=cursor.fetchone()

    return render_template('index.html',customerInfo=customerInfo)


@app.route("/submit", methods=['POST'])
def submit():
    name = request.values['name']
    idno = request.values['idno']
    checkin = request.values['checkin']
    if(checkin):
        checkin = datetime.strptime(request.values['checkin'], '%d/%m/%Y').strftime('%Y-%m-%d')
    checkout = request.values['checkout']
    if(checkout):
        checkout = datetime.strptime(request.values['checkout'], '%d/%m/%Y').strftime('%Y-%m-%d')
    days = request.values['days']
    gender = request.values['gender']
    room_no = request.values['room_no']
    phone = request.values['phone']
    address = request.values['address']
    remark = request.values['remark']

    sqlStuff = "INSERT INTO Customer (id, name, checkin, checkout, days, gender, room_no, phone, address, remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    if (request.values['serial_no'] != ""):
        sqlStuff = "UPDATE Customer SET id=%s, name=%s, checkin=%s, checkout=%s, days=%s, gender=%s, room_no=%s, phone=%s, address=%s, remark=%s WHERE serial_no="+request.values['serial_no']

    records = (idno, name, checkin, checkout, days, gender, room_no, phone, address, remark)
    cursor.execute(sqlStuff, records)
    mydb.commit()

    return redirect("/");

if __name__ == "__main__":  # 如果主程式執行
    app.run()  # 啟動伺服器