from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import math
import pandas as pd
app = Flask(__name__) 

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
      return redirect("/page/0");

@app.route("/page/<pageOffset>")
def customerTableByPage(pageOffset):
    sqlCount = "select count(*) from Customer"
    cursor.execute(sqlCount)
    count = cursor.fetchone()[0]
    pageCount = math.ceil(count/10);

    if pageOffset == None or int(pageOffset) < 0:
        pageOffset = 0
    if int(pageOffset) > pageCount:
        pageOffset = pageCount
    dataOffset = str(int(pageOffset)*10)
    
    sqlStuff = "select * from Customer limit " + dataOffset + ",10"
    cursor.execute(sqlStuff)
    customerInfo=cursor.fetchall()

    return render_template('table.html',customerInfo=customerInfo,pageCount=pageCount,count=count,pageOffset=int(pageOffset))

@app.route("/search/<condition>/page/<pageOffset>")
def search(condition,pageOffset):
    condition = condition.split("&")

    sqlCount = "select count(*) from Customer where " + condition[0] + "='" + condition[1] +"'"
    cursor.execute(sqlCount)
    count = cursor.fetchone()[0]
    pageCount = math.ceil(count/10);

    if pageOffset == None or int(pageOffset) < 0:
        pageOffset = 0
    if int(pageOffset) > pageCount:
        pageOffset = pageCount
    dataOffset = str(int(pageOffset)*10)

    sqlStuff = "select * from Customer where " + condition[0] + "='" + condition[1] +"' limit " + dataOffset + ",10"
    cursor.execute(sqlStuff)
    customerInfo=cursor.fetchall()

    return render_template('table.html',customerInfo=customerInfo,pageCount=pageCount,count=count,pageOffset=int(pageOffset))

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
    else:
        checkin = None
    checkout = request.values['checkout']
    if(checkout):
        checkout = datetime.strptime(request.values['checkout'], '%d/%m/%Y').strftime('%Y-%m-%d')
    else:
        checkout = None
    gender = request.values['gender']
    room_no = request.values['room_no']
    phone = request.values['phone']
    address = request.values['address']
    remark = request.values['remark']
    price = int(request.values['price'])

    if checkin != None and checkout != None:
        days = (datetime.strptime(request.values['checkout'], '%d/%m/%Y')-datetime.strptime(request.values['checkin'], '%d/%m/%Y')).days
    else:
        days = 0

    sqlStuff = "INSERT INTO Customer (id, name, checkin, checkout, days, gender, room_no, phone, address, remark, price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    if (request.values['serial_no'] != ""):
        sqlStuff = "UPDATE Customer SET id=%s, name=%s, checkin=%s, checkout=%s, days=%s, gender=%s, room_no=%s, phone=%s, address=%s, remark=%s, price=%s WHERE serial_no="+request.values['serial_no']

    records = (idno, name, checkin, checkout, days, gender, room_no, phone, address, remark, price)
    cursor.execute(sqlStuff, records)

    mydb.commit()

    return redirect("/");

@app.route("/exportCondition")
def exportCondition():
    return render_template('export.html')

@app.route("/export", methods=['POST'])
def export():
    startDate = request.values['startDate']
    if(startDate):
        startDate = datetime.strptime(request.values['startDate'], '%d/%m/%Y').strftime('%Y-%m-%d')
    else:
        startDate = "1997-1-1"
    endDate = request.values['endDate']
    if(endDate):
        endDate = datetime.strptime(request.values['endDate'], '%d/%m/%Y').strftime('%Y-%m-%d')
    else:
        endDate = datetime.today().strftime('%Y-%m-%d') 
    sqlStuff = "select id, name, checkin, checkout, days, gender, room_no, phone, address, remark, price from Customer where checkin between '" + startDate + "' and '" + endDate + "'" 
    cursor.execute(sqlStuff)
    data=cursor.fetchall()

    idList = []
    nameList = []
    checkinList = []
    checkoutList = []
    daysList = []
    genderList = []
    room_noList = []
    phoneList = []
    addressList = []
    remarkList = []
    priceList = []
    for id, name, checkin, checkout, days, gender, room_no, phone, address, remark, price in data:
        idList.append(id)
        nameList.append(name)
        checkinList.append(checkin)
        checkoutList.append(checkout)
        daysList.append(days)
        genderList.append(gender)
        room_noList.append(room_no)
        phoneList.append(phone)
        addressList.append(address)
        remarkList.append(remark)
        priceList.append(price)

    dic = {'身分證字號':idList, '名字':nameList, '入住時間':checkinList, '退房時間':checkoutList, '幾晚':daysList, '性別':genderList, '房號':room_noList, '金額':priceList, '電話':phoneList, '地址':addressList, '備註':remarkList}
    df = pd.DataFrame(dic)
    df.to_csv('/home/pickle88662213373/customer-information/csv/customer' + startDate + 'to' + endDate + '.csv')
    return redirect("/download/customer" + startDate + "to" + endDate + ".csv")

@app.route('/download/<file>')
def downloadFile (file):
    path = "/home/pickle88662213373/customer-information/csv/"+file
    return send_file(path, as_attachment=True)

if __name__ == "__main__":  # 如果主程式執行
    app.run()  # 啟動伺服器