from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(25))
    #password = db.Column(db.String(255), unique=True)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(50))
    username = db.Column(db.String(25))
    date_created = db.Column(db.Date)
    

    def __init__(self, firstname, lastname, username, gender, age, bio, date_created):
        #password
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.gender = gender
        self.age = age
        self.bio = bio
        self.date_created = date_created

    def __repr__(self):
        return '<User %r>' % self.name