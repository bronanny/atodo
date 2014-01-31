import os

try:
  install_dir = os.environ['INSTALL_DIR']
except KeyError:
  import sys
  print >> sys.stderr, 'Set INSTALL_DIR environment variable!'
  sys.exit(1)


in_production = 'sforman' not in install_dir # FIXME


logfilename = '/tmp/todoer.log'
template_dir = os.path.join(install_dir, 'site', 'templates')
static_dir = os.path.join(install_dir, 'site', 'static')
flask_settings = {'template_folder': template_dir}


if not in_production:
  flask_settings['static_folder'] = static_dir


