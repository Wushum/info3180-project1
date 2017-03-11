"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, time, random, datetime
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required
from flask_wtf import Form
from forms import ProfileForm
from models import Profile
from datetime import datetime
from random import randint
from sqlalchemy.sql import exists


# from flask.ext.wtf import Form
# from wtforms.fields import TextField, BooleanField
# from wtforms.validators import Required


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
    
def timeinfo():
    return time.strftime("%d %b %Y")


@app.route('/profile/<userid>', methods=['GET', 'POST'])
def profile_view(userid):
    user = db.session.query(Profile).filter(Profile.userid == str(userid)).first()
    if not user:
        flash("user cannot be found", 'danger')
    else:
        if request.header.get('Content-Type' == 'application/json') or request.method == 'POST':
            return jsonify(userid=user.userid, username=user.username, gender=user.gender, age=user.age, pic=user.pic, date_created=user.date_created)
        return render_template('profile.html', user=user)
    return redirect(url_for('profile_list'))
    
@app.route('/profile', methods=['GET', 'POST'])
def add_profile():
    form = ProfileForm(request.form)
    #file_folder = app.config['UPLOAD_FOLDER']
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = request.form['firstname']#.strip()
            lastname = request.form['lastname']#.strip()
            username = request.form['username']#.strip()
            gender = request.form['gender']
            age = request.form['age']
            bio = request.form['bio']
            pic = request.files['pic']
            file_folder = app.config["UPLOAD_FOLDER"]
            #date_created  = time.strftime("%m %d %Y")
            if pic.filename =='':
                picName = "profile-default.jpg"
            else:
                picName = secure_filename(pic.filename)
                pic.save(os.path.join(file_folder, picName))
            while True:
                userid = randint(10000, 20000)
                output = Profile.query.filter_by(userid=userid).first()
                if output is None:
                    
                #if not db.session.query(exists().where(Profile.userid ==str (userid))).scalar():
                    break
            date_created = timeinfo()
            profile =  Profile(str(userid),firstname, lastname, username, gender, bio, age, date_created)
            
            db.session.add(profile)
            db.session.commit()
            
            flash ('Profile created', 'success')
            return redirect(url_for('profile_list'))
    # flash_errors(profile_form)
    return render_template("profile.html", form=form)

@app.route('/profiles', methods=['GET', 'POST'])
def profile_list():
    plist = []
    result = db.session.query(Profile).all()
    for user in result:
        plist.append({"username": user.username, "userid": user.userid})
    if request.headers.get('Content-Type') == 'application/json' or request.method == 'POST':
        return jsonify(users = plist)
    return render_template('profiles.html', plist=plist)

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