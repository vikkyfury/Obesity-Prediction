"""
Basic tests for the Obesity Prediction Flask application.
"""

import unittest
import sys
import os

# Add the web_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web_app'))

from app import app

class TestObesityPredictionApp(unittest.TestCase):
    """Test cases for the Obesity Prediction Flask application."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test that the home page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Data Input Form', response.data)
    
    def test_predict_endpoint_exists(self):
        """Test that the predict endpoint exists."""
        response = self.app.post('/predict')
        # Should return 400 (Bad Request) because no data is sent
        self.assertEqual(response.status_code, 400)
    
    def test_form_fields_present(self):
        """Test that all required form fields are present."""
        response = self.app.get('/')
        form_fields = [
            b'name="gender"',
            b'name="age"',
            b'name="height"',
            b'name="weight"',
            b'name="family_history_with_overweight"',
            b'name="favc"',
            b'name="fcvc"',
            b'name="ncp"',
            b'name="caec"',
            b'name="smoke"',
            b'name="ch2o"',
            b'name="scc"',
            b'name="faf"',
            b'name="tue"',
            b'name="calc"',
            b'name="mtrans"'
        ]
        
        for field in form_fields:
            self.assertIn(field, response.data)

if __name__ == '__main__':
    unittest.main() 