from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, SelectField, IntegerField, RadioField
from wtforms.validators import InputRequired



class ProfileForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    #gender = SelectField('gender', choices = [('male', 'Male'), ('female', 'Female')])
    gender = RadioField('gender', choices = [('M','Male'),('F','Female')])
    age = IntegerField('age', validators=[InputRequired()])
    bio = TextAreaField('bio', validators=[InputRequired()])
    pic = FileField('pic', validators=[InputRequired()])