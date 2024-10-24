import pickle

from flask import Flask, request, jsonify


def load_from_pickle(pickle_file):
    with open(pickle_file, 'rb') as f_in:
        return pickle.load(f_in)

def predict_single(customer, dv, model):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]


app = Flask('subscript')


@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    dv = load_from_pickle('dv.bin')
    model = load_from_pickle('model1.bin')
    
    prediction = predict_single(customer, dv, model)
    subscript = prediction >= 0.5
    
    result = {
        'subscript_probability': float(prediction),
        'subscript': bool(subscript),
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)