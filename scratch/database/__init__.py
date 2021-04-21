import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from scratch.settings import SQLALCHEMY_DATABASE_URI


db = SQLAlchemy()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        try:
            db.session.execute(table.delete())
            if 'sqlite' not in SQLALCHEMY_DATABASE_URI:
                db.session.execute("ALTER TABLE users AUTO_INCREMENT=1;")
        except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError) as e:
            print('Empty Table %s' % e)
    db.session.commit()


def model_exists(users):
    engine = db.get_engine(bind=users.__bind_key__)
    return users.metadata.tables[users.__tablename__].exists(engine)
