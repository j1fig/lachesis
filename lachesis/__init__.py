from flask import Flask


app = Flask(__name__)


import lachesis.views
from lachesis.models.database import init_db, clear_db


if __name__ == '__main__':
    app.run(debug=True)
