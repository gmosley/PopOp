from flask import Flask, render_template, request, abort
from werkzeug import secure_filename
import json
import os
import database

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        # record the vote
        abort(418)
        pass

    job_id, images = database.getImagesforNextJob()
    return render_template('vote.html', job_id=job_id, img_1=images[0], img_2=images[1], img_3=images[2])
    # get a job from DB
    # return a rendered template with images
    abort(418)

@app.route("/upload")
def create_job():
    return render_template('dropzone.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/target", methods=['POST'])
def upload():
    print request.files
    file = request.files['file']
    if file and allowed_file(file.filename):
        # TODO: add requestid or cookie to filename
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print filename
        return json.dumps({'success':True, 'filename': filename}), 200, {'ContentType':'application/json'}
        # TODO: extra file parsing - resize, conversion, nudity
    else:
        return json.dumps({'error': "BAD REQUEST"}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run()
