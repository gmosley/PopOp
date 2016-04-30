from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Binary
from database import Base

class ImageSet(Base):
    __tablename__ = 'imagesets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, unique=False)
    tag = Column(String, unique=False, nullable=False)

    def __init__(self, user_id, description='No description', tag='Other'):
        self.user_id = user_id
        self.description = description
        self.tag = tag

    def __repr__(self):
        return '<ImageSet %d:(owner: %d description: %r)>' % (self.id, self.user_id, self.description)

class Reports(Base):
    __tablename__ = 'reports'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), primary_key=True)
    time = Column(DateTime, nullable=False)
    reason = Column(Integer, nullable=False)
    descrip = Column(String, nullable=True)

    def __init__(self, user_id, set_id, time, reason, descrip=''):
        self.user_id = user_id
        self.set_id = set_id
        self.time = time
        self.reason = reason
        if len(descrip) > 0:
            self.descrip = descrip

    def __repr__(self):
        return '<Report user:%d set:%d reason:%d>' %(self.user_id, self.set_id, self. reason)

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), nullable=False)
    address = Column(String, nullable=False)

    def __init__(self, set_id, address):
        self.set_id = set_id
        self.address = address
        self.reports = 0

    def __repr__(self):
        return '<Image(set: %d address: %r)>' % (self.set_id, self.address)

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), nullable=False)
    img1 = Column(Integer, ForeignKey('images.id'), nullable=False)
    img2 = Column(Integer, ForeignKey('images.id'), nullable=False)
    img3 = Column(Integer, ForeignKey('images.id'), nullable=False)
    perm_num = Column(Integer, nullable=False)
    done = Column(Boolean, nullable=False)

    def __init__(self, set_id, img1, img2, img3, perm_num=0):
        self.set_id = set_id
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.perm_num = perm_num
        self.done = False

    def __repr__(self):
        return '<Job %d:(set_id: %d done: %d)>' % (self.id, self.set_id, self.done)
        
class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    finish_time = Column(DateTime, nullable=False)
    first = Column(Integer, ForeignKey('images.id'), nullable=False)
    second = Column(Integer, ForeignKey('images.id'), nullable=False)
    third = Column(Integer, ForeignKey('images.id'), nullable=False)
    perm_num = Column(Integer, nullable=False)

    def __init__(self, set_id, worker_id, finish_time, first, second, third, perm_num=0):
        self.set_id = set_id
        self.worker_id = worker_id
        self.finish_time = finish_time
        self.first = first
        self.second = second
        self.third = third
        self.perm_num = perm_num

    def __repr__(self):
        return "<Result(1:%r 2:%r 3:%r finish_time:%r worker_id:%d set_id:%d)>" \
        % (self.first, self.second, self.third, self.finish_time, self.worker_id, self.set_id)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), nullable=False)
    password_hash = Column(String, nullable=False)
    points = Column(Integer, nullable=False)

    def __init__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.points = 0

    def __repr__(self):
        return '<User %r %r %d>' % (self.first_name, self.last_name, self.points)