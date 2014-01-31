import logging
from flask import Flask, request, render_template, jsonify
from settings import flask_settings


log = logging.getLogger('todoer')


app = Flask('todoer', **flask_settings)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
