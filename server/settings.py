# MUST have set INSTALL_DIR environment variable.
import os
try:
  install_dir = os.environ['INSTALL_DIR']
except KeyError:
  import sys
  print >> sys.stderr, 'Set INSTALL_DIR environment variable!'
  sys.exit(1)


import logging.config
import log_config


in_production = 'sforman' not in install_dir # FIXME


logfilename = '/var/log/todoer.log' if in_production else '/tmp/todoer.log'
template_dir = os.path.join(install_dir, 'site', 'templates')
static_dir = os.path.join(install_dir, 'site', 'static')
flask_settings = {'template_folder': template_dir}
database_uri = 'EXPLODE!' if in_production else 'sqlite:////tmp/test.db'


logging.config.dictConfig(log_config.config(logfilename))


if not in_production:
  flask_settings['static_folder'] = static_dir


def configure_database(app, db):
  app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
  app.config['SQLALCHEMY_POOL_RECYCLE'] = 60 * 60 # Once an hour.
  db.init_app(app)

