from scratch.database import db


def create_response(user):
    return {'id': user.id, 'name': user.name}


def save_to_db(user):
    db.session.add(user)
    db.session.commit()
