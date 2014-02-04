import logging
from flask import g, jsonify, request, abort
from flask.ext.restful import Resource, Api
from todo import GET_todo, PUT_or_POST_todo


log = logging.getLogger('api')


def configure_api(app, api_url='/api'):
  api = Api(app)
  api.add_resource(TodoAPI, api_url + '/todo/<int:ID>')


class TodoAPI(Resource):

  def get(self, ID):
    return GET_todo(ID, log)

  def put(self, ID):
    if not g.user.get_todo(ID):
      log.warning('unknown todo ID: %s for user: %s', ID, repr(g.user))
      abort(404)
    return PUT_or_POST_todo(ID, log)

  def post(self, ID):
    if g.user.get_todo(ID):
      log.warning('already have todo ID: %s for user: %s', ID, repr(g.user))
      abort(409)
    return PUT_or_POST_todo(ID, log)

  def delete(self, ID):
    try:
      deleted = g.user.del_todo(ID)
    except: # A lot can go wrong here.
      log.exception('deleting todo ID: %s for user %s', ID, repr(g.user))
      abort(500)
    if not deleted:
      log.warning('unknown todo ID: %s for user: %s', ID, repr(g.user))
      abort(404)
    return 'deleted'
