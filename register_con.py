#!/bin/python

import cgi
import mysql.connector as mysql


#connection between html page and python
print "Content-type: text/html\n\n"
data=cgi.FieldStorage()

fname=data.getvalue('fname')
lname=data.getvalue('lname')
email=data.getvalue('email')
contact=data.getvalue('contact')
username=data.getvalue('usname')
password=data.getvalue('passwd')


	connection=mysql.connect(user='root', password='123',host='localhost', database='adhoc2')
	cur=connection.cursor()
	connection.commit()

cur.execute("select Contact from register where contact=?", (contact,))
data = cur.fetchall()
if data is None:
        print ('not found')
else:
        print ('found')

#connecting mysql database to python

cur.execute("insert into register(First_name,Last_name,Contact,Email,Username,Pssword)values(%s,%s,%s,%s,%s,%s)",(fname,lname,contact,email,username,password))
print "Inserted into table"
connection.commit()

