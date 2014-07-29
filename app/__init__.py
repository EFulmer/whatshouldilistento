# __init__.py
import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy

import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' # name of view function that logs users in
oid = OpenID(app, os.path.join(config.basedir, 'tmp'))


from app import views, models

