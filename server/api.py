import logging
from flask import g, jsonify, request, abort
from flask.ext.restful import Resource, Api
from todo import GET_todo, PUT_or_POST_todo, todo_args_from_request


log = logging.getLogger('api')


def configure_api(app, api_url='/api'):
  api = Api(app)
  api.add_resource(TodoAPI, api_url + '/todo/<int:ID>')


class TodoAPI(Resource):

  def get(self, ID):
    return GET_todo(ID, log)

  def put(self, ID):
    if not g.user.get_todo(ID):
      log.warning('unknown todo ID: %s for user: %s', ID, repr(user))
      abort(404)
    return PUT_or_POST_todo(ID, log)

  def post(self, ID):
    if g.user.get_todo(ID):
      log.warning('already have todo ID: %s for user: %s', ID, repr(user))
      abort(409)
    return PUT_or_POST_todo(ID, log)
