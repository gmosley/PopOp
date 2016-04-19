# A walkthrough of our code:

We have 3 main chunks of code: the server code, database code, and client code.

## Server
Our server is written in Flask, since we thought it would fit well with what we've learned so far in NETS 213 (it's also super awesome and easy). There's really only one file to look at here:

#### `popop.py`
- The main server file. Talks with database and Amazon S3. Defines GET/POST routes for /vote and /upload. Run the server with python `popop.py`.

## Database
Our database code is split into two parts, `database.py` and `models.py`, along with a convinience file `make_database.py`. 
#### `database.py`
- Contains methods to access data and to create data.
#### `models.py`
- Defines an SQL schema. We have a User (not actively used), ImageSet, Image, Job, and Result. 
#### `make_database.py`
- Initializes a database and creates a user (Joe Doe), two image set requests, and the jobs for both image sets.

We used SQLAlchemy to create both these files, and we currently have a SQLite database, but we plan to migrate to PostgreSQL soon. 

## Client
Our Flask application does all the routing, so we can mainly focus on our HTML and CSS files. All the CSS files and statically served content is in `server/static/`.
#### `dropzone.html`
- Simply hooks up `dropzone.js` and allows users to upload images, which we route to our server and then upload to S3. We plan to do content control with this later,i.e. nuditity checking.
#### `homepage.html`
- Nothing much here, just a home page!
#### `vote.html`
- A _beautifully_ designed HIT which asks users to rank a set of 3 images. Users can drag to reorder them with some help form the jQueryUI library. We plan to add an image viewer in later as well.