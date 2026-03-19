#!/usr/bin/env python3
"""
AWS Database News Monitor - Main Script
Monitors AWS RSS feed for database-related announcements and provides analysis.
"""

import feedparser
import json
import re
import argparse
import sys
import os
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from pathlib import Path

class AWSDBNewsMonitor:
    def __init__(self, config_file=None):
        self.rss_url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Database-related keywords
        self.db_keywords = self.config.get('keywords', {}).get('database', [
            # AWS database services
            'rds', 'aurora', 'dynamodb', 'redshift', 'neptune', 'timestream',
            'documentdb', 'elasticache', 'memorydb', 'keyspaces', 'qldb',
            'quantum ledger', 'cassandra', 'mongodb',
            
            # Database engines
            'mysql', 'postgresql', 'postgres', 'mariadb', 'oracle', 'sql server',
            'sqlite', 'redis', 'graph database',
            
            # Database functionality
            'database', ' db ', 'backup', 'snapshot', 'restore', 'migration',
            'performance insights', 'query performance', 'indexing', 'clustering',
            'replication', 'read replica', 'failover', 'high availability',
            'encryption at rest', 'encryption in transit', 'database security',
            
            # Data-related
            'data warehouse', 'analytics', 'olap', 'oltp', 'data lake',
            'streaming data', 'real-time data', 'batch processing',
            'etl', 'data pipeline', 'data integration'
        ])
        
        # Service mapping
        self.service_map = {
            'rds': 'Amazon RDS',
            'aurora': 'Amazon Aurora', 
            'dynamodb': 'Amazon DynamoDB',
            'redshift': 'Amazon Redshift',
            'neptune': 'Amazon Neptune',
            'timestream': 'Amazon Timestream',
            'documentdb': 'Amazon DocumentDB',
            'elasticache': 'Amazon ElastiCache',
            'memorydb': 'Amazon MemoryDB',
            'keyspaces': 'Amazon Keyspaces',
            'qldb': 'Amazon QLDB'
        }
    
    def load_config(self, config_file):
        """Load configuration from file"""
        config = {
            'keywords': {},
            'notification': {'enabled': False},
            'output': {'directory': '.', 'log_file': 'aws_db_monitor.log'}
        }
        
        if config_file and os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                config.update(user_config)
            except ImportError:
                print("Warning: PyYAML not installed, using default configuration")
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
        return config
    
    def fetch_rss_feed(self):
        """Fetch RSS feed content"""
        try:
            response = requests.get(self.rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return feedparser.parse(response.content)
        except Exception as e:
            print(f"Error fetching RSS feed: {e}")
            return None
    
    def is_database_related(self, title, description=""):
        """Check if announcement is database-related"""
        text = (title + " " + description).lower()
        return any(keyword.lower() in text for keyword in self.db_keywords)
    
    def identify_service(self, title, description):
        """Identify AWS database service"""
        text = (title + " " + description).lower()
        
        for keyword, service in self.service_map.items():
            if keyword in text:
                return service
        
        # Generic identification
        if any(word in text for word in ['database', ' db ', 'mysql', 'postgresql']):
            return "AWS Database Service"
        
        return "AWS Data Service"
    
    def categorize_feature(self, title, description):
        """Categorize feature type"""
        text = (title + " " + description).lower()
        
        categories = []
        
        if any(word in text for word in ['performance', 'optimization', 'faster', 'speed', 'latency']):
            categories.append("Performance Optimization")
        
        if any(word in text for word in ['backup', 'snapshot', 'restore', 'recovery', 'disaster']):
            categories.append("Backup & Recovery")
        
        if any(word in text for word in ['security', 'encryption', 'auth', 'iam', 'access']):
            categories.append("Security")
        
        if any(word in text for word in ['monitoring', 'insights', 'metrics', 'logging', 'observability']):
            categories.append("Monitoring & Analytics")
        
        if any(word in text for word in ['region', 'availability', 'zone', 'regional']):
            categories.append("Regional Expansion")
        
        if any(word in text for word in ['version', 'engine', 'upgrade', 'update']):
            categories.append("Version Update")
        
        if any(word in text for word in ['migration', 'import', 'export', 'transfer']):
            categories.append("Data Migration")
        
        if any(word in text for word in ['scaling', 'auto-scaling', 'elastic', 'capacity']):
            categories.append("Auto Scaling")
        
        return categories if categories else ["New Feature"]
    
    def extract_use_cases(self, title, description):
        """Extract potential use cases"""
        text = (title + " " + description).lower()
        
        use_cases = []
        
        if any(word in text for word in ['analytics', 'warehouse', 'olap', 'business intelligence']):
            use_cases.append("Data Analytics & BI")
        
        if any(word in text for word in ['real-time', 'streaming', 'live data']):
            use_cases.append("Real-time Data Processing")
        
        if any(word in text for word in ['web', 'application', 'app', 'online']):
            use_cases.append("Web Applications")
        
        if any(word in text for word in ['enterprise', 'mission-critical', 'production']):
            use_cases.append("Enterprise Applications")
        
        if any(word in text for word in ['iot', 'sensor', 'telemetry', 'device']):
            use_cases.append("IoT & Sensor Data")
        
        if any(word in text for word in ['gaming', 'game', 'multiplayer']):
            use_cases.append("Gaming Applications")
        
        if any(word in text for word in ['financial', 'fintech', 'banking']):
            use_cases.append("Financial Services")
        
        if any(word in text for word in ['compliance', 'audit', 'regulation']):
            use_cases.append("Compliance & Audit")
        
        return use_cases if use_cases else ["General Database Applications"]
    
    def extract_advantages(self, title, description):
        """Extract key advantages"""
        text = (title + " " + description).lower()
        
        advantages = []
        
        if any(word in text for word in ['faster', 'performance', 'speed', 'efficiency']):
            advantages.append("Improved Performance")
        
        if any(word in text for word in ['cost', 'cheaper', 'reduce', 'saving', 'affordable']):
            advantages.append("Cost Reduction")
        
        if any(word in text for word in ['simple', 'easy', 'automated', 'streamline']):
            advantages.append("Simplified Operations")
        
        if any(word in text for word in ['secure', 'security', 'protection', 'encrypted']):
            advantages.append("Enhanced Security")
        
        if any(word in text for word in ['scalable', 'elastic', 'flexible', 'adaptive']):
            advantages.append("Better Scalability")
        
        if any(word in text for word in ['available', 'reliability', 'uptime', 'resilient']):
            advantages.append("Higher Availability")
        
        if any(word in text for word in ['global', 'worldwide', 'multi-region']):
            advantages.append("Global Deployment")
        
        return advantages if advantages else ["Feature Enhancement"]
    
    def extract_usage_guide(self, title, description):
        """Extract usage guidance"""
        text = (title + " " + description).lower()
        
        guide_points = []
        
        if 'console' in text:
            guide_points.append("AWS Management Console")
        
        if any(word in text for word in ['cli', 'command line', 'api']):
            guide_points.append("CLI & API Support")
        
        if 'terraform' in text or 'cloudformation' in text:
            guide_points.append("Infrastructure as Code")
        
        if any(word in text for word in ['sdk', 'library', 'integration']):
            guide_points.append("SDK Integration")
        
        if 'documentation' in text:
            guide_points.append("Official Documentation")
        
        return guide_points if guide_points else ["See AWS Documentation"]
    
    def analyze_features(self, limit=None):
        """Analyze database features from RSS feed"""
        print("🔄 Fetching AWS RSS feed...")
        
        feed = self.fetch_rss_feed()
        if not feed or not hasattr(feed, 'entries'):
            return {"error": "Unable to fetch RSS feed"}
        
        print(f"📊 RSS feed contains {len(feed.entries)} announcements")
        
        db_features = []
        total_count = 0
        
        entries = feed.entries[:limit] if limit else feed.entries
        
        for entry in entries:
            total_count += 1
            
            title = entry.get('title', '')
            description = entry.get('description', '')
            link = entry.get('link', '')
            pub_date = entry.get('published', '')
            
            if self.is_database_related(title, description):
                print(f"🗄️ Found database-related: {title}")
                
                # Analyze feature
                service = self.identify_service(title, description)
                categories = self.categorize_feature(title, description)
                use_cases = self.extract_use_cases(title, description)
                advantages = self.extract_advantages(title, description)
                usage_guide = self.extract_usage_guide(title, description)
                
                # Clean HTML tags
                clean_description = re.sub(r'<[^>]+>', '', description)
                clean_description = re.sub(r'&[^;]+;', '', clean_description)
                
                db_features.append({
                    'title': title,
                    'service': service,
                    'categories': categories,
                    'description': clean_description[:500] + "..." if len(clean_description) > 500 else clean_description,
                    'use_cases': use_cases,
                    'advantages': advantages,
                    'usage_guide': usage_guide,
                    'link': link,
                    'published_date': pub_date
                })
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_announcements': total_count,
            'database_features': db_features,
            'count': len(db_features)
        }
    
    def format_report(self, result, output_format='text'):
        """Format analysis results"""
        if 'error' in result:
            return f"❌ Error: {result['error']}"
        
        if output_format == 'json':
            return json.dumps(result, indent=2, ensure_ascii=False)
        
        # Text format
        report = []
        report.append("📰 AWS Database Features Report")
        report.append("=" * 50)
        report.append(f"📅 Date: {result['date']}")
        report.append(f"📊 Total AWS Announcements: {result['total_announcements']}")
        report.append(f"🗄️ Database-Related: {result['count']}")
        report.append("")
        
        if result['count'] == 0:
            report.append("ℹ️ No database-related features found today")
        else:
            for i, feature in enumerate(result['database_features'], 1):
                report.append(f"## {i}. {feature['service']}")
                report.append(f"**{feature['title']}**")
                report.append("")
                report.append(f"🏷️ **Categories**: {', '.join(feature['categories'])}")
                report.append(f"💡 **Use Cases**: {', '.join(feature['use_cases'])}")
                report.append(f"⚡ **Advantages**: {', '.join(feature['advantages'])}")
                report.append(f"🔧 **Usage**: {'; '.join(feature['usage_guide'])}")
                report.append("")
                report.append(f"📝 **Description**: {feature['description']}")
                report.append("")
                report.append(f"🔗 **Details**: {feature['link']}")
                report.append(f"📅 **Published**: {feature['published_date']}")
                report.append("")
                report.append("-" * 60)
                report.append("")
        
        return "\n".join(report)
    
    def save_results(self, result, output_dir="."):
        """Save results to files"""
        date_str = result.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Save JSON
        json_file = Path(output_dir) / f"aws_db_features_{date_str}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # Save report
        report_file = Path(output_dir) / f"aws_db_report_{date_str}.md"
        report = self.format_report(result, 'text')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(json_file), str(report_file)

def main():
    parser = argparse.ArgumentParser(description='Monitor AWS database service announcements')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--output-dir', default='.',
                       help='Output directory (default: current)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of announcements to process')
    parser.add_argument('--save', action='store_true',
                       help='Save results to files')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug output')
    
    args = parser.parse_args()
    
    try:
        monitor = AWSDBNewsMonitor(args.config)
        result = monitor.analyze_features(args.limit)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        # Output results
        report = monitor.format_report(result, args.output_format)
        print(report)
        
        # Save to files if requested
        if args.save:
            json_file, report_file = monitor.save_results(result, args.output_dir)
            print(f"\n✅ Results saved:")
            print(f"   📄 JSON: {json_file}")
            print(f"   📋 Report: {report_file}")
        
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()