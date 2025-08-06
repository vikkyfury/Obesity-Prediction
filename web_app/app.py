from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import OBESITY_LABELS, NUMERICAL_COLUMNS
from config import GENDER_MAPPING, MTRANS_MAPPING, FAMILY_HISTORY_MAPPING
from config import FAVC_MAPPING, SMOKE_MAPPING, SCC_MAPPING, CAEC_MAPPING, CALC_MAPPING

app = Flask(__name__)

# Simple prediction function based on BMI and lifestyle factors
def simple_prediction(data):
    """Simple prediction based on BMI and lifestyle factors"""
    try:
        # Calculate BMI
        height = float(data['height']) / 100  # Convert to meters
        weight = float(data['weight'])
        bmi = weight / (height ** 2)
        
        # Get lifestyle factors
        age = float(data['age'])
        gender = GENDER_MAPPING.get(data['gender'], 0)
        family_history = FAMILY_HISTORY_MAPPING.get(data['family_history_with_overweight'], 0)
        favc = FAVC_MAPPING.get(data['favc'], 0)
        fcvc = float(data['fcvc'])
        ncp = float(data['ncp'])
        caec = CAEC_MAPPING.get(data['caec'], 0)
        smoke = SMOKE_MAPPING.get(data['smoke'], 0)
        ch2o = float(data['ch2o'])
        scc = SMOKE_MAPPING.get(data['scc'], 0)
        faf = float(data['faf'])
        tue = float(data['tue'])
        calc = CALC_MAPPING.get(data['calc'], 0)
        mtrans = MTRANS_MAPPING.get(data['mtrans'], 0)
        
        # Calculate risk score
        risk_score = 0
        
        # BMI contribution (40% weight)
        if bmi < 18.5:
            risk_score += 0.1  # Insufficient weight
        elif bmi < 25:
            risk_score += 0.2  # Normal weight
        elif bmi < 30:
            risk_score += 0.6  # Overweight
        elif bmi < 35:
            risk_score += 0.8  # Obesity Type I
        elif bmi < 40:
            risk_score += 0.9  # Obesity Type II
        else:
            risk_score += 1.0  # Obesity Type III
        
        # Lifestyle factors (60% weight)
        lifestyle_score = 0
        
        # Age factor
        if age > 50:
            lifestyle_score += 0.2
        elif age > 30:
            lifestyle_score += 0.1
        
        # Family history
        if family_history == 1:
            lifestyle_score += 0.3
        
        # High caloric food consumption
        if favc == 1:
            lifestyle_score += 0.2
        
        # Vegetable consumption (inverse)
        lifestyle_score += (3 - fcvc) * 0.1
        
        # Number of main meals
        if ncp < 2:
            lifestyle_score += 0.1
        
        # Food consumption between meals
        if caec > 1:
            lifestyle_score += 0.2
        
        # Smoking
        if smoke == 1:
            lifestyle_score += 0.1
        
        # Water consumption (inverse)
        lifestyle_score += (5 - ch2o) * 0.05
        
        # Physical activity frequency (inverse)
        lifestyle_score += (3 - faf) * 0.15
        
        # Technology use (inverse)
        lifestyle_score += (3 - tue) * 0.1
        
        # Transportation
        if mtrans > 2:  # Less active transportation
            lifestyle_score += 0.1
        
        # Combine scores
        final_score = (risk_score * 0.4) + (lifestyle_score * 0.6)
        
        # Map to obesity categories
        if final_score < 0.3:
            return "Insufficient Weight"
        elif final_score < 0.5:
            return "Normal Weight"
        elif final_score < 0.7:
            return "Overweight"
        elif final_score < 0.85:
            return "Obesity Type I"
        elif final_score < 0.95:
            return "Obesity Type II"
        else:
            return "Obesity Type III"
            
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Normal Weight"  # Default fallback

@app.route('/')
def form():
    return render_template('full.html', model_loaded=True)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        print("Received data:", data)
        
        # Use simple prediction algorithm
        prediction = simple_prediction(data)
        print(f"Prediction: {prediction}")
        
        return render_template('output.html', prediction=prediction)
    except Exception as e:
        print("Error:", e)
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
