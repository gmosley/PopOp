from flask import Flask, render_template, session, request, abort
from werkzeug import secure_filename
import json
import os
import database
import boto
from uuid import uuid4

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# needs to actually be secret in production
app.secret_key = 'swordfish' 

# must be false in production
app.debug = True


@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        if 'job_id' in session:
            # record the vote
            database.createResult(session['job_id'], 1, request.form['first'],
                request.form['second'], request.form['third'])
        else:
            abort(400) 
    
    # TODO: parse args to get tags

    # no matter what, get a new set of images
    job_id, description, images = database.getImagesforNextJob()
    session['job_id'] = job_id
    return render_template('vote.html', description=description,
        img_1=images[0], img_2=images[1], img_3=images[2])

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

    if image_files:
        set_id = database.newRequest(1, image_files, description)
        database.generateJobs(set_id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    abort(400)
    


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route("/target", methods=['POST'])
# def upload():
#     print request.files
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         # TODO: add requestid or cookie to filename
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         print filename
#         return json.dumps({'success':True, 'filename': filename}), 200, {'ContentType':'application/json'}
#         # TODO: extra file parsing - resize, conversion, nudity
#     else:
#         return json.dumps({'error': "BAD REQUEST"}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run()
