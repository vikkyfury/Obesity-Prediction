# EC2 Deployment Summary for Obesity Prediction Application

## Overview

This repository now includes all necessary files to deploy the Obesity Prediction web application on Amazon EC2. The deployment is configured for production use with proper security, logging, and monitoring.

## Files Created for EC2 Deployment

### 1. **deploy_ec2.py** - Python Deployment Script
- **Purpose**: Python-based deployment script with modular functions
- **Usage**: 
  ```bash
  python deploy_ec2.py                    # Full deployment
  python deploy_ec2.py --install-only     # Only install dependencies
  python deploy_ec2.py --run-only         # Only run the application
  ```

### 2. **ec2_setup.sh** - Complete Setup Script
- **Purpose**: Comprehensive setup script for production deployment
- **Features**:
  - Installs all system dependencies
  - Sets up Python virtual environment
  - Configures Gunicorn for production
  - Creates systemd service for auto-start
  - Configures firewall rules
- **Usage**: `sudo ./ec2_setup.sh`

### 3. **quick_deploy.sh** - Simplified Deployment
- **Purpose**: Quick deployment for development/testing
- **Features**:
  - Minimal setup for fast deployment
  - Uses Flask development server
  - Basic systemd service
- **Usage**: `sudo ./quick_deploy.sh`

### 4. **gunicorn_config.py** - Production WSGI Configuration
- **Purpose**: Gunicorn configuration for production deployment
- **Features**:
  - Multiple worker processes
  - Proper logging configuration
  - Memory leak prevention
  - SSL ready (commented out)

### 5. **deploy_to_ec2.md** - Comprehensive Deployment Guide
- **Purpose**: Step-by-step deployment instructions
- **Contents**:
  - EC2 instance setup
  - Security group configuration
  - SSL/HTTPS setup
  - Troubleshooting guide
  - Maintenance procedures

## Updated Files

### 1. **web_app/app.py** - Production-Ready Flask App
- **Changes**:
  - Added environment variable support
  - Configurable host and port
  - Production-ready settings
  - Proper error handling

### 2. **requirements.txt** - Optimized Dependencies
- **Changes**:
  - Removed unnecessary packages (tensorflow, jupyter, etc.)
  - Added Gunicorn for production WSGI server
  - Kept only essential packages for web app

## Quick Start Guide

### Option 1: Quick Deployment (Recommended for Testing)
```bash
# 1. Upload files to EC2
scp -i your-key.pem -r ./* ec2-user@your-ec2-ip:/tmp/obesity-prediction/

# 2. SSH to EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# 3. Run quick deployment
sudo chmod +x /tmp/obesity-prediction/quick_deploy.sh
sudo /tmp/obesity-prediction/quick_deploy.sh
```

### Option 2: Production Deployment
```bash
# 1. Upload files to EC2
scp -i your-key.pem -r ./* ec2-user@your-ec2-ip:/tmp/obesity-prediction/

# 2. SSH to EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# 3. Run production setup
sudo chmod +x /tmp/obesity-prediction/ec2_setup.sh
sudo /tmp/obesity-prediction/ec2_setup.sh
```

## Security Group Configuration

**IMPORTANT**: Configure your EC2 security group to allow:
- **SSH (Port 22)**: Your IP address
- **Custom TCP (Port 5000)**: 0.0.0.0/0 (for web access)

## Application Access

After deployment, your application will be available at:
```
http://YOUR_EC2_PUBLIC_IP:5000
```

## Monitoring and Maintenance

### Check Application Status
```bash
sudo systemctl status obesity-prediction.service
```

### View Logs
```bash
# System logs
sudo journalctl -u obesity-prediction.service -f

# Application logs (production deployment)
tail -f /opt/obesity-prediction/logs/access.log
tail -f /opt/obesity-prediction/logs/error.log
```

### Restart Application
```bash
sudo systemctl restart obesity-prediction.service
```

### Update Application
```bash
# Stop service
sudo systemctl stop obesity-prediction.service

# Upload new files
scp -i your-key.pem -r ./* ec2-user@your-ec2-ip:/tmp/obesity-prediction/

# Copy to app directory
sudo cp -r /tmp/obesity-prediction/* /opt/obesity-prediction/

# Install new dependencies (if any)
cd /opt/obesity-prediction
source venv/bin/activate
pip install -r requirements.txt

# Start service
sudo systemctl start obesity-prediction.service
```

## Troubleshooting

### Common Issues

1. **Application not starting**
   ```bash
   sudo systemctl status obesity-prediction.service
   sudo journalctl -u obesity-prediction.service -f
   ```

2. **Port 5000 not accessible**
   - Check security group settings in AWS Console
   - Verify firewall configuration: `sudo firewall-cmd --list-all`

3. **Dependencies installation failed**
   ```bash
   sudo yum groupinstall -y "Development Tools"
   sudo yum install -y python3-devel gcc gcc-c++ make
   ```

4. **Memory issues**
   - Monitor memory: `free -h`
   - Consider upgrading instance type
   - Restart service: `sudo systemctl restart obesity-prediction.service`

## Production Recommendations

1. **Use HTTPS**: Set up SSL certificate with Let's Encrypt
2. **Domain Name**: Configure a domain name for your application
3. **Monitoring**: Set up CloudWatch alarms
4. **Backup**: Regular backups of application data
5. **Updates**: Keep system and application updated
6. **Security**: Regular security audits and updates

## Cost Optimization

1. **Instance Type**: Use appropriate size for your traffic
2. **Reserved Instances**: For long-term deployments
3. **Auto Scaling**: For variable traffic patterns
4. **Shutdown**: Stop instances when not in use (development)

## Support

For issues or questions:
1. Check the comprehensive guide: `deploy_to_ec2.md`
2. Review logs: `sudo journalctl -u obesity-prediction.service`
3. Verify security group settings in AWS Console
4. Test connectivity: `curl http://localhost:5000`

---

**Note**: This deployment setup is optimized for Amazon Linux 2. For other distributions, minor modifications may be required. 