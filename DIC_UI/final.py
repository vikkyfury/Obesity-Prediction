from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np

app = Flask(__name__)
model = load_model('my_model_nn_1.h5')

@app.route('/')
def form():
    return render_template('full.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        print("Received data:", data)  # Logging input data
        data = pd.DataFrame([data])
        processed_data = preprocess(data)
        prediction = get_prediction(processed_data, model)
        return render_template('output.html', prediction=prediction[0])
    except Exception as e:
        print("Error:", e)  # Logging errors
        return str(e)  # Returning errors to the browser for debugging

def preprocess(data):
    # Map categorical variables to numerical values
    mappings = {
        'gender': {'Male': 0, 'Female': 1},
        'mtrans': {
            'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 
            'Public_Transportation': 3, 'Walking': 4
        },
        'family_history_with_overweight': {'no': 0, 'yes': 1},
        'favc': {'no': 0, 'yes': 1},
        'smoke': {'no': 0, 'yes': 1},
        'scc': {'no': 0, 'yes': 1},
        'caec': {
            'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3
        },
        'calc': {
            'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3
        }
    }

    # Apply mappings to the data
    for column, mapping in mappings.items():
        if column in data:
            data[column] = data[column].map(mapping).astype(float)

    # Convert numerical columns to float
    numerical_cols = ['age', 'height', 'weight', 'fcvc', 'ncp', 'faf', 'tue', 'ch2o']
    for col in numerical_cols:
        if col in data:
            data[col] = data[col].astype(float)

    return data


def get_prediction(data, model):
    predictions = model.predict(data)
    highest_labels = np.argmax(predictions, axis=1)
    map_label = {
        0: 'Insufficient Weight', 1: 'Normal Weight', 2: 'Overweight Level I',
        3: 'Overweight Level II', 4: 'Obesity Type I', 5: 'Obesity Type II', 6: 'Obesity Type III'
    }
    highest_labels_mapped = [map_label[label] for label in highest_labels]
    return highest_labels_mapped

if __name__ == '__main__':
    app.run(debug=True, port=5000)
