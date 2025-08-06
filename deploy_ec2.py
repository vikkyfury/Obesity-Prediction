#!/usr/bin/env python3
"""
EC2 Deployment Script for Obesity Prediction Web Application
"""

import os
import sys
import subprocess
import argparse

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up the environment for production"""
    print("Setting up production environment...")
    
    # Set environment variables for production
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = '0'
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

def run_application():
    """Run the Flask application in production mode"""
    print("Starting Obesity Prediction Web Application...")
    print("Application will be available on port 5000")
    
    try:
        # Change to web_app directory
        web_app_dir = os.path.join(os.path.dirname(__file__), 'web_app')
        os.chdir(web_app_dir)
        
        # Run the Flask app with production settings
        subprocess.run([
            sys.executable, "app.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Deploy Obesity Prediction App on EC2')
    parser.add_argument('--install-only', action='store_true', help='Only install dependencies')
    parser.add_argument('--run-only', action='store_true', help='Only run the application')
    
    args = parser.parse_args()
    
    if args.install_only:
        install_dependencies()
        return
    
    if args.run_only:
        run_application()
        return
    
    # Full deployment
    install_dependencies()
    setup_environment()
    run_application()

if __name__ == "__main__":
    main() 