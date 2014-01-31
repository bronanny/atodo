import logging
from flask import (
  g,
  session,
  request,
  render_template,
  flash,
  redirect,
  )
from flask.ext.openid import OpenID
from settings import openid_store, login_url_fragment
from database import db, User


log = logging.getLogger('OpenID')


oid = OpenID(
  app=None,
  fs_store_path=openid_store,
  safe_roots=[],
  )


def before_request():
  if 'openid' in session:
    g.user = User.query.filter_by(openid=session['openid']).first()
  else:
    g.user = None


@oid.loginhandler
def login():

  if g.user:
    return redirect(oid.get_next_url())

  if request.method == 'GET':
    return render_template(
      'login.html',
      next=oid.get_next_url(),
      error=oid.fetch_error(),
      )

  if request.method != 'POST':
    return redirect(login_url_fragment)

  openid = request.form.get('openid')
  if openid:
    return oid.try_login(openid, ask_for=['fullname', 'nickname'])

  flash('Please select an OpenID provider.')
  return redirect(login_url_fragment)


@oid.after_login
def after_login(response):
  uoid = response.identity_url
  nick = response.nickname or response.fullname
  log.debug('after login: %r %r', uoid, nick)
  if not nick:
    flash('We didn\'t receive a user name from your OpenID provider!')
    return redirect(login_url_fragment)

  user = User.query.filter_by(openid=uoid).first()
  if user:
    flash('Welcome back %s.' % (nick,))
    g.user = user
    return redirect(oid.get_next_url())

  user = User(name=nick, openid=uoid)
  db.session.add(user)
  db.session.commit()
  g.user = user
  flash('Welcome %s. Thank you for trying us out!' % (nick,))
  return redirect('/')


def logout():
  session.pop('openid', None)
  flash('You have been signed out.')
  return redirect(login_url_fragment)
