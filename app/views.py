# views.py

from flask import flash
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db
from app import lm
from app import oid

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
@oid.loginhandler # handles logins - duh
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
        # print form.openid.data
        # print form.remember_me.data
        # flash("""TODO: Implement this you dork: \n
        #         Login for OpenID={}, \n
        #         remember_me={}""".format(form.openid.data, 
        #             form.remember_me.data))
        # return redirect('/')
    return render_template('login.html', 
            form=form,
            providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def user_load(id):
    return models.User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    user = models.User.query.filter_by(email=resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = models.User(nickname=nickname, email=resp.email) #, 
                # role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
        remember_me = False

        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)

        login_user(user, remember=remember_me)

        return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    # current_user global is set by Flask-Login
    g.user = current_user
