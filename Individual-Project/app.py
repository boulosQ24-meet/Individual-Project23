from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from requests.exceptions import HTTPError

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


Config = {
  "apiKey": "AIzaSyBty7GOqEjD5JYl5_3X1sp_9ZpgbgkDIs8",
  "authDomain": "mini-project-72664.firebaseapp.com",
  "databaseURL": "https://mini-project-72664-default-rtdb.europe-west1.firebasedatabase.app/",
  "projectId": "mini-project-72664",
  "storageBucket": "mini-project-72664.appspot.com",
  "messagingSenderId": "375044386375",
  "appId": "1:375044386375:web:c634f54258d61e0bcd8b62",
  "measurementId": "G-PNKB0E976B"
  }

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": username,"email": email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except HTTPError as err:
            #check if the HTTPError message is displaying it will redirect me to login.html
            #bcuz this error accure when the account we are trying to create is already saved in the database
            if "\"message\": \"EMAIL_EXISTS\"" in str(err):
                return redirect(url_for('login'))
        except Exception as e:
            return render_template('signup.html')
    return render_template('signup.html')

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except Exception as e:
            return render_template('signup.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    auth.current_user = None
    login_session['user'] = None
    return redirect(url_for('signup'))


#Code goes below here
@app.route("/home" , methods = ['GET', 'POST'])
def home():
    if not login_session['user']:
        return redirect(url_for('signup'))
    # HERE

    if request.method=='POST':
        author = request.form['author']
        postt = request.form['quote']
        username = request.form['formUsername']
        try:
            # UID = login_session['user']['localId']
            qoutes = {"author": author,"qoute": postt, "username": username}
            db.child("Posts").push(qoutes)
            postss = db.child('Posts').get().val()
            return render_template("index.html", postss = postss)
        except:
            error = "error"
    postss = db.child('Posts').get().val()
    return render_template("index.html", postss = postss)




if __name__ == '__main__':
    app.run(debug=True)