from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
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

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), nullable=False)
    reports = Column(Integer, nullable=False)
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
    done = Column(Boolean, nullable=False)

    def __init__(self, set_id, img1, img2, img3):
        self.set_id = set_id
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.done = False

    def __repr__(self):
        return '<Job %d:(set_id: %d done: %d)>' % (self.id, self.set_id, self.done)

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('imagesets.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    finish_time = Column(DateTime, nullable=False)
    first = Column(Integer, ForeignKey('images.id'), nullable=False)
    second = Column(Integer, ForeignKey('images.id'), nullable=False)
    third = Column(Integer, ForeignKey('images.id'), nullable=False)

    def __init__(self, set_id, worker_id, finish_time, first, second, third):
        self.set_id = set_id
        self.worker_id = worker_id
        self.finish_time = finish_time
        self.first = first
        self.second = second
        self.third = third

    def __repr__(self):
        return "<Result(1:%r 2:%r 3:%r finish_time: %r worker_id:%r)>" \
        % (self.first) % (self.second) % (self.third, self.finish_time, self.worker_id)

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
        return '<User %r>' % (self.name)