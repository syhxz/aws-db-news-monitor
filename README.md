# AWS Database News Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

An intelligent monitoring system for AWS database service announcements. Automatically fetches, filters, and analyzes AWS database-related features from official RSS feeds with comprehensive reporting and notification capabilities.

## ✨ Features

- **🔍 Intelligent Filtering**: Identifies database-related announcements using 50+ keywords
- **🧠 Smart Analysis**: Automatically categorizes features, identifies use cases, and extracts advantages
- **📊 Multiple Outputs**: JSON data and Markdown reports
- **🔔 Multi-Platform Notifications**: Webhook, Feishu, and email support
- **⏰ Automated Monitoring**: Cron integration for daily monitoring
- **🗄️ Comprehensive Coverage**: Monitors all AWS database services (RDS, Aurora, DynamoDB, etc.)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/aws-db-news-monitor.git
cd aws-db-news-monitor

# Install dependencies
pip install -r requirements.txt

# Run a test
python3 scripts/test_monitor.py
```

### Basic Usage

```bash
# Check today's database announcements
python3 scripts/monitor.py --save

# Generate detailed report
python3 scripts/monitor.py --output-format text --limit 20

# JSON output for integration
python3 scripts/monitor.py --output-format json
```

### Automated Setup

```bash
# Interactive setup with cron scheduling
bash scripts/setup_cron.sh
```

## 📋 Supported AWS Services

| Service | Coverage |
|---------|----------|
| **Relational** | RDS, Aurora MySQL/PostgreSQL |
| **NoSQL** | DynamoDB, DocumentDB |
| **Data Warehouse** | Redshift, Timestream |
| **Graph** | Neptune |
| **Cache** | ElastiCache, MemoryDB |
| **Search** | OpenSearch Service |
| **Other** | Keyspaces, QLDB, SimpleDB |

## ⚙️ Configuration

Create or modify `config/config.yaml`:

```yaml
# Basic configuration
notification:
  enabled: true
  method: "webhook"
  webhook_url: "https://your-webhook-url"

# Output settings  
output:
  directory: "./reports"
  
# Custom keywords
keywords:
  database:
    - "your_custom_keyword"
```

## 🔔 Notification Setup

### Webhook (Slack, Teams, Discord)
```yaml
notification:
  enabled: true
  method: "webhook"
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Feishu Integration
```yaml
notification:
  enabled: true
  method: "feishu"
  feishu:
    target: "ou_your_user_id"
```

### Email Notifications
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

## 📊 Sample Output

```json
{
  "date": "2026-03-19",
  "total_announcements": 100,
  "database_features": [
    {
      "title": "Amazon RDS for PostgreSQL now supports...",
      "service": "Amazon RDS",
      "categories": ["Performance Optimization"],
      "use_cases": ["Enterprise Applications"],
      "advantages": ["Improved Performance"],
      "usage_guide": ["AWS Console Configuration"],
      "link": "https://aws.amazon.com/..."
    }
  ],
  "count": 8
}
```

## 🛠️ Development

### Running Tests
```bash
python3 scripts/test_monitor.py
```

### Debug Mode
```bash
python3 scripts/monitor.py --debug
```

## 📖 Documentation

- [Complete Documentation](SKILL.md)
- [Configuration Guide](config/config.yaml)
- [Examples](examples/)
- [Changelog](CHANGELOG.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS for providing comprehensive RSS feeds
- OpenClaw community for integration support
- Contributors and users who provide feedback and improvements

## 📞 Support

- 📋 [Issues](https://github.com/your-username/aws-db-news-monitor/issues)
- 📚 [Documentation](SKILL.md)
- 💬 [Discussions](https://github.com/your-username/aws-db-news-monitor/discussions)