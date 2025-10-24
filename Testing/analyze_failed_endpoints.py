#!/usr/bin/env python3
"""
Analyze Failed Endpoints
Analyze the failed MCP tools to identify correct API endpoints
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def analyze_failed_endpoints():
    """Analyze failed endpoints to identify correct API paths"""
    
    print("🔍 Analyzing Failed MCP Tools Endpoints")
    print("=" * 60)
    
    # Failed tools from the test results
    failed_tools = {
        "topic_management": [
            "get_topic_description",
            "get_topic_info", 
            "get_topic_partitions",
            "get_topic_partition_infos",
            "get_topic_configs",
            "get_all_topic_configs",
            "get_default_topic_configs"
        ],
        "consumer_groups": [
            "get_consumer_groups",
            "get_consumer_group",
            "get_consumer_group_offsets", 
            "get_consumer_group_details",
            "get_consumer_group_members",
            "get_consumer_group_summary"
        ],
        "alert_management": [
            "get_all_alert_policies",
            "get_alert_policy",
            "get_alert_notifications",
            "get_alert_history",
            "get_alert_summary"
        ],
        "metrics": [
            "get_cluster_metrics",
            "get_broker_metrics_summary",
            "get_topic_metrics",
            "get_consumer_group_metrics",
            "get_producer_metrics",
            "get_consumer_metrics"
        ],
        "topic_data_sampling": [
            "get_topic_offsets",
            "get_topic_content",
            "get_topic_messages",
            "get_topic_sample",
            "get_topic_latest_messages"
        ],
        "kafka_connect": [
            "get_connectors",
            "get_connector",
            "get_connector_status",
            "get_connector_tasks",
            "get_connector_plugins",
            "get_connector_configs"
        ],
        "health_monitoring": [
            "get_cluster_health",
            "get_broker_health",
            "get_topic_health",
            "get_consumer_group_health",
            "get_system_health"
        ],
        "advanced_features": [
            "get_topic_schema",
            "get_topic_metadata",
            "get_topic_statistics",
            "get_broker_statistics",
            "get_cluster_statistics"
        ],
        "configuration": [
            "get_cluster_configs",
            "get_broker_configs",
            "get_topic_config_details",
            "get_consumer_group_configs",
            "get_connector_configs"
        ]
    }
    
    print("📊 Failed Tools by Category:")
    print("=" * 40)
    
    total_failed = 0
    for category, tools in failed_tools.items():
        count = len(tools)
        total_failed += count
        print(f"{category.replace('_', ' ').title()}: {count} tools")
        for tool in tools:
            print(f"  • {tool}")
        print()
    
    print(f"Total Failed Tools: {total_failed}")
    print()
    
    # Analyze error patterns
    print("🔍 Error Pattern Analysis:")
    print("=" * 40)
    
    error_patterns = {
        "HTTP 404 - configs/topics": [
            "get_topic_description",
            "get_topic_info",
            "get_topic_partitions", 
            "get_topic_partition_infos",
            "get_topic_configs",
            "get_all_topic_configs"
        ],
        "HTTP 404 - configs/default/topics": [
            "get_default_topic_configs"
        ],
        "HTTP 404 - consumerGroupRelatedDetails/consumerGroups": [
            "get_consumer_groups"
        ],
        "Missing Method Implementation": [
            "get_consumer_group",
            "get_consumer_group_offsets",
            "get_consumer_group_details",
            "get_consumer_group_members",
            "get_consumer_group_summary",
            "get_cluster_metrics",
            "get_broker_metrics_summary",
            "get_consumer_metrics",
            "get_alert_history",
            "get_alert_summary",
            "get_topic_messages",
            "get_topic_sample",
            "get_topic_latest_messages",
            "get_cluster_configs",
            "get_broker_configs",
            "get_topic_config_details",
            "get_consumer_group_configs",
            "get_connector_configs",
            "get_connector_status",
            "get_connector_tasks",
            "get_connector_plugins",
            "get_cluster_health",
            "get_broker_health",
            "get_topic_health",
            "get_consumer_group_health",
            "get_system_health",
            "get_topic_schema",
            "get_topic_metadata",
            "get_topic_statistics",
            "get_broker_statistics",
            "get_cluster_statistics"
        ],
        "Missing Required Parameters": [
            "get_producer_metrics",
            "get_topic_content"
        ]
    }
    
    for pattern, tools in error_patterns.items():
        print(f"{pattern}: {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5
            print(f"  • {tool}")
        if len(tools) > 5:
            print(f"  ... and {len(tools) - 5} more")
        print()
    
    return failed_tools, error_patterns

def suggest_api_endpoints():
    """Suggest correct API endpoints based on SMM API patterns"""
    
    print("💡 Suggested API Endpoints:")
    print("=" * 40)
    
    suggestions = {
        "topic_management": {
            "get_topic_description": "/api/v1/admin/topics/{topic_name}",
            "get_topic_info": "/api/v1/admin/topics/{topic_name}",
            "get_topic_partitions": "/api/v1/admin/topics/{topic_name}/partitions",
            "get_topic_partition_infos": "/api/v1/admin/topics/{topic_name}/partitions",
            "get_topic_configs": "/api/v1/admin/topics/{topic_name}/configs",
            "get_all_topic_configs": "/api/v1/admin/topics/configs",
            "get_default_topic_configs": "/api/v1/admin/configs/default/topics"
        },
        "consumer_groups": {
            "get_consumer_groups": "/api/v1/admin/consumers",
            "get_consumer_group": "/api/v1/admin/consumers/{group_id}",
            "get_consumer_group_offsets": "/api/v1/admin/consumers/{group_id}/offsets",
            "get_consumer_group_details": "/api/v1/admin/consumers/{group_id}",
            "get_consumer_group_members": "/api/v1/admin/consumers/{group_id}/members",
            "get_consumer_group_summary": "/api/v1/admin/consumers/{group_id}/summary"
        },
        "alert_management": {
            "get_all_alert_policies": "/api/v1/admin/alerts/policies",
            "get_alert_policy": "/api/v1/admin/alerts/policies/{policy_id}",
            "get_alert_notifications": "/api/v1/admin/alerts/notifications",
            "get_alert_history": "/api/v1/admin/alerts/history",
            "get_alert_summary": "/api/v1/admin/alerts/summary"
        },
        "metrics": {
            "get_cluster_metrics": "/api/v1/admin/metrics/cluster",
            "get_broker_metrics_summary": "/api/v1/admin/metrics/brokers/summary",
            "get_topic_metrics": "/api/v1/admin/metrics/topics/{topic_name}",
            "get_consumer_group_metrics": "/api/v1/admin/metrics/consumers/{group_id}",
            "get_producer_metrics": "/api/v1/admin/metrics/producers",
            "get_consumer_metrics": "/api/v1/admin/metrics/consumers"
        },
        "topic_data_sampling": {
            "get_topic_offsets": "/api/v1/admin/topics/{topic_name}/offsets",
            "get_topic_content": "/api/v1/admin/topics/{topic_name}/messages",
            "get_topic_messages": "/api/v1/admin/topics/{topic_name}/messages",
            "get_topic_sample": "/api/v1/admin/topics/{topic_name}/sample",
            "get_topic_latest_messages": "/api/v1/admin/topics/{topic_name}/messages/latest"
        },
        "kafka_connect": {
            "get_connectors": "/api/v1/admin/connectors",
            "get_connector": "/api/v1/admin/connectors/{connector_id}",
            "get_connector_status": "/api/v1/admin/connectors/{connector_id}/status",
            "get_connector_tasks": "/api/v1/admin/connectors/{connector_id}/tasks",
            "get_connector_plugins": "/api/v1/admin/connectors/plugins",
            "get_connector_configs": "/api/v1/admin/connectors/{connector_id}/configs"
        },
        "health_monitoring": {
            "get_cluster_health": "/api/v1/admin/health/cluster",
            "get_broker_health": "/api/v1/admin/health/brokers/{broker_id}",
            "get_topic_health": "/api/v1/admin/health/topics/{topic_name}",
            "get_consumer_group_health": "/api/v1/admin/health/consumers/{group_id}",
            "get_system_health": "/api/v1/admin/health/system"
        },
        "advanced_features": {
            "get_topic_schema": "/api/v1/admin/topics/{topic_name}/schema",
            "get_topic_metadata": "/api/v1/admin/topics/{topic_name}/metadata",
            "get_topic_statistics": "/api/v1/admin/topics/{topic_name}/statistics",
            "get_broker_statistics": "/api/v1/admin/brokers/{broker_id}/statistics",
            "get_cluster_statistics": "/api/v1/admin/cluster/statistics"
        },
        "configuration": {
            "get_cluster_configs": "/api/v1/admin/configs/cluster",
            "get_broker_configs": "/api/v1/admin/configs/brokers/{broker_id}",
            "get_topic_config_details": "/api/v1/admin/topics/{topic_name}/configs",
            "get_consumer_group_configs": "/api/v1/admin/consumers/{group_id}/configs",
            "get_connector_configs": "/api/v1/admin/connectors/{connector_id}/configs"
        }
    }
    
    for category, endpoints in suggestions.items():
        print(f"{category.replace('_', ' ').title()}:")
        for method, endpoint in endpoints.items():
            print(f"  {method}: {endpoint}")
        print()
    
    return suggestions

def main():
    """Main analysis function"""
    print("🧪 Failed MCP Tools Analysis")
    print("=" * 60)
    print("Analyzing failed endpoints to identify fixes needed")
    print()
    
    # Analyze failed tools
    failed_tools, error_patterns = analyze_failed_endpoints()
    
    # Suggest API endpoints
    suggestions = suggest_api_endpoints()
    
    print("📋 Summary:")
    print("=" * 20)
    print("1. Fix API endpoint paths for 404 errors")
    print("2. Implement missing method definitions")
    print("3. Add required parameters for method calls")
    print("4. Test each category individually")
    print("5. Validate with SMM API documentation")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
