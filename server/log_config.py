import sys, logging


def config(logfilename, in_production):
  return {
  'version': 1, # Logging config schema, nothing to do with us.

  'formatters': {
    'fo': {'format': '%(asctime)s %(name)s %(levelname)s %(message)s'},
    },

  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'level': logging.WARNING if in_production else logging.DEBUG,
      'formatter': 'fo',
      'stream': sys.stdout,
      },
    'disk': {
      'class': 'logging.FileHandler',
      'level': logging.INFO if in_production else logging.DEBUG,
      'formatter': 'fo',
      'filename': logfilename,
      },
    },

  'loggers': {
    'todoer': {
      'level': logging.DEBUG,
      'handlers': ['console', 'disk'],
      },
    'db': {
      'level': logging.DEBUG,
      'handlers': ['console', 'disk'],
      },
    },
  }


if __name__ == '__main__':
  import logging.config
  logging.config.dictConfig(config('/tmp/todoer.log', False))
  logging.getLogger('todoer').error('cats!')
