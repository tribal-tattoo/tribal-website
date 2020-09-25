import os
from flask import Flask, render_template, request, redirect
# from flask_compress import Compress
import urllib.request
from flask import g
import firebase_admin
from firebase_admin import credentials,firestore
from flask_mail import Mail,Message
import time
from datetime import date

# <script async>(function(w, d) { w.CollectId = "5d33527bbbe93a2116d19d38"; var h = d.head || d.getElementsByTagName("head")[0]; var s = d.createElement("script"); s.setAttribute("type", "text/javascript"); s.setAttribute("src", "https://collectcdn.com/launcher.js"); h.appendChild(s); })(window, document);</script>

cred = credentials.Certificate("tribal-tattoo-ae837-firebase-adminsdk-em2bs-c5b3a1bd5a.json")
defaultApp = firebase_admin.initialize_app(cred)
db = firestore.client()

salt = "TwinFuries"

app=Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tribalwebsitemys@gmail.com'
app.config['MAIL_PASSWORD'] = 'Tribal@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# Compress(app)
# Compress(app)

@app.route("/",methods=['POST','GET'])
def home() : 
	upcomingEvent = ""
	upcomingBlog =""
	message=""
	doc_ref = db.collection(u'events').where(u'complete',"==", "false").get()
	doc_ref2 = db.collection(u'blogs').where(u'complete',"==", "false").get()
	eventList = {}
	blogList ={}
	for doc in doc_ref:
		eventList[doc.id] = doc.to_dict()
	for doc in doc_ref2:
		blogList[doc.id] = doc.to_dict()
	if len(eventList) == 0:
		upcomingEvent = "No Upcoming Events"
	if len(blogList) == 0:
		upcomingBlog = "No Blogs Posted"
	if request.method== 'POST':
		name = request.form['name']
		artist = request.form['artist']
		date = request.form['date']
		time = request.form['time']
		email = request.form['email']
		phNum = request.form['phNum']
		doc_id = email + " " + date
		doc_ref = db.collection(u'appointments').document(doc_id)
		doc_ref.set({
			u'name':name,
			u'contact':phNum,
			u'date':date,
			u'artist':artist,
			u'time':time,
			u'email':email
		})
		msg = Message('Booking Confirmation', sender = 'tribaltattoont@gmail.com', recipients = [email])
		msg.body = "Your booking has been registered. We will contact you shortly"
		mail.send(msg)
		message = "Booking Submitted, Check your mail for confirmation"
		return render_template("index2.html", message=message, bloggy=blogList, upcomingBlog= upcomingBlog, events=eventList, upcomingEvent = upcomingEvent)
	return render_template("index2.html", message=message, bloggy=blogList, upcomingBlog= upcomingBlog, events=eventList, upcomingEvent = upcomingEvent)
	
@app.route("/404")
def not404():
	return render_template("404.html")
	
@app.route("/about")
def about() : 
	return render_template("about.html")

@app.route("/achievements")
def achievement() : 
	return render_template("achievement.html")

@app.route("/services",methods=['POST','GET'])
def services() : 
	message=""
	if request.method== 'POST':
		name = request.form['name']
		artist = request.form['artist']
		date = request.form['date']
		time = request.form['time']
		email = request.form['email']
		phNum = request.form['phNum']
		doc_id = email + " " + date
		doc_ref = db.collection(u'appointments').document(doc_id)
		doc_ref.set({
			u'name':name,
			u'contact':phNum,
			u'date':date,
			u'artist':artist,
			u'time':time,
			u'email':email
		})
		msg = Message('Booking Confirmation', sender = 'tribaltattoont@gmail.com', recipients = [email])
		msg.body = "Your booking has been registered. We will contact you shortly"
		mail.send(msg)
		message = "Booking Submitted, Check your mail for confirmation"
		return render_template("service3.html", message=message)
	return render_template("service3.html", message=message)
	

@app.route("/project")
def project() : 
	return render_template("project.html")

# @app.route("/booking")
# def booking() : 
# 	return render_template("booking.html")

