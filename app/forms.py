from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class ProfileForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    
