from flask import Flask,render_template,request, url_for, redirect, session
import string
import random
import os

import twitter_sentiment
import db

pyBot = db.Database()

req_image = os.path.join('static', 'img')

app=Flask(__name__)
app.secret_key = "teamblu"

def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    x = ''.join(random.choice(chars) for _ in range(size))
    return x

@app.route('/')
def index():
	if 'username' in session:
		return render_template("index.html", session=session)
	else:
		return redirect(url_for('log_in'))

@app.route('/login')
def log_in():
	if 'username' in session:
		session['login'] = "signed_in"
		return redirect(url_for('index'))
	return render_template("login.html")

@app.route('/validate', methods=["POST"])
def validate():
	username = request.form["username"]
	password = request.form["password"]
	check_user = pyBot.con_auth(username, password)
	if check_user == None:
		return render_template("nouser.html")
	else:
		session['username'] = username
		session['login'] = "signed_in"
		session['name'] = check_user["name"]
		return redirect(url_for('index'))

@app.route('/genid', methods=["POST"])
def id_gen():
	usertext = request.form["usertext"]
	no_tweets = request.form["no_tweets"]
	no_tweets = int(no_tweets)
	unique_id = id_generator()
	twitter_sentiment.checksentiment(unique_id, usertext, no_tweets)
	pyBot.insertid(unique_id, session["username"])
	return render_template("showid.html", unique_id=unique_id)

@app.route('/haveid')
def haveid():
	return render_template("haveid.html")

@app.route('/showgraph', methods=["POST"])
def show():
	un_id = request.form["userid"]
	img_name = un_id+".png"
	for files in os.walk(req_image):
		if img_name in files[2]:
			checkid = pyBot.check_id(un_id)
			img_path = os.path.join(req_image, img_name)
			return render_template("showgraph.html", img_name=img_path, checkid=checkid)
		else:
			return render_template("noimage.html")

@app.route('/register', methods=["POST"])
def register():
	name = request.form["name"]
	contact = request.form["contact"]
	email = request.form["email"]
	username = request.form["username"]
	password = request.form["password"]
	try:
		pyBot.register_user(name, contact, email, username, password)
		return render_template("registered.html", username=username)
	except:
		return render_template("error.html")

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('login', None)
	session.pop('name', None)
	return redirect(url_for('log_in'))

if __name__=='__main__':
	app.run(debug=True)