# forms.py

from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required


class ArtistForm(Form):
    name = TextField('name', validators=[Required()])
