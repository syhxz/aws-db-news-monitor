# Changelog

## [1.0.0] - 2026-03-19

### Added
- Initial release of AWS Database News Monitor skill
- RSS feed monitoring from AWS official announcements
- Intelligent filtering for database-related content
- Comprehensive feature analysis including:
  - Service identification (RDS, Aurora, DynamoDB, etc.)
  - Feature categorization (performance, security, backup, etc.)
  - Use case analysis (analytics, real-time, enterprise, etc.)
  - Advantage identification (performance, cost, scalability, etc.)
  - Usage guidance extraction
- Multiple output formats (JSON and Markdown)
- Notification support for multiple platforms:
  - Webhook integration (Slack, Teams, Discord)
  - Feishu integration (via OpenClaw)
  - Email notifications
- Automated daily monitoring with cron integration
- Comprehensive configuration system via YAML
- Example configurations and documentation
- Test suite for validation
- MIT license

### Features
- Monitor 15+ AWS database services
- 50+ database-related keywords for accurate filtering
- Automatic HTML tag cleaning and content formatting
- Rate limiting and retry mechanisms
- Configurable output directories and file naming
- Environment variable support for containerized deployments
- Debug mode for troubleshooting
- Extensive logging capabilities

### Documentation
- Complete skill documentation (SKILL.md)
- Configuration examples
- Usage guides and examples
- Troubleshooting section
- API documentation for integration