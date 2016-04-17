from flask import Flask, render_template, request, abort
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        # record the vote
        pass
        
    # get a job from DB
    # return a rendered template with images
    abort(418)

if __name__ == "__main__":
    app.run(debug=True)
