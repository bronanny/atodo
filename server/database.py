import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


log = logging.getLogger('db')


db = SQLAlchemy()


class InvalidData(Exception):
  code = 500 # "Bunt" for now with an INTERNAL SERVER ERROR


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
  name = db.Column(db.String(50))
  openid = db.Column(db.String(200))
##  tz = db.Column(db.TZ())
  todos = db.relationship(
    "ToDo",
    order_by="desc(ToDo.priority)",
    primaryjoin="ToDo.user_id==User.id",
    )

  def __init__(self, name, openid):
    log.debug('Creating user %r', name)
    self.name = name
    self.openid = openid

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

  def get_jsoned_todos(self):
    return [todo.as_jsonish() for todo in self.todos]

  def get_todo(self, ID):
    return ToDo.query.filter_by(user_id=self.id, id=ID).first()

  def post_todo(self, body, priority, ID, due_date, due_tz, completed):
    td = self.get_todo(ID)
    if not td:
      td = ToDo(ID, self.id, priority, body, due_date, due_tz, completed)
    else:
      td.body = body
      td.priority = priority
      td.due_date = due_date
      td.due_tz = due_tz
      td.completed = completed
    db.session.add(td)
    db.session.commit()
    return td

  def del_todo(self, ID):
    td = ToDo.query.filter_by(user_id=self.id, id=ID).first()
    if td:
      db.session.delete(td)
      db.session.commit()
      return True
    return False


class ToDo(db.Model):

  __tablename__ = 'todo'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship(User, primaryjoin=user_id == User.id)
  priority = db.Column(db.Integer())
##  created_date = db.Column(db.DATE())
##  created_tz = db.Column(db.TZ())
  due_date = db.Column(db.Integer)
  due_tz = db.Column(db.String(10))
  body = db.Column(db.String(1024))
  completed = db.Column(db.Boolean())

  def __init__(self, ID, user_id, priority, body, due_date, due_tz, completed):
    log.debug('Creating ToDo %r', ID)
    self.id = ID
    self.user_id = user_id
    self.priority = priority
    self.body = body
    self.due_date = due_date
    self.due_tz = due_tz
    self.completed = completed

  def as_jsonish(self):
    return {
      'priority': self.priority,
      'body': self.body, # FIXME: encoding? HTML saftey?
      'sync': True,
      'ID': self.id,
      'due_date': '%i %s' % (self.due_date, self.due_tz),
      'completed': self.completed,
      }

  @classmethod
  def validate_data(class_, body, priority, ID, due_date, completed):
    try: ID = int(ID)
    except (TypeError, ValueError):
      raise InvalidData('non-numeric todo ID.')

    if False: # FIXME: validate incoming data
      raise InvalidData()
