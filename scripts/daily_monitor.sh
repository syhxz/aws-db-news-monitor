#!/bin/bash
# Daily AWS Database News Monitor Script
# Automated monitoring with optional notifications

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${AWS_DB_MONITOR_OUTPUT_DIR:-$HOME/aws-db-reports}"
LOG_FILE="${AWS_DB_MONITOR_LOG_FILE:-$OUTPUT_DIR/aws_db_monitor.log}"
CONFIG_FILE="$SKILL_DIR/config/config.yaml"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "$LOG_FILE"
}

log_message "Starting AWS Database News Monitor..."

# Check for required Python packages
if ! python3 -c "import feedparser, requests" 2>/dev/null; then
    log_message "Installing required Python packages..."
    pip3 install --user feedparser requests
fi

# Run the monitor
log_message "Fetching and analyzing AWS announcements..."

if python3 "$SCRIPT_DIR/monitor.py" --config "$CONFIG_FILE" --output-dir "$OUTPUT_DIR" --save --output-format json; then
    log_message "Monitor completed successfully"
    
    # Check if we found any database features
    TODAY=$(date '+%Y-%m-%d')
    JSON_FILE="$OUTPUT_DIR/aws_db_features_$TODAY.json"
    
    if [ -f "$JSON_FILE" ]; then
        DB_COUNT=$(python3 -c "
import json
try:
    with open('$JSON_FILE', 'r') as f:
        data = json.load(f)
    print(data.get('count', 0))
except:
    print(0)
")
        
        log_message "Found $DB_COUNT database-related features"
        
        # Send notification if features found and notifications enabled
        if [ "$DB_COUNT" -gt 0 ] && [ "${AWS_DB_MONITOR_NOTIFICATION:-false}" = "true" ]; then
            log_message "Sending notification for $DB_COUNT features..."
            
            if python3 "$SCRIPT_DIR/send_notification.py" --data-file "$JSON_FILE" --config "$CONFIG_FILE"; then
                log_message "Notification sent successfully"
            else
                log_message "Failed to send notification"
            fi
        fi
    else
        log_message "No output file generated"
    fi
else
    log_message "Monitor failed with exit code $?"
    exit 1
fi

log_message "AWS Database News Monitor completed"