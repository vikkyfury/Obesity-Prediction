#!/bin/bash

# EC2 Setup Script for Obesity Prediction Web Application
# This script should be run on a fresh EC2 instance

set -e  # Exit on any error

echo "=== EC2 Setup for Obesity Prediction App ==="

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo yum install -y python3 python3-pip

# Install development tools (needed for some Python packages)
echo "Installing development tools..."
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3-devel

# Install additional system dependencies
echo "Installing system dependencies..."
sudo yum install -y gcc gcc-c++ make openssl-devel bzip2-devel libffi-devel

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /opt/obesity-prediction
sudo chown ec2-user:ec2-user /opt/obesity-prediction

# Copy application files (assuming they're uploaded to /tmp)
echo "Copying application files..."
cp -r /tmp/obesity-prediction/* /opt/obesity-prediction/

# Change to application directory
cd /opt/obesity-prediction

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Set up environment variables
echo "Setting up environment variables..."
cat > .env << EOF
FLASK_ENV=production
FLASK_DEBUG=0
HOST=0.0.0.0
PORT=5000
EOF

# Create systemd service file for Gunicorn
echo "Creating systemd service..."
sudo tee /etc/systemd/system/obesity-prediction.service > /dev/null << EOF
[Unit]
Description=Obesity Prediction Web Application
After=network.target

[Service]
Type=simple
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/obesity-prediction
Environment=PATH=/opt/obesity-prediction/venv/bin
Environment=FLASK_ENV=production
Environment=FLASK_DEBUG=0
ExecStart=/opt/obesity-prediction/venv/bin/gunicorn -c gunicorn_config.py web_app.app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo "Enabling systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable obesity-prediction.service

# Configure firewall (if using firewalld)
echo "Configuring firewall..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-port=5000/tcp
    sudo firewall-cmd --reload
fi

# Configure security group (this needs to be done in AWS console or CLI)
echo "IMPORTANT: Configure your EC2 security group to allow inbound traffic on port 5000"
echo "You can do this in the AWS Console:"
echo "1. Go to EC2 Dashboard"
echo "2. Click on Security Groups"
echo "3. Select your instance's security group"
echo "4. Add inbound rule: Type=Custom TCP, Port=5000, Source=0.0.0.0/0"

# Start the service
echo "Starting the application..."
sudo systemctl start obesity-prediction.service

# Check service status
echo "Checking service status..."
sudo systemctl status obesity-prediction.service

echo "=== Setup Complete ==="
echo "Your application should now be running on http://YOUR_EC2_PUBLIC_IP:5000"
echo ""
echo "Useful commands:"
echo "  Check status: sudo systemctl status obesity-prediction.service"
echo "  View logs: sudo journalctl -u obesity-prediction.service -f"
echo "  Restart service: sudo systemctl restart obesity-prediction.service"
echo "  Stop service: sudo systemctl stop obesity-prediction.service"
echo "  View Gunicorn logs: tail -f /opt/obesity-prediction/logs/access.log"
echo "  View error logs: tail -f /opt/obesity-prediction/logs/error.log" 