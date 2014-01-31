from main import app
from database import User

app.test_request_context().push()
for user in User.query.all():
  print user, user.openid
