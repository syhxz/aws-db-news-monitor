#!/usr/bin/env python3
"""
Notification sender for AWS Database News Monitor
Supports multiple notification methods
"""

import json
import argparse
import sys
import os
from pathlib import Path

class NotificationSender:
    def __init__(self, config=None):
        self.config = config or {}
    
    def load_data(self, data_file):
        """Load monitoring results from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data file {data_file}: {e}")
            return None
    
    def format_message(self, data):
        """Format data into notification message"""
        count = data.get('count', 0)
        
        if count == 0:
            return None  # No message needed
        
        message = f"""📰 AWS Database Features Daily Report

📅 Date: {data['date']}
📊 Total AWS Announcements: {data['total_announcements']}
🗄️ Database-Related: {count}

🏆 Key Features:
"""
        
        # Add top 3 features
        for i, feature in enumerate(data['database_features'][:3], 1):
            use_cases = ', '.join(feature.get('use_cases', ['General Use'])[:2])
            message += f"""
{i}. {feature['service']}
   {feature['title'][:80]}...
   💡 {use_cases}
"""
        
        if count > 3:
            message += f"\n... and {count-3} more database features"
        
        message += "\n\nView detailed analysis and usage guidance in the full report."
        
        return message
    
    def send_webhook(self, message, webhook_url):
        """Send notification via webhook"""
        import requests
        
        payload = {
            "text": message,
            "msgtype": "text"
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Webhook notification failed: {e}")
            return False
    
    def send_feishu(self, message, target_id):
        """Send notification via Feishu (if OpenClaw available)"""
        try:
            # Try to use OpenClaw's message function
            sys.path.append('/usr/local/lib/node_modules/openclaw')
            from openclaw import message as send_message
            
            send_message(
                action='send',
                channel='feishu',
                target=target_id,
                message=message
            )
            return True
        except Exception as e:
            print(f"Feishu notification failed: {e}")
            return False
    
    def send_email(self, message, email_config):
        """Send notification via email"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config.get('from')
            msg['To'] = email_config.get('to')
            msg['Subject'] = "AWS Database Features Daily Report"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port', 587))
            server.starttls()
            server.login(email_config.get('username'), email_config.get('password'))
            
            text = msg.as_string()
            server.sendmail(email_config.get('from'), email_config.get('to'), text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False
    
    def send_notification(self, data):
        """Send notification based on configuration"""
        notification_config = self.config.get('notification', {})
        
        if not notification_config.get('enabled', False):
            print("Notifications disabled")
            return True
        
        message = self.format_message(data)
        if not message:
            print("No notification needed (no database features found)")
            return True
        
        method = notification_config.get('method', '').lower()
        
        if method == 'webhook':
            webhook_url = notification_config.get('webhook_url')
            if webhook_url:
                return self.send_webhook(message, webhook_url)
            else:
                print("Webhook URL not configured")
                return False
        
        elif method == 'feishu':
            target_id = notification_config.get('target')
            if target_id:
                return self.send_feishu(message, target_id)
            else:
                print("Feishu target ID not configured")
                return False
        
        elif method == 'email':
            email_config = notification_config.get('email', {})
            if email_config:
                return self.send_email(message, email_config)
            else:
                print("Email configuration missing")
                return False
        
        else:
            print(f"Unsupported notification method: {method}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Send AWS database news notifications')
    parser.add_argument('--data-file', required=True,
                       help='JSON data file from monitor')
    parser.add_argument('--config', 
                       help='Configuration file path')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - show message without sending')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if args.config and os.path.exists(args.config):
        try:
            import yaml
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f) or {}
        except ImportError:
            print("Warning: PyYAML not available, using default config")
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
    
    sender = NotificationSender(config)
    
    # Load monitoring data
    data = sender.load_data(args.data_file)
    if not data:
        sys.exit(1)
    
    # Format message
    message = sender.format_message(data)
    if not message:
        print("No notification needed")
        sys.exit(0)
    
    if args.test:
        print("Test mode - would send:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        sys.exit(0)
    
    # Send notification
    if sender.send_notification(data):
        print("✅ Notification sent successfully")
        sys.exit(0)
    else:
        print("❌ Notification failed")
        sys.exit(1)

if __name__ == "__main__":
    main()