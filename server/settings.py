import os

try:
  install_dir = os.environ['INSTALL_DIR']
except KeyError:
  import sys
  print >> sys.stderr, 'Set INSTALL_DIR environment variable!'
  sys.exit(1)

logfilename = '/tmp/todoer.log'
template_dir = os.path.join(install_dir, 'site', 'templates')