@app.route("/booking",methods=['POST','GET'])
def booking():
	message=""
	if request.method== 'POST':
		name = request.form['name']
		artist = request.form['artist']
		date = request.form['date']
		time = request.form['time']
		email = request.form['email'] if request.form['email'] else ""
		phNum = request.form['phNum']
		doc_id = phNum + " " + date
		doc_ref = db.collection(u'appointments').document(doc_id)
		
		doc_ref.set({
			u'name':name,
			u'contact':phNum,
			u'date':date,
			u'artist':artist,
			u'time':time,
			u'email':email
		})
		if email != "":
			msg = Message('Booking Confirmation', sender = 'tribalwebsitemys@gmail.com', recipients = [email])
			msg.body = "Your booking has been registered. We will contact you shortly"
			mail.send(msg)
		message = "Booking Submitted, Check your mail (if given) for confirmation"
		return render_template("booking.html", message=message)
	return render_template("booking.html", message=message)



@app.route("/shop")
def shop() : 
	return render_template("shop.html")

@app.route("/team")
def team() : 
	return render_template("team.html")

@app.route("/portfolio")
def portfolio() : 
	return render_template("team2.html")

@app.route("/contact")
def contact() : 
	return render_template("contact.html")

@app.route("/portfolioPraveen")
def portfolioPraveen() : 
	return render_template("portfolioPraveen.html")

@app.route('/portfolioChaitra')
def portfolioChaitra():
	return render_template('portfolioChaitra.html')

@app.route("/consult", methods=['POST','GET'])
def consult():
	message = ""
	if request.method == "POST":
		fullName = request.form['name']
		email = request.form['email']
		phNum = request.form['phNum']
		curDate = date.today()
		doc_ref = db.collection(u'consultations').document(fullName + "  " + curDate.strftime("%Y-%m-%d"))
		doc_ref.set({
			u'name':fullName,
			u'email':email,
			u'phNum':phNum
		})
		message = "Information Submitted, we will contact you shortly"
		return render_template("index2.html", message = message)
	return render_template("index2.html", message = message)

@app.route("/portfolioSohel")
def portfolioSohel() : 
	return render_template("portfolioSohel.html")

@app.route("/portfolioSomanna")
def portfolioSomanna() : 
	return render_template("portfolioSomanna.html")


@app.route("/events")
def events() : 
	noPost = ""
	doc_ref = db.collection(u'events').get()
	eventList = {}
	for doc in doc_ref:
		eventList[doc.id] = doc.to_dict()
	if len(eventList) == 0:
		noPost = "No events as of yet. Stay tuned!"
	return render_template("events.html",events=eventList, noPost = noPost)


@app.route("/blog")
def blogs() : 
	noPost = ""
	doc_ref = db.collection(u'blogs').get()
	blogList = {}
	for doc in doc_ref:
		blogList[doc.id] = doc.to_dict()
	if len(blogList) == 0:
		noPost = "No posts as of now. Stay tuned!"
	return render_template("blog.html",blogs=blogList, noPost = noPost)


@app.route("/register/<event>",methods=['POST','GET'])
def register(event = None) : 
	message=""
	doc_ref = db.collection(u'events').document(event).get()
	
	doc = doc_ref.to_dict()
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		phNum = request.form['phNum']
		dob = request.form['dob']
		address = request.form['address']
		# doc_id = email + " " + date
		col_ref = db.collection(u'events').document(event)
		doc_ref = col_ref.collection(u'registrations').document(email)
		doc_ref.set({
			u'name':name,
			u'contact':phNum,
			u'email':email,
			u'dob':dob,
			u'address':address
		})
		user_ref = db.collection(u'users').document()
		user_ref.set({
			u'name':name,
			u'contact':phNum,
			u'date':str(int(dob.split('-')[2])) + "-" + str(int(dob.split('-')[1]))
		})
		msg = Message('Registration Confirmation', sender = 'tribaltattoont@gmail.com', recipients = [email])
		msg.body = "Congratulations, your registration for the event " + event.split(" ")[0] + " on " + event.split(" ")[1] +" has been confirmed"
		mail.send(msg)
		message = "Booking Submitted, Check your mail for confirmation"
		return render_template("register.html", event=event, message=message, eventData=doc)
	return render_template("register.html", event=event, message=message, eventData=doc)



@app.route("/blogDetails/<blog>",methods=['POST','GET'])
def blogDetails(blog = None) : 
	message=""
	doc_ref = db.collection(u'blogs').document(blog).get()
	doc = doc_ref.to_dict()
	return render_template("blogDetails.html", eventData=doc)


if __name__ == "__main__":
    app.run(debug=True,threaded=True)