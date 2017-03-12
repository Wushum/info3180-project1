from app import db

class Profile(db.Model):
    userid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(255), nullable =False)
    lastname = db.Column(db.String(255), nullable =False)
    username = db.Column(db.String(25), unique=True)
    gender = db.Column(db.String(10), nullable =False)
    age = db.Column(db.Integer, nullable =False)
    bio = db.Column(db.String(50))
    pic = db.Column(db.String(100), nullable =False)
    date_created = db.Column(db.Date())
    

    def __init__(self, userid, firstname, lastname, username, gender, age, bio, pic, date_created):
        #password
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.gender = gender
        self.age = age
        self.bio = bio
        self.pic=pic
        self.date_created = date_created

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
