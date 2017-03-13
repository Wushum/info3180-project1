"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, time, random
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from flask_wtf import Form
from app.models import Profile
from random import randint


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


@app.route('/profile', methods=['POST','GET'])
def add_profile():
    
    
    if request.method == 'POST':
        userid = random.randint(10000, 20000)
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        age = request.form['age']
        bio = request.form['bio']
        
        pic = request.files['pic']
        
        file_folder = app.config["UPLOAD_FOLDER"]
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(file_folder, filename))
            
        date_created = time.strftime("%d %b %Y")
        profile =  Profile(userid=userid, username=username, firstname=firstname, lastname=lastname, gender=gender, age=age, bio=bio, date_created=date_created, pic=pic.filename,)
        
    
        db.session.add(profile)
        db.session.commit()
            
        
        return redirect(url_for('profile_list'))
    
    return render_template("profile.html")

@app.route('/profiles', methods=['POST','GET'])
def profile_list():
    # plist = []
    # result = db.session.query(Profile).all()
    # for user in result:
    #     plist.append({"username": user.username, "userid": user.userid})
    # if request.headers.get('Content-Type') == 'application/json' or request.method == 'POST':
    #     return jsonify(result)
    # return render_template('profiles.html', plist=plist)
    profiles = db.session.query(Profile).all()
    if request.headers['Content-Type']=='application/json' or request.method == "POST":
        userlist = []
        for profile in profiles:
            userlist.append({'userid':profile.userid, 'username':profile.username})
            profiles = {'Users':userlist}
        return jsonify(profiles)
    elif request.method == 'GET':
        return render_template('profiles.html',profiles=profiles)

    
    
    
@app.route('/profile/<userid>', methods=['POST','GET'])
def profile_view(userid):
    print userid
    profile = db.session.query(Profile).filter_by(userid=userid).first()

    if request.headers['Content-Type']=='application/json' or request.method == "POST":
        return jsonify(userid=profile.userid, username=profile.username, pic=profile.pic, gender=profile.gender, age=profile.age, profile_created_on=profile.date_created)
    else:
        return render_template('profile_view.html', profile=profile)
        
    
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