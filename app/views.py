# views.py

from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from flask.ext.sqlalchemy import SQLAlchemy

from app import app
import config
import models
from forms import ArtistForm, LoginForm
import rym_scraper


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/enter_band', methods=['GET', 'POST'])
def enter_band():
    form = ArtistForm()
    
    if form.validate_on_submit():
        return band_info(form.name.data)
    else:
        return render_template('enter_band.html', form=form)


@app.route('/band_info', methods=['GET', 'POST'])
def band_info(artist):
    rym_rec = "{0}'s best album is {1}, according to RateYourMusic."
    try:
        info = rym_scraper.get_artist_info(artist)
        flash(rym_rec.format(info.name, info.best_album))
    except Exception as e:
        print e
        flash("Sorry, {0} isn't listed on Rate Your Music.".format(artist))

    return render_template('band_info.html')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print form.openid.data
        print form.remember_me.data
        flash("""TODO: Implement this you dork: \n
                Login for OpenID={}, \n
                remember_me={}""".format(form.openid.data, 
                    form.remember_me.data))
        return redirect('/')
    return render_template('login.html', 
            form=form,
            providers=app.config['OPENID_PROVIDERS'])

