from flask import g, session, request, render_template
from flask.ext.openid import OpenID
from settings import openid_store
from database import db, User


oid = OpenID(
  app=None,
  fs_store_path=openid_store,
  safe_roots=[],
  )


def before_request():
  g.user = None
  if 'openid' in session:
    g.user = User.query.filter_by(openid=session['openid']).first()


@oid.loginhandler
def login():

  if g.user is not None:
    return redirect(oid.get_next_url())

  if request.method == 'GET':
    return render_template(
      'login.html',
      next=oid.get_next_url(),
      error=oid.fetch_error(),
      )

  assert request.method == 'POST', (
    'request.method not POST|GET: %r'
    % (request.method,)
    )

  openid = request.form.get('openid')
  if openid:
      return oid.try_login(openid, ask_for=['nickname'])
