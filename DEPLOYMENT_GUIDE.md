# Obesity Prediction EC2 Deployment Guide

This guide will help you deploy your Obesity Prediction application to EC2 using your PEM file.

## Prerequisites

1. **EC2 Instance**: A running EC2 instance with Amazon Linux 2 or Ubuntu
2. **PEM File**: Your EC2 key pair file (e.g., `obesity_prediction.pem`)
3. **EC2 IP Address**: The public IP address of your EC2 instance
4. **Security Group Configuration**: Ensure your EC2 security group allows:
   - SSH (Port 22) from your IP
   - HTTP (Port 5000) from anywhere (0.0.0.0/0)

## Quick Deployment

### Step 1: Place your PEM file in the project directory

Make sure your PEM file (e.g., `obesity_prediction.pem`) is in the same directory as this project.

### Step 2: Run the deployment script

```bash
# Make the script executable (if not already done)
chmod +x deploy_obesity_prediction.sh

# Run the deployment
./deploy_obesity_prediction.sh obesity_prediction.pem YOUR_EC2_IP_ADDRESS
```

Example:
```bash
./deploy_obesity_prediction.sh obesity_prediction.pem 18.xxx.xxx.xxx
```

### Step 3: Verify deployment

After the script completes, you should see output like:
```
=== Deployment Summary ===
EC2 Instance IP: 18.xxx.xxx.xxx
Public IP: 18.xxx.xxx.xxx
Application URL: http://18.xxx.xxx.xxx:5000
```

## Alternative Deployment Methods

### Method 1: Using Python Script

```bash
python3 deploy_with_pem.py --pem-file obesity_prediction.pem --ec2-ip YOUR_EC2_IP
```

### Method 2: Manual Deployment

If you prefer to deploy manually:

1. **Upload files to EC2**:
```bash
scp -i obesity_prediction.pem -r ./* ec2-user@YOUR_EC2_IP:/tmp/obesity-prediction/
```

2. **SSH into EC2**:
```bash
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP
```

3. **Run setup script**:
```bash
chmod +x /tmp/obesity-prediction/ec2_setup.sh
sudo /tmp/obesity-prediction/ec2_setup.sh
```

## Troubleshooting

### Common Issues

#### 1. PEM File Permissions
```bash
chmod 400 obesity_prediction.pem
```

#### 2. SSH Connection Failed
- Check if EC2 instance is running
- Verify security group allows SSH (port 22)
- Ensure PEM file path is correct
- Try connecting manually: `ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP`

#### 3. Application Not Accessible
- Check security group allows port 5000
- Verify service is running: `sudo systemctl status obesity-prediction.service`
- Check logs: `sudo journalctl -u obesity-prediction.service -f`

#### 4. Dependencies Installation Failed
```bash
# SSH into EC2 and run manually
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP
sudo yum update -y
sudo yum install -y python3 python3-pip
sudo yum groupinstall -y "Development Tools"
```

## Post-Deployment

### Useful Commands

```bash
# SSH into your EC2 instance
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP

# Check service status
sudo systemctl status obesity-prediction.service

# View real-time logs
sudo journalctl -u obesity-prediction.service -f

# Restart the service
sudo systemctl restart obesity-prediction.service

# Stop the service
sudo systemctl stop obesity-prediction.service

# Check application logs
tail -f /opt/obesity-prediction/logs/access.log
tail -f /opt/obesity-prediction/logs/error.log
```

### Security Group Configuration

Make sure your EC2 security group has these inbound rules:

| Type | Protocol | Port Range | Source |
|------|----------|------------|--------|
| SSH | TCP | 22 | Your IP address |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 |

### Monitoring

```bash
# Check system resources
htop
df -h
free -h

# Check network connectivity
curl http://localhost:5000
```

## Updating the Application

To update your application:

1. **Stop the service**:
```bash
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP "sudo systemctl stop obesity-prediction.service"
```

2. **Upload new files**:
```bash
scp -i obesity_prediction.pem -r ./* ec2-user@YOUR_EC2_IP:/tmp/obesity-prediction/
```

3. **Run setup again**:
```bash
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP "sudo /tmp/obesity-prediction/ec2_setup.sh"
```

4. **Start the service**:
```bash
ssh -i obesity_prediction.pem ec2-user@YOUR_EC2_IP "sudo systemctl start obesity-prediction.service"
```

## Cost Optimization

- Use t2.micro (free tier) for development
- Stop instances when not in use
- Consider reserved instances for production
- Monitor usage with AWS Cost Explorer

## Security Best Practices

1. **Regular Updates**: Keep your EC2 instance updated
2. **Security Groups**: Only open necessary ports
3. **SSH Keys**: Use key-based authentication
4. **Firewall**: Configure additional firewall rules if needed
5. **Monitoring**: Set up CloudWatch alarms
6. **Backup**: Regularly backup your application data

## Support

If you encounter issues:

1. Check the application logs: `sudo journalctl -u obesity-prediction.service`
2. Verify security group settings in AWS Console
3. Test connectivity: `curl http://localhost:5000`
4. Check system resources: `htop`, `df -h`, `free -h`
5. Review the detailed deployment logs in the script output 