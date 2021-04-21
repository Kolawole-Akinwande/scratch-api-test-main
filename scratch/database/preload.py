import csv
import logging
from os import path
from scratch.database import db
from scratch.database.models import Users
import sqlalchemy.exc

log = logging.getLogger(__name__)


def preload_data():
    error = False
    if path.exists('data.csv'):
        with open('data.csv', 'r') as doc:
            reader = csv.DictReader(doc)  # comma is default delimiter
            try:
                db.session.bulk_save_objects(Users(user['id'], user['name']) for user in reader)

            except sqlalchemy.exc.IntegrityError as e:
                error = True
                log.info(e)
        if not error:
            db.session.commit()
    else:
        print('Cannot preload database, file does not exist')
