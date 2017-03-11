from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, SelectField, IntegerField, RadioField#, FileAllowed
from wtforms.validators import InputRequired
from models import Profile
from flask_wtf.file import FileAllowed


class ProfileForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    #gender = SelectField('gender', choices = [('male', 'Male'), ('female', 'Female')])
    gender = RadioField('gender', choices = [('M','Male'),('F','Female')])
    age = IntegerField('age', validators=[InputRequired()])
    bio = TextAreaField('bio', validators=[InputRequired()])
    #pic = FileField('pic', validators=[InputRequired()])
    pic = FileField('pic', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')])
    
    def validate(self):
      """ Ensures a unique username is chosen """
      if not FlaskForm.validate(self):
        return False
     
      # Check if username is already in the database
      user = Profile.query.filter_by(username=self.username.data).first()
      if user:
        # Error message
        self.username.errors.append('Username already taken.')
        return False
      else:
        return True  