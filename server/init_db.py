import sys
from main import app
from database import db, User, log

app.test_request_context().push()

if len(sys.argv) > 1 and raw_input('Drop tables? [yes/N] ') == 'yes':
  log.info('Dropping tables.')
  db.drop_all()
  log.info('Tables dropped.')

log.info('Create all.')
db.create_all()
log.info('Created.')
