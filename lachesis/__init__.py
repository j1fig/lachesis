from flask import Flask


app = Flask(__name__)


import lachesis.views


if __name__ == '__main__':
    app.run(debug=True)
