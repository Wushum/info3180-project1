from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    password = db.Column(db.String(255), unique=True)

    def __init__(self, firstname, lastname, password):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name