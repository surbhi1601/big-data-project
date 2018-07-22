#!/bin/python

import cgi
import mysql.connector as mysql

#connection between html page and python
print "Content-type: text/html\n\n"
data=cgi.FieldStorage()

username=data.getvalue('usname')
password=data.getvalue('passwd')


#connecting mysql database to python
connection=mysql.connect(user='root', password='123',host='localhost', database='adhoc2')
cur=connection.cursor()


cur.execute("select Username,Pssword from register where Username=%s AND Pssword=%s",(username,password))
output=cur.fetchall()
value=len(output) 
if value == 0:
	print "login unsuccessful"
	 
else:
	print "login successful"
	print "<meta http-equiv='refresh' content='2; url=http://localhost/home.html'>"




