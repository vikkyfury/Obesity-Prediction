from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import sys
import os
import joblib

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MODEL_PATH, OBESITY_LABELS, NUMERICAL_COLUMNS
from config import GENDER_MAPPING, MTRANS_MAPPING, FAMILY_HISTORY_MAPPING
from config import FAVC_MAPPING, SMOKE_MAPPING, SCC_MAPPING, CAEC_MAPPING, CALC_MAPPING

app = Flask(__name__)

# Load model and scaler
model = None
scaler = None
try:
    # Load the advanced model
    model = load_model(MODEL_PATH, compile=False)
    print("✅ Advanced model loaded successfully!")
    
    # Load the advanced scaler
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'advanced_scaler.pkl')
    scaler = joblib.load(scaler_path)
    print("✅ Advanced scaler loaded successfully!")
    
except Exception as e:
    print(f"❌ Error loading model/scaler: {e}")
    print("⚠️ Running in demo mode with random predictions")
    model = None
    scaler = None

@app.route('/')
def form():
    return render_template('full.html', model_loaded=model is not None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        print("Received data:", data)  # Logging input data
        
        if model is None or scaler is None:
            # Demo mode - return a sample prediction
            import random
            demo_predictions = list(OBESITY_LABELS.values())
            demo_prediction = random.choice(demo_predictions)
            return render_template('output.html', 
                                prediction=demo_prediction, 
                                demo_mode=True)
        
        data = pd.DataFrame([data])
        processed_data = preprocess(data)
        prediction = get_prediction(processed_data, model)
        return render_template('output.html', prediction=prediction[0])
    except Exception as e:
        print("Error:", e)  # Logging errors
        return f"Error: {str(e)}", 500

def preprocess(data):
    # Map categorical variables to numerical values
    mappings = {
        'gender': GENDER_MAPPING,
        'mtrans': MTRANS_MAPPING,
        'family_history_with_overweight': FAMILY_HISTORY_MAPPING,
        'favc': FAVC_MAPPING,
        'smoke': SMOKE_MAPPING,
        'scc': SCC_MAPPING,
        'caec': CAEC_MAPPING,
        'calc': CALC_MAPPING
    }

    # Apply mappings to the data
    for column, mapping in mappings.items():
        if column in data:
            data[column] = data[column].map(mapping).astype(float)

    # Convert numerical columns to float
    for col in NUMERICAL_COLUMNS:
        if col in data:
            data[col] = data[col].astype(float)

    # Add engineered features for advanced model
    if 'height' in data and 'weight' in data and 'age' in data:
        data['BMI'] = data['weight'] / ((data['height'] / 100) ** 2)
        data['Age_Height_Ratio'] = data['age'] / data['height']
        data['Weight_Height_Ratio'] = data['weight'] / data['height']
        
        # Activity and lifestyle scores
        if 'faf' in data and 'tue' in data:
            data['Activity_Score'] = (4 - data['faf']) * (3 - data['tue'])
        if 'fcvc' in data and 'ncp' in data and 'caec' in data:
            data['Diet_Score'] = data['fcvc'] * data['ncp'] * (1 + data['caec'])
            data['Lifestyle_Score'] = data['Activity_Score'] - data['Diet_Score']

    # Scale the features using the advanced scaler
    if scaler is not None:
        feature_columns = [
            'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
            'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS',
            'BMI', 'Age_Height_Ratio', 'Weight_Height_Ratio', 'Activity_Score', 'Diet_Score', 'Lifestyle_Score'
        ]
        
        # Ensure all required features are present
        for col in feature_columns:
            if col not in data:
                data[col] = 0  # Default value for missing features
        
        # Scale the data
        data_scaled = scaler.transform(data[feature_columns])
        return pd.DataFrame(data_scaled, columns=feature_columns)

    return data


def get_prediction(data, model):
    predictions = model.predict(data)
    highest_labels = np.argmax(predictions, axis=1)
    highest_labels_mapped = [OBESITY_LABELS[label] for label in highest_labels]
    return highest_labels_mapped

if __name__ == '__main__':
    app.run(debug=True, port=5001)
