from flask import Flask
import pymysql
import pymysql.cursors
import datetime

#Initialize the app from Flask
app = Flask(__name__)
app.config.from_object('config')


#Configure MySQL
# For MAMP on Mac, add the port or unix_socket AND pwd = "root"
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='', # password for XMAPP
                       db='airline_service_db',
                       # port=5000,
                       unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Check that the two dates don't overlap
def validateDates(begintime, endtime):
    begindate = datetime.datetime.strptime(begintime, '%Y-%m-%dT%H:%M')
    enddate = datetime.datetime.strptime(endtime, '%Y-%m-%dT%H:%M')
    return begindate <= enddate
