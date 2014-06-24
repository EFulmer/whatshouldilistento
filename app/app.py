from flask import flash
from flask import Flask
from flask import render_template
from flask import request

from best_album import best_album


app = Flask(__name__)
DEBUG = True
SECRET_KEY = 'development key'
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/enter_band', methods=['GET', 'POST'])
def enter_band():
    if request.method == 'POST':
        artist = request.form['artist']
        try:
            recommended = best_album(artist)
            flash('Recommended album for {0}: {1}'.forat(artist, recommended))
        except Exception:
            flash("""Looks like {0} isn't listed on Rate Your Music. 
                    
                    Nice job namedropping them!""".format(artist))
    return render_template('enter_band.html')


if __name__ == '__main__':
    app.run()
