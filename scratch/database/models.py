from scratch.database import db


class Users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, id, name):
        self.name = name
        self.id = id

    def __repr__(self):
        return '<User %r>' % self.name
