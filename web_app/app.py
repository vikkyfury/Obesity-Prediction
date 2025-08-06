from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MODEL_PATH, OBESITY_LABELS, NUMERICAL_COLUMNS
from config import GENDER_MAPPING, MTRANS_MAPPING, FAMILY_HISTORY_MAPPING
from config import FAVC_MAPPING, SMOKE_MAPPING, SCC_MAPPING, CAEC_MAPPING, CALC_MAPPING

app = Flask(__name__)

# Load model with custom_objects to handle compatibility issues
model = None
try:
    # Try loading with custom_objects to handle compatibility
    from tensorflow.keras import Model
    from tensorflow.keras.layers import InputLayer
    
    # Create a custom InputLayer that ignores batch_shape
    class CompatibleInputLayer(InputLayer):
        def __init__(self, **kwargs):
            # Remove batch_shape if present
            kwargs.pop('batch_shape', None)
            super().__init__(**kwargs)
    
    model = load_model(MODEL_PATH, compile=False, custom_objects={
        'Model': Model,
        'InputLayer': CompatibleInputLayer
    })
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Model loading failed. The model was saved with an older TensorFlow version.")
    print("Please retrain the model using the current TensorFlow version.")
    print("For now, the application will run in demo mode.")
    model = None

@app.route('/')
def form():
    return render_template('full.html', model_loaded=model is not None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        print("Received data:", data)  # Logging input data
        
        if model is None:
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

    return data


def get_prediction(data, model):
    predictions = model.predict(data)
    highest_labels = np.argmax(predictions, axis=1)
    highest_labels_mapped = [OBESITY_LABELS[label] for label in highest_labels]
    return highest_labels_mapped

if __name__ == '__main__':
    app.run(debug=True, port=5001)
