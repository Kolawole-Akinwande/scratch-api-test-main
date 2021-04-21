import logging.config
import os

from flask import Blueprint, Flask

from scratch import settings
from scratch.api.users import api, ns
from scratch.database import clear_data, db, model_exists
from scratch.database.preload import preload_data
from scratch.database.models import Users

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


@app.route('/healthz')
def health():
    return 'OK'


def initialize_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['SQLALCHEMY_BINDS'] = settings.SQLALCHEMY_BINDS
    blueprint = Blueprint('api', __name__, url_prefix='/v1')
    api.init_app(app)
    api.init_app(blueprint)
    api.add_namespace(ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    with app.app_context():
        if settings.ENVIRONMENT == "development":
            clear_data()
            db.drop_all(bind='users')
            db.create_all(bind='users')
            preload_data()
        else:
            if not model_exists(Users):
                db.create_all(bind='users')
                preload_data()
            else:
                preload_data()


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG, host='0.0.0.0')


if __name__ == '__main__':
    main()
