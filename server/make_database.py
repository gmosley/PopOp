# import files and create database
# note: you must delete the old database before running this
import database
database.init_db()
import models

from database import db_session

# create a user. for now, this is our only user
u = models.User("joe", "doe", "email@seas.upenn.edu", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3")
# objects must be added and commited to the database
db_session.add(u)
db_session.commit()

# create a image set of logos
i1 = models.ImageSet(u.id, "Vote by the best logo")
db_session.add(i1)
db_session.commit()

# add logos to the image set
img1 = models.Image(i1.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/logos/arch.png")
img2 = models.Image(i1.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/logos/centos.png")
img3 = models.Image(i1.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/logos/fedora.png")
img4 = models.Image(i1.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/logos/ubuntu.png")

db_session.add(img1)
db_session.add(img2)
db_session.add(img3)
db_session.add(img4)
db_session.commit()

i2 = models.ImageSet(u.id, "CATS CATS CATS")
db_session.add(i2)
db_session.commit()

img1 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat1.jpg")
img2 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat2.jpg")
img3 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat3.jpg")
img4 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat4.jpg")
img5 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat5.jpg")
img6 = models.Image(i2.id, "https://raw.githubusercontent.com/gmosley/PopOp/master/data/aggregation/photos/cat6.jpg")

db_session.add(img1)
db_session.add(img2)
db_session.add(img3)
db_session.add(img4)
db_session.add(img5)
db_session.commit()

# generate jobs
database.generateJobs(i1.id)
database.generateJobs(i2.id)