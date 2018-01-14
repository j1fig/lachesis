from flask_sqlalchemy import SQLAlchemy

from lachesis import app, settings

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

def clear_db():
    db.drop_all()


def init_db():
    db.create_all()


init_db()
