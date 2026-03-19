# OpenClaw Skill Integration Guide

This skill can be integrated with OpenClaw for seamless database monitoring and notifications.

## Installation in OpenClaw

### Method 1: Direct Installation
```bash
# Navigate to OpenClaw skills directory
cd ~/.openclaw/workspace/skills/

# Clone the skill
git clone https://github.com/syhxz/aws-db-news-monitor.git

# Install dependencies
cd aws-db-news-monitor
pip3 install --user -r requirements.txt

# Test the installation
python3 scripts/test_monitor.py
```

### Method 2: Using ClawHub (if available)
```bash
# Search for the skill
openclaw skill search aws-db-news

# Install via ClawHub
openclaw skill install aws-db-news-monitor
```

## OpenClaw Integration Features

### Automatic Feishu Integration
When running within OpenClaw, the skill automatically detects and uses OpenClaw's messaging capabilities for Feishu notifications:

```yaml
# config/config.yaml
notification:
  enabled: true
  method: "feishu"
  feishu:
    target: "your_feishu_user_id"  # Your Feishu user ID
```

### Skill Activation
The skill follows OpenClaw skill conventions:

1. **SKILL.md**: Complete documentation and usage guide
2. **Standard structure**: Scripts, config, examples, tests
3. **Environment integration**: Works with OpenClaw's environment
4. **Logging**: Integrates with OpenClaw's logging system

### Usage within OpenClaw

```bash
# From OpenClaw workspace
cd ~/.openclaw/workspace/skills/aws-db-news-monitor

# Run monitoring
python3 scripts/monitor.py --config config/config.yaml --save

# Set up automated monitoring
bash scripts/setup_cron.sh
```

### Message Integration
The skill can send notifications through OpenClaw's message system:

```python
# Automatically detected when OpenClaw is available
from openclaw import message

message(
    action='send',
    channel='feishu',
    target='your_user_id',
    message='AWS Database Features Report...'
)
```

## Configuration for OpenClaw

### Recommended Configuration
Create `config/openclaw.yaml`:

```yaml
# OpenClaw-specific configuration
notification:
  enabled: true
  method: "feishu"
  feishu:
    target: "${OPENCLAW_FEISHU_USER_ID}"  # Environment variable

output:
  directory: "${HOME}/.openclaw/workspace/aws-db-reports"
  log_file: "${HOME}/.openclaw/logs/aws_db_monitor.log"

logging:
  level: "INFO"
  format: "%(asctime)s - AWS-DB-Monitor - %(levelname)s - %(message)s"
```

### Environment Variables
Set these in your OpenClaw environment:

```bash
export OPENCLAW_FEISHU_USER_ID="your_feishu_user_id"
export AWS_DB_MONITOR_OUTPUT_DIR="$HOME/.openclaw/workspace/aws-db-reports"
export AWS_DB_MONITOR_NOTIFICATION="true"
```

## Automation Setup

### Cron Integration
```bash
# Set up daily monitoring (integrates with OpenClaw)
bash scripts/setup_cron.sh

# Or manually add to crontab:
# 30 9 * * * /path/to/.openclaw/workspace/skills/aws-db-news-monitor/scripts/daily_monitor.sh
```

### OpenClaw Heartbeat Integration
Add to your OpenClaw heartbeat configuration:

```markdown
# In ~/.openclaw/workspace/HEARTBEAT.md
### 🗄️ AWS Database News Monitor
- **Status**: ✅ Enabled
- **Schedule**: Daily at 09:30 UTC
- **Notifications**: Feishu (when features found)
- **Last Check**: [Auto-updated]
```

## Skill Structure

```
aws-db-news-monitor/
├── SKILL.md              # OpenClaw skill documentation
├── README.md             # General documentation
├── scripts/
│   ├── monitor.py        # Main monitoring script
│   ├── daily_monitor.sh  # Automated daily script
│   ├── send_notification.py # Notification handler
│   └── test_monitor.py   # Test suite
├── config/
│   ├── config.yaml       # Default configuration
│   └── openclaw.yaml     # OpenClaw-specific config
├── examples/             # Usage examples
└── requirements.txt      # Python dependencies
```

## Troubleshooting

### Common Issues

1. **Notifications not working**
   - Check Feishu user ID configuration
   - Verify OpenClaw messaging is available
   - Test with: `python3 scripts/send_notification.py --test`

2. **Permission issues**
   - Ensure scripts are executable: `chmod +x scripts/*.sh scripts/*.py`
   - Check file permissions for output directory

3. **Missing dependencies**
   - Install requirements: `pip3 install --user -r requirements.txt`
   - For system packages: `sudo apt install python3-feedparser python3-yaml`

### Debug Mode
```bash
python3 scripts/monitor.py --debug --config config/openclaw.yaml
```

### Logs
```bash
# Check OpenClaw logs
tail -f ~/.openclaw/logs/aws_db_monitor.log

# Check cron logs
tail -f /var/log/cron
```

## Support

For OpenClaw-specific issues:
- Check OpenClaw documentation
- Verify skill is properly installed in `~/.openclaw/workspace/skills/`
- Ensure OpenClaw environment is active

For skill-specific issues:
- [GitHub Issues](https://github.com/syhxz/aws-db-news-monitor/issues)
- Review [SKILL.md](SKILL.md) for detailed documentation