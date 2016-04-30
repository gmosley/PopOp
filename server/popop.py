from flask import Flask, render_template, session, request, abort, redirect, url_for, flash
from werkzeug import secure_filename
import flask.ext.login as flask_login
import json
import os
import database
import boto
from Crypto.Hash import SHA256
from models import User as dbuser
from uuid import uuid4

app = Flask(__name__)
# needs to actually be secret in production
app.secret_key = 'swordfish'

# must be false in production
app.debug = True

# Login manager stuff
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    
    def __init__(self, email, first, last):
        self.id = email
        self.first_name = first
        self.last_name = last


@login_manager.user_loader
def user_loader(email):
    print "user loader"
    u = dbuser.query.filter(dbuser.email == email).first()
    if u:
        user = User(u.email, u.first_name, u.last_name)
        return user

# Routes

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    print "signup here"
    print request.form
    first = request.form['first_name']
    last = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    print (first, last, email, password)
    if len(first) > 0 and len(last) > 0 and len(email) > 0 and len(password) > 0:
        noerror, msg = database.signupUser(first, last, email, password)
        print (noerror, msg)
        if noerror:
            print "signed up user " + email
            return redirect(url_for('index'))
        print msg
        return json.dumps({'error': True, 'error-descrip':'This email has already been registered.'}), \
            400, {'ContentType':'application/json'}
    else:
        return json.dumps({'error': True, 'error-descrip':'Some fields are invalid.'}), 400, {'ContentType':'application/json'}

@app.route("/login", methods=['POST'])
def login():
    print "trying to login"
    email = request.form['email']
    password = request.form['password']
    u = database.validateLogin(email, password)
    print (email, password)
    print u
    if u:
        flash('Logged in!')
        user = User(u.email, u.first_name, u.last_name)
        flask_login.login_user(user)
    else:
        flash('Invalid username or password.')
    return redirect(url_for('index'))

@app.route("/logout", methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@app.route("/report", methods=['POST'])
def report():
    if 'set_id' in session:
        user_id = 1
        set_id = session['set_id']
        reason = request.form.get('reason')
        description = ""
        if(database.createReport(user_id, set_id, reason, description)):
            return 200
    return 400

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        if 'set_id' in session and 'job_id' in session:
            # record the vote
            database.createResult(session['job_id'], session['set_id'], 1, request.form['first'],
                request.form['second'], request.form['third'])
        else:
            abort(400) 
    
    # TODO: parse args to get tags

    # no matter what, get a new set of images
    result = database.getImagesforNextJob()
    print result
    if result:
        job_id, set_id, description, images = result
        session['job_id'] = job_id
        session['set_id'] = set_id
        return render_template('vote.html', description=description,
            img_1=images[0], img_2=images[1], img_3=images[2])

    return render_template('nomore.html')

# need to figure out file uploading

@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('dropzone.html')
    
    c = boto.connect_s3()
    b = c.get_bucket('popop-uploads')

    description = request.form.get('description')

    image_files = []
    for file_id in request.files:
        file = request.files[file_id]
        img_type = file.content_type.split('/')[1]
        if img_type in ['png', 'jpg', 'jpeg']:
            dst_file = uuid4().hex + '.' + img_type
            key = b.new_key(dst_file)
            key.content_type= file.content_type
            key.set_contents_from_string(file.read())
            key.set_acl('public-read')
            image_files.append('https://s3.amazonaws.com/popop-uploads/' + dst_file)

    if len(image_files) >= 3:
        set_id = database.newRequest(1, image_files, description)
        database.generateJobs(set_id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return "Not enough image files!", 400
    
if __name__ == "__main__":
    app.run()