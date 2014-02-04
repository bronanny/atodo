import logging
from json import dumps
from flask import Flask, render_template, g
from settings import (
  flask_settings,
  configure_database,
  login_url_fragment,
  js_source,
  )
from database import db
from oid_handling import (
  oid,
  before_request,
  login,
  logout,
  login_required,
  guard,
  )
from todo import todos, todo
from api import configure_api


log = logging.getLogger('todoer')


app = Flask('todoer', **flask_settings)
configure_database(app, db)
oid.init_app(app)
app.before_request(before_request)
configure_api(app)


@app.route('/')
@login_required
def index():
  return render_template(
    'index.html',
    js_source=js_source,
    username=g.user.name,
    )


app.route(login_url_fragment, methods=['GET', 'POST'])(login)
app.route('/logout')(logout)


app.route('/todos')(guard(todos))
app.route('/todo/<ID>', methods=['GET', 'POST'])(guard(todo))


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
