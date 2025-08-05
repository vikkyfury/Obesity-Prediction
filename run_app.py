#!/usr/bin/env python3
"""
Convenience script to run the Obesity Prediction web application.
"""

import os
import sys
import subprocess

def main():
    """Run the Flask web application."""
    # Change to web_app directory
    web_app_dir = os.path.join(os.path.dirname(__file__), 'web_app')
    
    if not os.path.exists(web_app_dir):
        print("Error: web_app directory not found!")
        sys.exit(1)
    
    # Change to web_app directory
    os.chdir(web_app_dir)
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("Error: app.py not found in web_app directory!")
        sys.exit(1)
    
    print("Starting Obesity Prediction Web Application...")
    print("Navigate to http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 