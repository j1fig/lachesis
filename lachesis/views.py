import json
import pickle

import pandas as pd
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from lachesis import app
from lachesis.transformers import ObservationCleaner
from lachesis.models import db, Prediction


def reload_pipeline():
    with open('pipeline.pickle', 'rb') as fh:
        pipeline = pickle.load(fh)

    with open('columns.json') as fh:
        columns = json.load(fh)

    with open('dtypes.pickle', 'rb') as fh:
        dtypes = pickle.load(fh)

    return pipeline, columns, dtypes


pipeline, columns, dtypes = reload_pipeline()


@app.errorhandler(IntegrityError)
def handle_duplicate_observation(error):
    response = jsonify({
        'message': 'Duplicate observation',
    })
    response.status_code = 400
    return response


@app.route('/predict', methods=['POST'])
def predict():
    payload = request.get_json()
    print(payload)
    if any([p not in payload for p in ('observation', 'id')]):
        raise BadRequest('Missing `observation` or `id` mandatory fields')

    observation = payload['observation']
    observation_id = payload['id']
    observation.update({'id': observation_id})
    obs = pd.DataFrame([observation], columns=columns).astype(dtypes)
    proba = pipeline.predict_proba(obs)[0, 1]
    db.session.add(
        Prediction(
            observation_id=observation_id,
            observation=json.dumps(observation),
            proba=proba
        )
    )
    db.session.commit()
    return jsonify({
        'proba': proba
    })


@app.route('/update', methods=['POST'])
def update():
    payload = request.get_json()
    print(payload)
    if any([p not in payload for p in ('true_class', 'id')]):
        raise BadRequest('Missing `true_class` or `id` mandatory fields')

    p = Prediction.query.filter_by(observation_id=payload['id']).get_or_404()
    p.true_class = obs['true_class']
    db.session.commit()
    return jsonify(p.to_dict())
