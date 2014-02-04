import logging
from flask import g, jsonify, request, abort
from database import ToDo, InvalidData


log = logging.getLogger('todoer')


def todos():
  log.debug('Fetching todos for %s', repr(g.user))
  return jsonify(todos=g.user.get_jsoned_todos())


def todo(ID):
  if request.method == 'GET':
    return GET_todo(ID)
  assert request.method == 'POST', repr(request.method)
  return PUT_or_POST_todo(ID)


def PUT_or_POST_todo(ID, log=log):
  args = todo_args_from_request()
  if args['ID'] != ID:
    log.error('ID %r not equal ID %r', args['ID'], ID)
    abort(500)
  log.debug('setting todo ID: %s for user %s', ID, repr(g.user))
  try:
    return jsonify(todo=g.user.post_todo(**args).as_jsonish())
  except: # A lot can go wrong here.
    log.exception('setting todo ID: %s for user %s', ID, repr(g.user))
    abort(500)


def GET_todo(ID, log=log):
  try: ID = int(ID)
  except ValueError:
    log.error('non-numeric todo ID: %r for user: %s', ID, repr(g.user))
    abort(404)
  log.debug('getting todo ID: %s for user %s', ID, repr(g.user))
  td = g.user.get_todo(ID)
  if not td:
    log.warning('unknown todo ID: %s for user: %s', ID, repr(g.user))
    abort(404)
  log.debug('got todo ID: %s for user: %s', ID, repr(g.user))
  return jsonify(todo=td.as_jsonish())


def parse_due_date(date_string):
  try:
    epoch, timezone = date_string.split(None, 1)
    try: epoch = int(epoch)
    except (TypeError, ValueError):
      raise InvalidData('Bad epoch! %r' % (epoch,))
    return epoch, timezone
  except:
    log.exception()
    abort(500)


def todo_args_from_request():
  body = request.form.get('body')
  priority = request.form.get('priority')
  ID = request.form.get('ID')
  due_date, due_tz = parse_due_date(request.form.get('due_date', ''))
  completed = request.form.get('completed') == 'true'
  try:
    ToDo.validate_data(body, priority, ID, due_date, completed)
  except InvalidData, err:
    log.error('Invalid FORM Data %s todo ID: %s for user %s', err, ID, repr(g.user))
    abort(err.code)
  return locals()
