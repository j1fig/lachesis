import json
import pickle

import pandas as pd
from flask import request, jsonify

from lachesis import app
from lachesis.transformers import ObservationCleaner


def reload_pipeline():
    with open('pipeline.pickle', 'rb') as fh:
        pipeline = pickle.load(fh)

    with open('columns.json') as fh:
        columns = json.load(fh)

    with open('dtypes.pickle', 'rb') as fh:
        dtypes = pickle.load(fh)

    return pipeline, columns, dtypes


pipeline, columns, dtypes = reload_pipeline()


@app.route('/predict', methods=['POST'])
def predict():
    payload = request.get_json()
    observation = payload['observation']
    observation.update({'id': payload['id']})
    obs = pd.DataFrame([observation], columns=columns).astype(dtypes)
    proba = pipeline.predict_proba(obs)[0, 1]
    return jsonify({
        'prediction': proba
    })
