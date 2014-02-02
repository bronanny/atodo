import logging
from json import dumps
from flask import Flask, render_template, Markup, g
from settings import (
  flask_settings,
  configure_database,
  login_url_fragment,
  kolib,
  uslib,
  zplib,
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


log = logging.getLogger('todoer')


app = Flask('todoer', **flask_settings)
configure_database(app, db)
oid.init_app(app)
app.before_request(before_request)


@app.route('/')
@login_required
def index():
  return render_template(
    'index.html',
    username=g.user.name,
    todos=dumps(g.user.get_jsoned_todos()),
    kolib=Markup(kolib),
    uslib=Markup(uslib),
    zplib=Markup(zplib),
    )


app.route(login_url_fragment, methods=['GET', 'POST'])(login)
app.route('/logout')(logout)


app.route('/todos')(guard(todos))
app.route('/todo/<ID>', methods=['GET', 'POST'])(guard(todo))


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
