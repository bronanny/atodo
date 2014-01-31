import sys, logging
from settings import logfilename


config = {
  'version': 1, # Logging config schema, nothing to do with us.

  'formatters': {
    'fo': {'format': '%(asctime)s %(name)s %(levelname)s %(message)s'},
    },

  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'level': logging.DEBUG,
      'formatter': 'fo',
      'stream': sys.stdout,
      },
    'disk': {
      'class': 'logging.FileHandler',
      'level': logging.INFO,
      'formatter': 'fo',
      'filename': logfilename,
      },
    },

  'loggers': {
    'todoer': {
      'level': logging.DEBUG,
      'handlers': ['console', 'disk'],
      },
    },
  }


if __name__ == '__main__':
  import logging.config
  logging.config.dictConfig(config)
  log = logging.getLogger('todoer')
  log.error('cats!')
