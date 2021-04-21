import os

FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = os.getenv('RESTPLUS_SWAGGER_UI_DOC_EXPANSION', 'list')
RESTPLUS_VALIDATE = os.getenv('RESTPLUS_VALIDATE', True)
ENVIRONMENT = os.getenv('ENVIRONMENT', "development")
SQLALCHEMY_BINDS = {
    'users':        SQLALCHEMY_DATABASE_URI,
}
print(SQLALCHEMY_BINDS)