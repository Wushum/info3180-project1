"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from flask_login import login_user
from flask_wtf import Form
from forms import ProfileForm
from models import Profile


# from flask.ext.wtf import Form
# from wtforms.fields import TextField, BooleanField
# from wtforms.validators import Required




###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
    
@app.route('/profiles')
def profiles():
    profiles = db.session.query(Profile).all()
    return render_template('profiles.html', profiles=profiles)

@app.route('/add_profile', methods=['POST', 'GET'])
def add_profile():
    profile_form = ProfileForm()
    
    if request.method == 'POST':
        if profile_form.validate_on_submit():
        
        
            firstname = profile_form.firstname.data
            lastname = profile_form.lastname.data
            password = profile_form.password.data
            
            profile =  Profile(firstname, lastname, password)
            
            db.session.add(profile)
            db.session.commit()
            
            flash ('Profile created', 'success')
            return redirect(url_for('home'))
            
            
    # flash_errors(profile_form)
    return render_template("add_profile.html", form=profile_form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")