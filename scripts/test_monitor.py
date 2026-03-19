#!/usr/bin/env python3
"""
Test script for AWS Database News Monitor
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from monitor import AWSDBNewsMonitor

def test_basic_functionality():
    """Test basic monitoring functionality"""
    print("🧪 Testing AWS Database News Monitor...")
    
    monitor = AWSDBNewsMonitor()
    
    # Test RSS feed fetch
    print("📡 Testing RSS feed access...")
    feed = monitor.fetch_rss_feed()
    if not feed:
        print("❌ Failed to fetch RSS feed")
        return False
    
    print(f"✅ RSS feed contains {len(feed.entries)} entries")
    
    # Test analysis with limited entries
    print("🔍 Testing feature analysis...")
    result = monitor.analyze_features(limit=20)
    
    if 'error' in result:
        print(f"❌ Analysis failed: {result['error']}")
        return False
    
    print(f"✅ Analysis completed:")
    print(f"   📊 Processed: {result['total_announcements']} announcements")
    print(f"   🗄️ Database-related: {result['count']}")
    
    # Test report formatting
    print("📝 Testing report generation...")
    report = monitor.format_report(result, 'text')
    json_report = monitor.format_report(result, 'json')
    
    if len(report) > 0 and len(json_report) > 0:
        print("✅ Report generation successful")
    else:
        print("❌ Report generation failed")
        return False
    
    return True

def test_keyword_matching():
    """Test keyword matching functionality"""
    print("🔍 Testing keyword matching...")
    
    monitor = AWSDBNewsMonitor()
    
    # Test cases
    test_cases = [
        ("Amazon RDS for MySQL now supports new feature", True),
        ("Amazon Aurora performance improvements", True),
        ("Amazon DynamoDB global tables", True),
        ("Amazon EC2 instances now available", False),
        ("AWS Lambda function updates", False),
        ("Database backup and restore capabilities", True),
        ("Performance Insights for PostgreSQL", True),
    ]
    
    passed = 0
    for text, expected in test_cases:
        result = monitor.is_database_related(text)
        if result == expected:
            print(f"✅ '{text[:40]}...' -> {result}")
            passed += 1
        else:
            print(f"❌ '{text[:40]}...' -> {result} (expected {expected})")
    
    print(f"📊 Keyword matching: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)

def test_service_identification():
    """Test service identification"""
    print("🏷️ Testing service identification...")
    
    monitor = AWSDBNewsMonitor()
    
    test_cases = [
        ("Amazon RDS MySQL engine update", "Amazon RDS"),
        ("Aurora PostgreSQL performance", "Amazon Aurora"),
        ("DynamoDB global secondary indexes", "Amazon DynamoDB"),
        ("Redshift data warehouse features", "Amazon Redshift"),
        ("Neptune graph database", "Amazon Neptune"),
    ]
    
    passed = 0
    for text, expected in test_cases:
        result = monitor.identify_service(text, "")
        if result == expected:
            print(f"✅ '{text}' -> {result}")
            passed += 1
        else:
            print(f"❌ '{text}' -> {result} (expected {expected})")
    
    print(f"📊 Service identification: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)

def main():
    """Run all tests"""
    print("🚀 Starting AWS Database News Monitor Tests")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Keyword Matching", test_keyword_matching),
        ("Service Identification", test_service_identification),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name} Test: PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} Test: FAILED")
        except Exception as e:
            print(f"❌ {test_name} Test: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The monitor is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())