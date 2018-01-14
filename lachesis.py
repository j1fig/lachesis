import json
import pickle
import pandas as pd
from flask import Flask, request, jsonify


def reload_classifier():
    with open('columns.json') as fh:
        columns = json.load(fh)

    with open('classifier.pickle', 'rb') as fh:
        classifier = pickle.load(fh)

    with open('dtypes.pickle', 'rb') as fh:
        dtypes = pickle.load(fh)

    return classifier, columns, dtypes


app = Flask(__name__)


classifier, columns, dtypes = reload_classifier()


@app.route('/predict', methods=['POST'])
def predict():
    payload = request.get_json()
    print(payload)
    obs = pd.DataFrame([payload], columns=columns).astype(dtypes)
    proba = classifier.predict_proba(obs)[0, 1]
    return jsonify({
        'prediction': proba
    })

if __name__ == '__main__':
    app.run(debug=True)

