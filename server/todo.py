import logging
from flask import g, jsonify


log = logging.getLogger('todoer')


def todos():
  log.debug('Fetching todos for %s', repr(g.user))
  return jsonify(todos=g.user.todos)
