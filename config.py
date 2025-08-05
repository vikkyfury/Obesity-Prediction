"""
Configuration settings for the Obesity Prediction project.
"""

import os

# Flask configuration
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Model configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'my_model_nn_1.h5')

# Feature mappings
GENDER_MAPPING = {'Male': 0, 'Female': 1}
MTRANS_MAPPING = {
    'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 
    'Public_Transportation': 3, 'Walking': 4
}
FAMILY_HISTORY_MAPPING = {'no': 0, 'yes': 1}
FAVC_MAPPING = {'no': 0, 'yes': 1}
SMOKE_MAPPING = {'no': 0, 'yes': 1}
SCC_MAPPING = {'no': 0, 'yes': 1}
CAEC_MAPPING = {
    'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3
}
CALC_MAPPING = {
    'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3
}

# Prediction labels
OBESITY_LABELS = {
    0: 'Insufficient Weight',
    1: 'Normal Weight', 
    2: 'Overweight Level I',
    3: 'Overweight Level II',
    4: 'Obesity Type I',
    5: 'Obesity Type II',
    6: 'Obesity Type III'
}

# Numerical columns
NUMERICAL_COLUMNS = ['age', 'height', 'weight', 'fcvc', 'ncp', 'faf', 'tue', 'ch2o']

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 