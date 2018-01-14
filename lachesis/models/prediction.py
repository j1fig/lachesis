from lachesis.models import db


class Prediction(db.Model):
    observation_id = db.Column(db.Integer, primary_key=True)
    proba = db.Column(db.Float, nullable=False)
    observation = db.Column(db.String(512), nullable=False)
    true_class = db.Column(db.Integer)

    def __repr__(self):
        return '<Prediction {}> is {}'.format(self.observation_id, self.proba)
