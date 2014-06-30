# app.py

from flask import flash
from flask import Flask
from flask import render_template
from flask import request

import rym_scraper


app = Flask(__name__)
DEBUG = True
SECRET_KEY = 'development key'
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/enter_band', methods=['GET', 'POST'])
def enter_band():
    rym_rec = "For {0}, RateYourMusic recommends listening to {1}"
    if request.method == 'POST':
        artist_name = request.form['artist']
    try:
        artist_info = rym_scraper.get_artist_info(artist_name)
        flash(rym_rec.format(artist_info.artist_name, artist_info.best_album))
    except Exception as e:
        flash("""Looks like {0} isn't listed on Rate Your Music. 
                 Sorry about that!""".format(artist_name))
    return render_template('enter_band.html')


if __name__ == '__main__':
    app.run()

