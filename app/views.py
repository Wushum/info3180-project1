"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, time
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
    
def date():
    return time.strftime("%m %d %Y")
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('add_profile'))
    return render_template('login.html', error=error)
    
@app.route('/profiles')
def profiles():
    users= db.session.query(Profile).all()
    return render_template('profiles.html',users=users)
    # if not session.get('logged_in'):
    #     abort(401)
        
        
    # import os
    # rootdir = os.getcwd()
    # filelist = []
    
    # for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
    #     for file in files:
    #         f = os.path.join(subdir, file)
    #         filelist += [f]
            
    #         #names = os.listdir(os.path.join(app.static_folder, 'imgs'))
    #         #img_url =  url_for('static/uploads', filesname = os.path.join('imgs' (names))
    #     return render_template('profiles.html', filelist=filelist)
        
    
@app.route('/add_profile', methods=['POST', 'GET'])
def add_profile():
    if not session.get('logged_in'):
        abort(401)
        
    file_folder = app.config["UPLOAD_FOLDER"]
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_folder, filename))
    
    profile_form = ProfileForm()
    
    if request.method == 'POST':
        if profile_form.validate_on_submit():
        
        
            firstname = profile_form.firstname.data
            lastname = profile_form.lastname.data
            username = profile_form.username.data
            #password = profile_form.password.data
            gender = profile_form.gender.data
            age = profile_form.age.data
            bio = profile_form.bio.data
            #date_created = profile_form.date_created.data
            
            profile =  Profile(firstname, lastname, username, gender, age, bio, date())
            
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