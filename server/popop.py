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
        user.id = u.id
        return user

@login_manager.unauthorized_handler
def unauthorized():

    # flash('You need to be logged in to view this page.')
    return redirect(url_for('login'))

# Routes

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    first = request.form['first_name']
    last = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    print (first, last, email, password)
    if len(first) > 0 and len(last) > 0 and len(email) > 0 and len(password) > 0:
        noerror, msg = database.signupUser(first, last, email, password)
        if noerror:
            user = User(email, first, last)
            flask_login.login_user(user)
            return redirect(url_for('index'))
        print msg
        return json.dumps({'error': True, 'error-descrip':'This email has already been registered.'}), \
            400, {'ContentType':'application/json'}
    else:
        return json.dumps({'error': True, 'error-descrip':'Some fields are invalid.'}), 400, {'ContentType':'application/json'}

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    print "trying to login"
    email = request.form['email']
    password = request.form['password']
    u = database.validateLogin(email, password)
    print (email, password)
    print u
    if u:
        user = User(u.email, u.first_name, u.last_name)
        flask_login.login_user(user)
        return request.args.get('next') or redirect(url_for('index'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('index'))

@app.route("/logout", methods=['POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@app.route("/report", methods=['POST'])
@flask_login.login_required
def report():
    print "works"
    if 'set_id' in session:
        user_id = "1"
        set_id = session['set_id']
        reason = request.form['reason']
        description = ""
        if(database.createReport(user_id, set_id, reason, description)):
            flask.flash("report successful")
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    abort(400)

@app.route("/vote", methods=['GET', 'POST'])
@flask_login.login_required
def vote():
    if request.method == 'POST':
        if 'set_id' in session and 'job_id' in session:
            # record the vote
            session['working'] = False
            database.createResult(session['job_id'], session['set_id'], flask_login.current_user.id, request.form['first'],
                request.form['second'], request.form['third'], session['perm_num'])
        else:
            abort(400)

    # no matter what, get a new set of images
    result = database.getImagesforNextJob(flask_login.current_user.id)
    print result
    if result:
        job_id, set_id, perm_num, description, images = result
        session['job_id'] = job_id
        session['set_id'] = set_id
        session['perm_num'] = perm_num
        session['working'] = True
        return render_template('vote.html', description=description,
            img_1=images[0], img_2=images[1], img_3=images[2])

    return render_template('nomore.html')

# need to figure out file uploading

@app.route("/upload", methods=['GET','POST'])
@flask_login.login_required
def upload():
    if request.method == 'GET':
        return render_template('dropzone.html')
    
    c = boto.connect_s3()
    b = c.get_bucket('popop-test')

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
            image_files.append('https://s3.amazonaws.com/popop-test/' + dst_file)

    if len(image_files) >= 3:
        set_id = database.newRequest(flask_login.current_user.id, image_files, description)
        database.generateJobs(set_id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return "Not enough image files!", 400


@app.route("/profile")
@flask_login.login_required
def profile():
    name = flask_login.current_user.first_name + " " + flask_login.current_user.last_name
    stats = database.getStatsForUser(1)#flask_login.current_user.id)
    print stats

    return render_template('profile.html', stats=stats)

if __name__ == "__main__":
    app.run()