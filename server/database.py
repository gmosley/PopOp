from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
engine = create_engine('sqlite:///./db/database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

from models import ImageSet, Image, Job, Result, User

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
        return False

# Generate a list of jobs for a given ImageSet
# Returns: True if success, False otherwise
def generateJobs(imageset_id):
    MIN_JOBS = 10
    MAX_JOBS = 50
    try:
        images = Image.query.with_entities(Image.id).filter(Image.set_id == imageset_id).all()
        for i in xrange(0,len(images) - 2):
            job = Job(imageset_id, images[i][0], images[i + 1][0], images[i + 2][0])
            db_session.add(job)
        db_session.commit()
        return True
    except Exception, e:
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
        return False