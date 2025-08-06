#!/bin/bash

# Quick Deployment Script for Obesity Prediction App
# This is a simplified version for quick deployment

echo "=== Quick EC2 Deployment ==="

# Check if we're on Amazon Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" == "amzn" ]]; then
        echo "Detected Amazon Linux"
    else
        echo "Warning: This script is optimized for Amazon Linux"
    fi
fi

# Install Python 3 if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo yum install -y python3 python3-pip
fi

# Create app directory
APP_DIR="/opt/obesity-prediction"
echo "Setting up application in $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown ec2-user:ec2-user $APP_DIR

# Copy files (assuming they're in /tmp)
if [ -d "/tmp/obesity-prediction" ]; then
    echo "Copying application files..."
    cp -r /tmp/obesity-prediction/* $APP_DIR/
else
    echo "Error: Application files not found in /tmp/obesity-prediction"
    echo "Please upload your application files first"
    exit 1
fi

cd $APP_DIR

# Create virtual environment
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Create simple systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/obesity-prediction.service > /dev/null << EOF
[Unit]
Description=Obesity Prediction App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python web_app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "Starting application..."
sudo systemctl daemon-reload
sudo systemctl enable obesity-prediction.service
sudo systemctl start obesity-prediction.service

# Check status
echo "Checking application status..."
sudo systemctl status obesity-prediction.service --no-pager

echo ""
echo "=== Quick Deployment Complete ==="
echo "Your application should be running on port 5000"
echo "Make sure your EC2 security group allows inbound traffic on port 5000"
echo ""
echo "Useful commands:"
echo "  Check status: sudo systemctl status obesity-prediction.service"
echo "  View logs: sudo journalctl -u obesity-prediction.service -f"
echo "  Restart: sudo systemctl restart obesity-prediction.service" 