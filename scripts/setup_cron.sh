#!/bin/bash
# Setup automated monitoring with crontab

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_SCRIPT="$SCRIPT_DIR/daily_monitor.sh"

echo "🔧 Setting up AWS Database News Monitor automation..."

# Make scripts executable
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$SCRIPT_DIR"/*.py

# Get current crontab (if exists)
TEMP_CRONTAB=$(mktemp)
crontab -l 2>/dev/null | grep -v "aws-db-news-monitor" > "$TEMP_CRONTAB" || true

# Ask user for schedule
echo "Choose monitoring schedule:"
echo "1) Daily at 09:30 UTC (recommended)"
echo "2) Daily at 12:00 UTC" 
echo "3) Daily at 18:00 UTC"
echo "4) Custom schedule"
echo -n "Enter choice (1-4): "

read -r choice

case $choice in
    1)
        CRON_SCHEDULE="30 9 * * *"
        TIME_DESC="09:30 UTC daily"
        ;;
    2)
        CRON_SCHEDULE="0 12 * * *"
        TIME_DESC="12:00 UTC daily"
        ;;
    3)
        CRON_SCHEDULE="0 18 * * *"
        TIME_DESC="18:00 UTC daily"
        ;;
    4)
        echo -n "Enter cron schedule (e.g., '30 9 * * *' for daily at 09:30): "
        read -r CRON_SCHEDULE
        TIME_DESC="custom schedule: $CRON_SCHEDULE"
        ;;
    *)
        echo "Invalid choice, using default (09:30 UTC daily)"
        CRON_SCHEDULE="30 9 * * *"
        TIME_DESC="09:30 UTC daily"
        ;;
esac

# Add new cron job
echo "# AWS Database News Monitor - $TIME_DESC" >> "$TEMP_CRONTAB"
echo "$CRON_SCHEDULE $DAILY_SCRIPT" >> "$TEMP_CRONTAB"

# Install new crontab
crontab "$TEMP_CRONTAB"
rm "$TEMP_CRONTAB"

echo "✅ Cron job installed successfully!"
echo "📅 Schedule: $TIME_DESC"
echo "📝 Command: $DAILY_SCRIPT"
echo ""
echo "Current crontab:"
crontab -l | grep -A1 -B1 "aws-db-news-monitor" || echo "No entries found"
echo ""
echo "🔧 To modify the schedule later:"
echo "   crontab -e"
echo ""
echo "📋 To view logs:"
echo "   tail -f \$HOME/aws-db-reports/aws_db_monitor.log"