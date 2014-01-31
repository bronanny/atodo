import logging
from flask import Flask, request, render_template
from settings import flask_settings, configure_database, login_url_fragment
from database import db
from oid_handling import oid, before_request, login, logout, login_required


log = logging.getLogger('todoer')


app = Flask('todoer', **flask_settings)
configure_database(app, db)
oid.init_app(app)
app.before_request(before_request)


@app.route('/')
@login_required
def index():
  return render_template('index.html')


app.route(login_url_fragment, methods=['GET', 'POST'])(login)
app.route('/logout')(logout)


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
