# views.py

from flask import flash
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db
from app import lm
from app import oid

import config
import models
from forms import ArtistForm, LoginForm
import last_fm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
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
    rym_rec = "{0}'s best album is {1}, according to Last.fm."
    try:
        info = last_fm.get_best_album(artist)
        flash(rym_rec.format(info.artist, info.album))

        if g.user is not None:
            entry = models.ArtistEntry(name=info.artist, 
                                       album=info.album, 
                                       id=g.user.id)
            db.session.add(entry)
            db.session.commit()
    except last_fm.ArtistNotFoundException:
        flash("Sorry, {0} isn't listed on Last.fm.".format(artist))
    except Exception as e:
        print e
        flash("Sorry, an error occurred. It'll be fixed soon!")

    return render_template('band_info.html')


@app.route('/my_bands', methods=('GET',))
@login_required
def my_bands():
    if g.user is None:
        flash('Sorry, but you must be logged in to keep a band to-do list.')
        return render_template('hello.html')
    bands = models.ArtistEntry.query.filter(models.ArtistEntry.id == g.user.id).all()
    return render_template('my_bands.html')


@app.route('/login', methods=['GET','POST'])
@oid.loginhandler # handles logins - duh
def login():
    if g.user is not None and g.user.is_authenticated():
        flash("Hey, you're already logged in!")
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
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
        user = models.User(nickname=nickname, email=resp.email)
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

