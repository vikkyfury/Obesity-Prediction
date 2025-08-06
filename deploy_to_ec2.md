# EC2 Deployment Guide for Obesity Prediction Application

This guide will walk you through deploying the Obesity Prediction web application on an Amazon EC2 instance.

## Prerequisites

1. An AWS account with EC2 access
2. Basic knowledge of AWS EC2 and security groups
3. SSH access to your EC2 instance

## Step 1: Launch an EC2 Instance

### 1.1 Choose an Instance Type
- **Recommended**: t2.micro (free tier) or t3.small for better performance
- **OS**: Amazon Linux 2 AMI (recommended) or Ubuntu Server 20.04 LTS

### 1.2 Configure Security Group
Create or modify the security group to allow the following inbound traffic:
- **SSH (Port 22)**: Your IP address
- **HTTP (Port 80)**: 0.0.0.0/0 (optional, for future use)
- **Custom TCP (Port 5000)**: 0.0.0.0/0 (for the Flask application)

### 1.3 Launch the Instance
1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose Amazon Linux 2 AMI
4. Select your desired instance type
5. Configure security group as above
6. Launch and download your key pair (.pem file)

## Step 2: Connect to Your EC2 Instance

```bash
# Connect via SSH (replace with your instance details)
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

## Step 3: Upload Application Files

### Option A: Using SCP (from your local machine)
```bash
# Create a temporary directory on EC2
ssh -i your-key.pem ec2-user@your-ec2-public-ip "mkdir -p /tmp/obesity-prediction"

# Upload files from your local machine
scp -i your-key.pem -r /path/to/your/obesity-prediction/* ec2-user@your-ec2-public-ip:/tmp/obesity-prediction/
```

### Option B: Using Git (if your code is in a repository)
```bash
# On EC2 instance
sudo yum install -y git
git clone https://github.com/your-username/obesity-prediction.git /tmp/obesity-prediction
```

## Step 4: Run the Setup Script

```bash
# Make the setup script executable
chmod +x /tmp/obesity-prediction/ec2_setup.sh

# Run the setup script
sudo /tmp/obesity-prediction/ec2_setup.sh
```

## Step 5: Verify Deployment

### 5.1 Check Service Status
```bash
sudo systemctl status obesity-prediction.service
```

### 5.2 Check Application Logs
```bash
sudo journalctl -u obesity-prediction.service -f
```

### 5.3 Test the Application
Open your web browser and navigate to:
```
http://YOUR_EC2_PUBLIC_IP:5000
```

## Step 6: Optional - Set Up Domain Name

### 6.1 Using Route 53 (AWS DNS)
1. Register a domain or use an existing one
2. Create an A record pointing to your EC2 public IP
3. Wait for DNS propagation (can take up to 48 hours)

### 6.2 Using a Custom Domain
1. Point your domain's A record to your EC2 public IP
2. Update your application configuration if needed

## Step 7: SSL/HTTPS Setup (Recommended for Production)

### 7.1 Install Certbot
```bash
# For Amazon Linux 2
sudo yum install -y certbot python3-certbot-nginx

# For Ubuntu
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx
```

### 7.2 Set Up Nginx as Reverse Proxy
```bash
# Install Nginx
sudo yum install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/conf.d/obesity-prediction.conf > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 7.3 Obtain SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com
```

## Troubleshooting

### Common Issues

#### 1. Application Not Starting
```bash
# Check service status
sudo systemctl status obesity-prediction.service

# View detailed logs
sudo journalctl -u obesity-prediction.service -f
```

#### 2. Port 5000 Not Accessible
- Verify security group allows inbound traffic on port 5000
- Check if firewall is blocking the port
- Ensure the application is running on 0.0.0.0:5000

#### 3. Dependencies Installation Failed
```bash
# Install system dependencies manually
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3-devel gcc gcc-c++ make

# Reinstall Python packages
source /opt/obesity-prediction/venv/bin/activate
pip install -r requirements.txt
```

#### 4. Memory Issues
- Consider upgrading to a larger instance type
- Monitor memory usage: `free -h`
- Restart the service: `sudo systemctl restart obesity-prediction.service`

## Maintenance

### Updating the Application
```bash
# Stop the service
sudo systemctl stop obesity-prediction.service

# Update code (upload new files or pull from git)
# Install new dependencies if needed
source /opt/obesity-prediction/venv/bin/activate
pip install -r requirements.txt

# Start the service
sudo systemctl start obesity-prediction.service
```

### Monitoring
```bash
# Check service status
sudo systemctl status obesity-prediction.service

# View real-time logs
sudo journalctl -u obesity-prediction.service -f

# Check system resources
htop
df -h
free -h
```

### Backup
```bash
# Create backup of application
sudo tar -czf /tmp/obesity-prediction-backup-$(date +%Y%m%d).tar.gz /opt/obesity-prediction
```

## Security Best Practices

1. **Regular Updates**: Keep your EC2 instance updated
2. **Security Groups**: Only open necessary ports
3. **SSH Keys**: Use key-based authentication, disable password login
4. **Firewall**: Configure firewalld or iptables
5. **SSL**: Always use HTTPS in production
6. **Monitoring**: Set up CloudWatch alarms for monitoring

## Cost Optimization

1. **Instance Type**: Use appropriate instance size for your traffic
2. **Reserved Instances**: Consider reserved instances for long-term deployments
3. **Auto Scaling**: Set up auto scaling for variable traffic
4. **Shutdown**: Stop instances when not in use (for development)

## Support

If you encounter issues:
1. Check the application logs: `sudo journalctl -u obesity-prediction.service`
2. Verify security group settings in AWS Console
3. Test connectivity: `curl http://localhost:5000`
4. Check system resources: `htop`, `df -h`, `free -h` 