from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, SelectField, IntegerField
from wtforms.validators import InputRequired

class ProfileForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    #password = PasswordField('password', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    #gender = StringField('gender', validators=[InputRequired()])
    age = StringField('age', validators=[InputRequired()])
    bio = StringField('bio', validators=[InputRequired()])
