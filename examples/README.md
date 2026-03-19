# Example AWS Database Features Output

This directory contains example outputs from the AWS Database News Monitor.

## Files

- `sample_output.json` - Example JSON output with feature analysis
- `sample_report.md` - Example formatted report
- `notification_example.txt` - Example notification message
- `crontab_example.txt` - Example crontab configuration

## Usage Examples

### Basic Monitoring
```bash
# Monitor today's announcements
python3 scripts/monitor.py --save

# Generate report for last 48 hours with specific format
python3 scripts/monitor.py --output-format text --save --limit 50

# JSON output for integration
python3 scripts/monitor.py --output-format json --limit 10
```

### Automated Setup
```bash
# Interactive setup with cron scheduling
bash scripts/setup_cron.sh

# Manual crontab entry (daily at 09:30 UTC)
30 9 * * * /path/to/aws-db-news-monitor/scripts/daily_monitor.sh
```

### Configuration Examples

#### Webhook Notification (Slack)
```yaml
notification:
  enabled: true
  method: "webhook"
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

#### Feishu Notification
```yaml
notification:
  enabled: true
  method: "feishu" 
  feishu:
    target: "ou_your_user_id"
```

#### Email Notification
```yaml
notification:
  enabled: true
  method: "email"
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your_email@gmail.com"
    password: "your_app_password"
    from: "your_email@gmail.com"
    to: "recipient@example.com"
```

### Environment Variables
```bash
# Set custom output directory
export AWS_DB_MONITOR_OUTPUT_DIR="$HOME/aws-reports"

# Enable notifications
export AWS_DB_MONITOR_NOTIFICATION="true"

# Custom log file
export AWS_DB_MONITOR_LOG_FILE="$HOME/logs/aws_db_monitor.log"
```

### Integration with OpenClaw
If you're using this skill within OpenClaw, notifications can be sent directly through OpenClaw's messaging system:

```yaml
notification:
  enabled: true
  method: "feishu"
  feishu:
    target: "your_feishu_user_id"
```

The skill will automatically detect and use OpenClaw's messaging capabilities when available.