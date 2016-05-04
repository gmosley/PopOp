from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from Crypto.Hash import SHA256

import itertools
import math
import random

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
engine = create_engine('sqlite:///./db/database_2.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

from models import ImageSet, Image, Job, Result, User, Reports


def signupUser(first_name, last_name, email, password):
    does_exist = User.query.filter(User.email == email).first()
    if not does_exist:
        phash = SHA256.new(password).hexdigest()
        print (password, phash)
        u = User(first_name, last_name, email, phash)
        db_session.add(u)
        db_session.commit()
        return (u.id, '')
    else:
        return (False, 'This email has already been taken.')

def validateLogin(email, password):
    u = User.query.filter(User.email == email).first()
    if u:
        phash = SHA256.new(password).hexdigest()
        print (password, phash)
        print u.password_hash
        if phash == u.password_hash:
            clone = User(u.first_name, u.last_name, u.email, '')
            return clone
    return False

# Expects owner id, list of image addresses, and a description.
# Returns: id of newly created ImageSet, false if failed
def newRequest(owner, image_addresses, description):
    try:
        imageset = ImageSet(owner, description)
        db_session.add(imageset)
        db_session.commit()
        for addr in image_addresses:
            image = Image(imageset.id, addr)
            db_session.add(image)
        db_session.commit()
        return imageset.id
    except Exception, e:
        print e
        return False

# create report and commit it to database
# Returns: True if success, False otherwise 
# reason is 0 for nudity, 1 for offensive, 2 for no images
def createReport(user_id, set_id, reason, descrip):
    try:
        report = Reports(user_id, set_id, datetime.now(), reason, descrip)
        db_session.add(report)
        db_session.commit()
        return True
    except Exception, e:
        print e
        return False


# Generate a list of jobs for a given ImageSet
# Returns: True if success, False otherwise
def generateJobs(imageset_id):
    MIN_JOBS = 10
    MAX_JOBS = 50
    try:
        images = Image.query.with_entities(Image.id).filter(Image.set_id == imageset_id).all()

        all_jobs = []
        combinations = list(enumerate(itertools.combinations(range(len(images)), 3)))
        num_combinations = len(combinations)

        multiplier, extra = divmod(MIN_JOBS, num_combinations)

        if multiplier > 0:
            for i in xrange(multiplier):
                all_jobs.extend(combinations)
            random.shuffle(combinations)
            all_jobs.extend(combinations[:extra])
        else:
            random.shuffle(combinations)
            all_jobs.extend(combinations[:min(MAX_JOBS, num_combinations)])

        for (p_id, (i1, i2, i3)) in all_jobs:
            job = Job(imageset_id, images[i1][0], images[i2][0], images[i3][0], p_id)
            db_session.add(job)
        db_session.commit()
        return True
    except Exception, e:
        print e
        return False

# Gets images for next availiable job
# Takes in a tag, which is empty by default
# Returns: List of image addresses, False if failed
def getImagesforNextJob(tag=''):
    try:
        job = Job.query.filter(Job.done == False).first()
        description = ImageSet.query.with_entities(ImageSet.description).filter(ImageSet.id == job.set_id).first()[0]
        images = []
        images.append(Image.query.with_entities(Image.address).filter(Image.id == job.img1).first()[0])
        images.append(Image.query.with_entities(Image.address).filter(Image.id == job.img2).first()[0])
        images.append(Image.query.with_entities(Image.address).filter(Image.id == job.img3).first()[0])
        return (job.id, job.set_id, description, images)
    except Exception, e:
        print e
        return False

# Create a result, expects job id, worker id, and the order
# of the images.
# Returns: The id of the result, or False if failed
def createResult(job_id, set_id, worker_id, first, second, third):
    try:
        job = Job.query.filter(Job.id == job_id).first()
        job.done = True
        finish_time = datetime.now()
        result = Result(set_id, worker_id, finish_time, first, second, third)

        db_session.add(job)
        db_session.add(result)
        db_session.commit()
        return result.id
    except Exception, e:
        print e
        return False

# Gets image sets owned by a user.
# Returns: A list of tuples in the format (set_id, user_id, description, tag)
def getStatsForUser(user_id):
    try:
        image_sets = ImageSet.query.filter(ImageSet.user_id == user_id).all()
        stats = []
        for image_set in image_sets:
            jobs = Job.query.filter(Job.set_id == image_set.id).all()
            jobcount = len(jobs)
            complete = 0
            for job in jobs:
                if job.done:
                    complete += 1
            print str(complete) + "/" + str(jobcount) + " complete"
            stats.append({
                'description': image_set.description,
                'jobcount': jobcount,
                'complete': complete})
        return stats
    except Exception, e:
        print e
        return False