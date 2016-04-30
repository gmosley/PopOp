import csv
import database
from models import ImageSet, Image, Job, Result, User
from collections import defaultdict

print '''import database
database.init_db()
import models

from database import db_session

# create a user. for now, this is our only user
u = models.User("joe", "doe", "email@seas.upenn.edu", "password")
# objects must be added and commited to the database
db_session.add(u)
db_session.commit()'''

mapping = defaultdict(list)

with open('images.csv', 'rb') as images_csv:
    images = csv.DictReader(images_csv)
    for image in images:
        mapping[image['set_id']].append(image['address'])


with open('imagesets.csv', 'rb') as imagesets_csv:
    imagesets = csv.DictReader(imagesets_csv)
    for imageset in imagesets:
        print '\nimgset = models.ImageSet(u.id, "{}")'.format(imageset['description'])
        print 'db_session.add(imgset)'
        print 'db_session.commit()'
        for url in mapping[imageset['id']]:
            print 'img = models.Image(imgset.id, "{}")'.format(url)
            print 'db_session.add(img)'
        print 'db_session.commit()'
        print 'database.generateJobs(imgset.id)'
