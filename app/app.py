# app.py

from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

import config
from forms import ArtistForm
import rym_scraper


app = Flask(__name__)
app.config.from_object(config)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/enter_band', methods=['GET', 'POST'])
def enter_band():
    form = ArtistForm()
    if form.validate_on_submit():
        print "we're good!"
        print form.name.data
        return band_info(form.name.data)
    else:
        print "we're not good!"
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


if __name__ == '__main__':
    app.run()

