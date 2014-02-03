import os, unittest, tempfile
import main
from database import db, User


class TestTest(unittest.TestCase):

  def setUp(self):
    if not main.app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite://'):
      raise RuntimeError('Test against sqlite DB! not %r'
                         % main.app.config['SQLALCHEMY_DATABASE_URI'])
    main.app.config['TESTING'] = True
    main.app.debug = True
    main.app.test_request_context().push()
    db.drop_all()
    db.create_all()
    self.app = main.app.test_client()

  def tearDown(self):
    pass

  def create_user(self, name='ed', openid='oooiiidddddddd'):
    u = User(name, openid)
    db.session.add(u)
    db.session.commit()
    return u

  def test_hello(self):
    rv = self.app.get('/')
    self.assertTrue('Hello World!' in rv.data)

  def test_create_user(self):
    ed = self.create_user()
    users = User.query.all()
    self.assertTrue(ed in users)
    self.assertTrue(len(users) == 1)

  def test_api_get(self):
    ed = self.create_user()
    ed.post_todo('body', 0, 0)
    rv = self.app.get('/api/todo/0')
    print rv.data
    self.assertTrue('Hello World!' in rv.data)


if __name__ == '__main__':
    unittest.main()
