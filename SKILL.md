---
name: aws-db-news-monitor
description: Monitor AWS database service announcements and analyze new features automatically. Fetches from AWS RSS feed, filters database-related news, analyzes features with use cases and advantages, and optionally sends notifications.
---

# AWS Database News Monitor

Automatically monitor AWS database service announcements and provide intelligent analysis of new features.

## Features

- **RSS Feed Monitoring**: Fetches latest announcements from AWS official RSS feed
- **Intelligent Filtering**: Identifies database-related announcements using comprehensive keyword matching
- **Feature Analysis**: Automatically analyzes:
  - Service identification (RDS, Aurora, DynamoDB, etc.)
  - Feature categories (performance, security, backup, etc.)
  - Use cases and scenarios
  - Key advantages and benefits
  - Usage guidance
- **Multiple Output Formats**: Supports both JSON data and Markdown reports
- **Notification Support**: Can integrate with messaging platforms
- **Comprehensive Coverage**: Monitors all AWS database services

## Supported AWS Database Services

- **Relational**: RDS, Aurora MySQL/PostgreSQL
- **NoSQL**: DynamoDB, DocumentDB
- **Data Warehouse**: Redshift, Timestream
- **Graph**: Neptune
- **Cache**: ElastiCache, MemoryDB
- **Search**: OpenSearch Service
- **Other**: Keyspaces, QLDB, SimpleDB

## Usage

### Basic Monitoring
```bash
# Check for today's database announcements
python3 scripts/monitor.py

# Generate detailed report
python3 scripts/monitor.py --output-format text --hours 24

# JSON output for integration
python3 scripts/monitor.py --output-format json --limit 10
```

### Automated Monitoring
```bash
# Set up daily monitoring (example for crontab)
# Runs daily at 09:30 UTC
30 09 * * * /path/to/aws-db-news-monitor/scripts/daily_monitor.sh

# Or use the setup script
bash scripts/setup_cron.sh
```

### Testing
```bash
# Test the monitoring functionality
python3 scripts/test_monitor.py

# Test notification system
python3 scripts/test_notification.py
```

## Configuration

### Environment Variables
- `AWS_DB_MONITOR_OUTPUT_DIR`: Output directory for reports (default: current directory)
- `AWS_DB_MONITOR_LOG_FILE`: Log file path (default: aws_db_monitor.log)
- `AWS_DB_MONITOR_NOTIFICATION`: Enable notifications (true/false)

### Notification Setup
Edit `config/notification_config.yaml` to configure your preferred notification method:
```yaml
notification:
  enabled: true
  method: "feishu"  # or "webhook", "email"
  target: "your_target_id"
  webhook_url: "https://your-webhook-url"
```

## Output Format

### JSON Structure
```json
{
  "date": "2026-03-19",
  "total_announcements": 100,
  "database_features": [
    {
      "title": "Feature Title",
      "service": "Amazon RDS",
      "categories": ["Performance Optimization"],
      "use_cases": ["Enterprise Applications"],
      "advantages": ["Improved Performance"],
      "usage_guide": ["AWS Console Configuration"],
      "description": "Feature description...",
      "link": "https://aws.amazon.com/...",
      "published_date": "2026-03-19"
    }
  ],
  "count": 5
}
```

### Report Format
- Executive summary with statistics
- Feature-by-feature analysis
- Usage scenarios and benefits
- Implementation guidance
- Links to detailed documentation

## Requirements

- Python 3.7+
- feedparser library
- requests library
- Internet connection for RSS feed access

## Installation

1. Clone or download this skill
2. Install dependencies: `pip install -r requirements.txt`
3. Configure notification settings if needed
4. Run manually or set up automated monitoring

## Customization

### Adding Keywords
Edit `config/keywords.yaml` to add new database-related keywords:
```yaml
database_keywords:
  services:
    - "your_service_name"
  features:
    - "your_feature_keyword"
```

### Custom Analysis Rules
Extend the analysis logic in `scripts/analyzer.py` to add custom feature categorization rules.

## Examples

See the `examples/` directory for:
- Sample output files
- Integration examples
- Notification templates
- Crontab configurations

## Troubleshooting

### Common Issues
1. **No announcements found**: Check RSS feed accessibility
2. **Keyword matching issues**: Review and update keyword lists
3. **Notification failures**: Verify notification configuration

### Debug Mode
```bash
python3 scripts/monitor.py --debug
```

### Logs
Check the log file for detailed execution information:
```bash
tail -f aws_db_monitor.log
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review example configurations
- Open an issue on GitHub