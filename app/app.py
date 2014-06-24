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
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        artist = request.form['artist']
        recommended = best_album(artist)
        flash(recommended)
    return render_template('enter_band.html')


if __name__ == '__main__':
    app.run()
