#!/bin/bash

# Obesity Prediction EC2 Deployment Script
# Usage: ./deploy_obesity_prediction.sh <pem_file> <ec2_ip>

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <pem_file> <ec2_ip> [username]"
    echo "Example: $0 obesity_prediction.pem 18.xxx.xxx.xxx"
    exit 1
fi

PEM_FILE="$1"
EC2_IP="$2"
USERNAME="${3:-ec2-user}"

print_status "Starting deployment with PEM file: $PEM_FILE"
print_status "EC2 IP: $EC2_IP"
print_status "Username: $USERNAME"

# Check if PEM file exists
if [ ! -f "$PEM_FILE" ]; then
    print_error "PEM file not found: $PEM_FILE"
    exit 1
fi

# Fix PEM file permissions
print_status "Setting PEM file permissions..."
chmod 400 "$PEM_FILE"

# Test SSH connection
print_status "Testing SSH connection..."
if ! ssh -i "$PEM_FILE" -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$USERNAME@$EC2_IP" "echo 'Connection successful'" 2>/dev/null; then
    print_error "Failed to connect to EC2 instance"
    print_error "Please check:"
    print_error "  1. PEM file path is correct"
    print_error "  2. EC2 IP address is correct"
    print_error "  3. EC2 instance is running"
    print_error "  4. Security group allows SSH (port 22)"
    exit 1
fi

print_status "SSH connection successful!"

# Create temporary directory on EC2
print_status "Creating temporary directory on EC2..."
ssh -i "$PEM_FILE" -o StrictHostKeyChecking=no "$USERNAME@$EC2_IP" "mkdir -p /tmp/obesity-prediction"

# Upload application files
print_status "Uploading application files to EC2..."
if ! scp -i "$PEM_FILE" -o StrictHostKeyChecking=no -r ./* "$USERNAME@$EC2_IP:/tmp/obesity-prediction/"; then
    print_error "Failed to upload files"
    exit 1
fi

print_status "Files uploaded successfully!"

# Run setup script on EC2
print_status "Running setup script on EC2..."
ssh -i "$PEM_FILE" -o StrictHostKeyChecking=no "$USERNAME@$EC2_IP" << 'EOF'
    chmod +x /tmp/obesity-prediction/ec2_setup.sh
    sudo /tmp/obesity-prediction/ec2_setup.sh
EOF

# Check service status
print_status "Checking service status..."
ssh -i "$PEM_FILE" -o StrictHostKeyChecking=no "$USERNAME@$EC2_IP" "sudo systemctl status obesity-prediction.service --no-pager"

# Get public IP
print_status "Getting EC2 public IP..."
PUBLIC_IP=$(ssh -i "$PEM_FILE" -o StrictHostKeyChecking=no "$USERNAME@$EC2_IP" "curl -s http://169.254.169.254/latest/meta-data/public-ipv4")

if [ -n "$PUBLIC_IP" ]; then
    print_status "EC2 Public IP: $PUBLIC_IP"
    print_status "Application URL: http://$PUBLIC_IP:5000"
else
    print_warning "Could not retrieve public IP automatically"
    print_status "Application should be available at: http://$EC2_IP:5000"
fi

print_status "Deployment completed!"
echo ""
echo "=== Deployment Summary ==="
echo "EC2 Instance IP: $EC2_IP"
echo "Public IP: $PUBLIC_IP"
echo "Application URL: http://${PUBLIC_IP:-$EC2_IP}:5000"
echo ""
echo "Useful commands:"
echo "  SSH into instance: ssh -i $PEM_FILE $USERNAME@$EC2_IP"
echo "  Check service: sudo systemctl status obesity-prediction.service"
echo "  View logs: sudo journalctl -u obesity-prediction.service -f"
echo "  Restart service: sudo systemctl restart obesity-prediction.service"
echo "  Stop service: sudo systemctl stop obesity-prediction.service"
echo ""
print_status "Make sure your EC2 security group allows inbound traffic on port 5000!" 