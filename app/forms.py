# forms.py

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required


class ArtistForm(Form):
    """Form for users to enter in an artist's name."""
    name = TextField('name', 
            validators=[Required(message='Please enter a name.')])


# This was stolen without shame from Miguel Grinberg's Flask tutorial!
class LoginForm(Form):
    """OpenID login form."""
    openid      = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
