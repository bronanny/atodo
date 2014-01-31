from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import logging


log = logging.getLogger('db')


db = SQLAlchemy()


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
  name = db.Column(db.String(50))
  password = db.Column(db.String(12))
##  tz = db.Column(db.TZ())
  todos = db.relationship(
    "ToDo",
    order_by="desc(ToDo.priority)",
    primaryjoin="ToDo.user_id==User.id",
    )
  def __init__(self, name, password):
    log.debug('Creating user %r', name)
    self.name = name
    self.password = password

  def __repr__(self):
    return "<User(%r)>" % (self.name)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    assert self.id is not None
    return unicode(self.id)


class ToDo(db.Model):

  __tablename__ = 'todo'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship(User, primaryjoin=user_id == User.id)
  priority = db.Column(db.Integer())
##  created_date = db.Column(db.DATE())
##  created_tz = db.Column(db.TZ())
##  due_date = db.Column(db.DATE())
##  due_tz = db.Column(db.TZ())
  body = db.Column(db.String(1024))
