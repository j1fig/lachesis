from flask_sqlalchemy import SQLAlchemy

from lachesis import app, settings

# app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vzyaqvirizeqbu:69c9cfa986766b9333e736551d19d031b93d2c71c2d012f1168f8b179e2e5933@ec2-54-217-243-160.eu-west-1.compute.amazonaws.com:5432/d74ceh9goigkmi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

def clear_db():
    db.drop_all()


def init_db():
    print('Initializaing database with: {}'.format(settings.DATABASE_URL))
    db.create_all()


init_db()
