import logging
from flask import Flask, request, render_template, jsonify
from settings import template_dir


log = logging.getLogger('todoer')


app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  import logging.config
  import log_config
  logging.config.dictConfig(log_config.config)
  app.debug = True
  app.run(host='0.0.0.0')
