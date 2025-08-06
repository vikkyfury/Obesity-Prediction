#!/usr/bin/env python3
"""
EC2 Deployment Script using PEM file for Obesity Prediction Web Application
"""

import os
import sys
import subprocess
import argparse
import json
import time
from pathlib import Path

class EC2Deployer:
    def __init__(self, pem_file, ec2_ip, username="ec2-user"):
        self.pem_file = pem_file
        self.ec2_ip = ec2_ip
        self.username = username
        self.project_dir = Path(__file__).parent
        self.remote_app_dir = "/opt/obesity-prediction"
        
    def check_pem_file(self):
        """Check if PEM file exists and has correct permissions"""
        if not os.path.exists(self.pem_file):
            print(f"Error: PEM file not found at {self.pem_file}")
            return False
            
        # Check and fix permissions
        stat = os.stat(self.pem_file)
        if stat.st_mode & 0o777 != 0o400:
            print(f"Fixing PEM file permissions...")
            os.chmod(self.pem_file, 0o400)
            
        return True
    
    def run_ssh_command(self, command, capture_output=False):
        """Run SSH command on EC2 instance"""
        ssh_cmd = [
            "ssh", "-i", self.pem_file, "-o", "StrictHostKeyChecking=no",
            f"{self.username}@{self.ec2_ip}", command
        ]
        
        try:
            if capture_output:
                result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            else:
                subprocess.run(ssh_cmd, check=True)
                return True
        except subprocess.CalledProcessError as e:
            print(f"SSH command failed: {e}")
            return False
    
    def run_scp_command(self, local_path, remote_path, upload=True):
        """Upload or download files using SCP"""
        scp_cmd = [
            "scp", "-i", self.pem_file, "-o", "StrictHostKeyChecking=no"
        ]
        
        if upload:
            scp_cmd.extend([local_path, f"{self.username}@{self.ec2_ip}:{remote_path}"])
        else:
            scp_cmd.extend([f"{self.username}@{self.ec2_ip}:{remote_path}", local_path])
            
        try:
            subprocess.run(scp_cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"SCP command failed: {e}")
            return False
    
    def test_connection(self):
        """Test SSH connection to EC2 instance"""
        print("Testing SSH connection...")
        return self.run_ssh_command("echo 'Connection successful'")
    
    def upload_files(self):
        """Upload application files to EC2"""
        print("Uploading application files to EC2...")
        
        # Create temporary directory on EC2
        self.run_ssh_command(f"mkdir -p /tmp/obesity-prediction")
        
        # Upload all project files
        print("Uploading project files...")
        if not self.run_scp_command(
            f"{self.project_dir}/*",
            "/tmp/obesity-prediction/",
            upload=True
        ):
            print("Failed to upload files")
            return False
            
        print("Files uploaded successfully!")
        return True
    
    def setup_ec2_environment(self):
        """Set up the EC2 environment"""
        print("Setting up EC2 environment...")
        
        # Run the setup script
        setup_commands = [
            "chmod +x /tmp/obesity-prediction/ec2_setup.sh",
            "sudo /tmp/obesity-prediction/ec2_setup.sh"
        ]
        
        for cmd in setup_commands:
            if not self.run_ssh_command(cmd):
                print(f"Failed to run: {cmd}")
                return False
                
        return True
    
    def check_service_status(self):
        """Check if the service is running"""
        print("Checking service status...")
        status = self.run_ssh_command("sudo systemctl status obesity-prediction.service", capture_output=True)
        print(status)
        return "active (running)" in status
    
    def get_ec2_info(self):
        """Get EC2 instance information"""
        print("Getting EC2 instance information...")
        info = self.run_ssh_command("curl -s http://169.254.169.254/latest/meta-data/public-ipv4", capture_output=True)
        if info:
            print(f"EC2 Public IP: {info}")
        return info
    
    def deploy(self):
        """Main deployment method"""
        print("=== EC2 Deployment with PEM File ===")
        
        # Check PEM file
        if not self.check_pem_file():
            return False
            
        # Test connection
        if not self.test_connection():
            print("Failed to connect to EC2 instance")
            return False
            
        # Upload files
        if not self.upload_files():
            return False
            
        # Setup environment
        if not self.setup_ec2_environment():
            return False
            
        # Check service status
        if not self.check_service_status():
            print("Warning: Service might not be running properly")
            
        # Get EC2 info
        public_ip = self.get_ec2_info()
        
        print("\n=== Deployment Summary ===")
        print(f"EC2 Instance IP: {self.ec2_ip}")
        print(f"Public IP: {public_ip}")
        print(f"Application URL: http://{public_ip}:5000")
        print("\nUseful commands:")
        print(f"  SSH into instance: ssh -i {self.pem_file} {self.username}@{self.ec2_ip}")
        print("  Check service: sudo systemctl status obesity-prediction.service")
        print("  View logs: sudo journalctl -u obesity-prediction.service -f")
        print("  Restart service: sudo systemctl restart obesity-prediction.service")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Deploy Obesity Prediction App to EC2 using PEM file')
    parser.add_argument('--pem-file', required=True, help='Path to your PEM file')
    parser.add_argument('--ec2-ip', required=True, help='EC2 instance IP address')
    parser.add_argument('--username', default='ec2-user', help='EC2 username (default: ec2-user)')
    parser.add_argument('--test-only', action='store_true', help='Only test connection')
    
    args = parser.parse_args()
    
    deployer = EC2Deployer(args.pem_file, args.ec2_ip, args.username)
    
    if args.test_only:
        if deployer.test_connection():
            print("Connection test successful!")
        else:
            print("Connection test failed!")
        return
    
    success = deployer.deploy()
    if success:
        print("\n✅ Deployment completed successfully!")
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 