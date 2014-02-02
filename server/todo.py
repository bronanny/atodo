import logging
from flask import g, jsonify, request, abort
from database import InvalidData


log = logging.getLogger('todoer')


def todos():
  log.debug('Fetching todos for %s', repr(g.user))
  return jsonify(todos=g.user.get_jsoned_todos())


def todo(ID):
  try:
    ID = int(ID)
  except ValueError:
    log.error('non-numeric todo ID: %r', ID)
    abort(404)

  if request.method == 'GET':
    td = g.user.get_todo(ID)
    if not td:
      log.warning('unknown todo ID: %s', ID)
      abort(404)
    log.debug('todo ID: %s', ID)
    return jsonify(todo=td.as_jsonish())

  assert request.method == 'POST', repr(request.method)

  log.debug('posting todo ID: %s for user %s', ID, repr(g.user))
  try:
    result = g.user.post_todo(
      body=request.form.get('body'),
      priority=request.form.get('priority'),
      ID=ID,
      )
  except InvalidData, err:
    log.error('posting todo ID: %s for user %s', ID, repr(g.user))
    abort(err.code)
  except:
    log.exception('posting todo ID: %s for user %s', ID, repr(g.user))
    abort(500)

  return jsonify(todo=result.as_jsonish())
