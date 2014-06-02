from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'What do you want to listen to?'


if __name__ == '__main__':
    app.run()
