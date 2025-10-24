#!/usr/bin/env python3
"""
Explore Alternative API Patterns
Test different endpoint structures to discover more working SMM APIs
"""

import os
import sys
import json
import requests
from pathlib import Path
from urllib.parse import urljoin

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def explore_alternative_apis():
    """Explore alternative API patterns to find more working endpoints"""
    
    print("🔍 Exploring Alternative API Patterns")
    print("=" * 60)
    
    try:
        from ssm_mcp_server.client import SMMClient
        from ssm_mcp_server.config import ServerConfig
        from ssm_mcp_server.auth import KnoxAuthFactory
        
        # Create configuration for cloud environment
        config = ServerConfig()
        config.knox_gateway_url = os.getenv("KNOX_GATEWAY_URL", "https://irb-kakfa-only-master0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-kakfa-only/cdp-proxy-api/smm-api")
        config.knox_user = os.getenv("KNOX_USER", "admin")
        config.knox_password = os.getenv("KNOX_PASSWORD", "admin")
        config.smm_readonly = True
        config.knox_verify_ssl = True
        
        print("✅ Cloud configuration created")
        print(f"   Gateway: {config.knox_gateway_url}")
        print(f"   User: {config.knox_user}")
        
        # Create auth factory and client
        auth_factory = KnoxAuthFactory(
            gateway_url=config.knox_gateway_url,
            token=None,
            cookie=None,
            user=config.knox_user,
            password=config.knox_password,
            token_endpoint=None,
            passcode_token=None,
            verify=config.knox_verify_ssl
        )
        
        session = auth_factory.build_session()
        client = SMMClient(
            base_url=config.build_smm_base(),
            session=session,
            timeout_seconds=30,
            proxy_context_path=config.proxy_context_path
        )
        
        print("✅ SMM client created for API exploration")
        print()
        
        # Test various API patterns
        api_patterns = [
            # Consumer Groups - Alternative patterns
            ("/api/v1/consumers", "Consumers v1"),
            ("/api/v1/consumer-groups", "Consumer Groups v1"),
            ("/api/v1/consumerGroups", "Consumer Groups Camel v1"),
            ("/api/v2/consumers", "Consumers v2"),
            ("/api/v2/consumer-groups", "Consumer Groups v2"),
            ("/api/v2/consumerGroups", "Consumer Groups Camel v2"),
            ("/consumers", "Consumers Root"),
            ("/consumer-groups", "Consumer Groups Root"),
            ("/consumerGroups", "Consumer Groups Camel Root"),
            ("/api/consumers", "Consumers API"),
            ("/api/consumer-groups", "Consumer Groups API"),
            ("/api/consumerGroups", "Consumer Groups Camel API"),
            
            # Metrics - Alternative patterns
            ("/api/v1/metrics", "Metrics v1"),
            ("/api/v1/metrics/cluster", "Cluster Metrics v1"),
            ("/api/v1/metrics/brokers", "Broker Metrics v1"),
            ("/api/v1/metrics/topics", "Topic Metrics v1"),
            ("/api/v1/metrics/consumers", "Consumer Metrics v1"),
            ("/api/v2/metrics", "Metrics v2"),
            ("/api/v2/metrics/cluster", "Cluster Metrics v2"),
            ("/api/v2/metrics/brokers", "Broker Metrics v2"),
            ("/api/v2/metrics/topics", "Topic Metrics v2"),
            ("/metrics", "Metrics Root"),
            ("/api/metrics", "Metrics API"),
            ("/api/metrics/cluster", "Cluster Metrics API"),
            ("/api/metrics/brokers", "Broker Metrics API"),
            ("/api/metrics/topics", "Topic Metrics API"),
            
            # Alerts - Alternative patterns
            ("/api/v1/alerts", "Alerts v1"),
            ("/api/v1/alerts/policies", "Alert Policies v1"),
            ("/api/v1/alerts/notifications", "Alert Notifications v1"),
            ("/api/v1/alerts/history", "Alert History v1"),
            ("/api/v2/alerts", "Alerts v2"),
            ("/api/v2/alerts/policies", "Alert Policies v2"),
            ("/api/v2/alerts/notifications", "Alert Notifications v2"),
            ("/alerts", "Alerts Root"),
            ("/api/alerts", "Alerts API"),
            ("/api/alerts/policies", "Alert Policies API"),
            ("/api/alerts/notifications", "Alert Notifications API"),
            
            # Health - Alternative patterns
            ("/api/v1/health", "Health v1"),
            ("/api/v1/health/cluster", "Cluster Health v1"),
            ("/api/v1/health/brokers", "Broker Health v1"),
            ("/api/v1/health/topics", "Topic Health v1"),
            ("/api/v2/health", "Health v2"),
            ("/api/v2/health/cluster", "Cluster Health v2"),
            ("/api/v2/health/brokers", "Broker Health v2"),
            ("/health", "Health Root"),
            ("/api/health", "Health API"),
            ("/api/health/cluster", "Cluster Health API"),
            ("/api/health/brokers", "Broker Health API"),
            
            # Connectors - Alternative patterns
            ("/api/v1/connectors", "Connectors v1"),
            ("/api/v1/kafka-connect", "Kafka Connect v1"),
            ("/api/v1/connect", "Connect v1"),
            ("/api/v2/connectors", "Connectors v2"),
            ("/api/v2/kafka-connect", "Kafka Connect v2"),
            ("/api/v2/connect", "Connect v2"),
            ("/connectors", "Connectors Root"),
            ("/kafka-connect", "Kafka Connect Root"),
            ("/connect", "Connect Root"),
            ("/api/connectors", "Connectors API"),
            ("/api/kafka-connect", "Kafka Connect API"),
            ("/api/connect", "Connect API"),
            
            # Topic Data - Alternative patterns
            ("/api/v1/topics/heartbeats/messages", "Topic Messages v1"),
            ("/api/v1/topics/heartbeats/offsets", "Topic Offsets v1"),
            ("/api/v1/topics/heartbeats/sample", "Topic Sample v1"),
            ("/api/v1/topics/heartbeats/content", "Topic Content v1"),
            ("/api/v2/topics/heartbeats/messages", "Topic Messages v2"),
            ("/api/v2/topics/heartbeats/offsets", "Topic Offsets v2"),
            ("/api/v2/topics/heartbeats/sample", "Topic Sample v2"),
            ("/topics/heartbeats/messages", "Topic Messages Root"),
            ("/topics/heartbeats/offsets", "Topic Offsets Root"),
            ("/topics/heartbeats/sample", "Topic Sample Root"),
            ("/api/topics/heartbeats/messages", "Topic Messages API"),
            ("/api/topics/heartbeats/offsets", "Topic Offsets API"),
            ("/api/topics/heartbeats/sample", "Topic Sample API"),
            
            # Configuration - Alternative patterns
            ("/api/v1/configs", "Configs v1"),
            ("/api/v1/configs/cluster", "Cluster Configs v1"),
            ("/api/v1/configs/brokers", "Broker Configs v1"),
            ("/api/v1/configs/topics", "Topic Configs v1"),
            ("/api/v2/configs", "Configs v2"),
            ("/api/v2/configs/cluster", "Cluster Configs v2"),
            ("/api/v2/configs/brokers", "Broker Configs v2"),
            ("/configs", "Configs Root"),
            ("/api/configs", "Configs API"),
            ("/api/configs/cluster", "Cluster Configs API"),
            ("/api/configs/brokers", "Broker Configs API"),
            
            # Statistics - Alternative patterns
            ("/api/v1/statistics", "Statistics v1"),
            ("/api/v1/statistics/cluster", "Cluster Statistics v1"),
            ("/api/v1/statistics/brokers", "Broker Statistics v1"),
            ("/api/v1/statistics/topics", "Topic Statistics v1"),
            ("/api/v2/statistics", "Statistics v2"),
            ("/api/v2/statistics/cluster", "Cluster Statistics v2"),
            ("/api/v2/statistics/brokers", "Broker Statistics v2"),
            ("/statistics", "Statistics Root"),
            ("/api/statistics", "Statistics API"),
            ("/api/statistics/cluster", "Cluster Statistics API"),
            ("/api/statistics/brokers", "Broker Statistics API"),
            
            # Schema Registry - Alternative patterns
            ("/api/v1/schemas", "Schemas v1"),
            ("/api/v1/schema-registry", "Schema Registry v1"),
            ("/api/v1/schema", "Schema v1"),
            ("/api/v2/schemas", "Schemas v2"),
            ("/api/v2/schema-registry", "Schema Registry v2"),
            ("/schemas", "Schemas Root"),
            ("/schema-registry", "Schema Registry Root"),
            ("/schema", "Schema Root"),
            ("/api/schemas", "Schemas API"),
            ("/api/schema-registry", "Schema Registry API"),
            
            # Admin - Alternative patterns
            ("/api/v1/admin", "Admin v1"),
            ("/api/v1/admin/cluster", "Admin Cluster v1"),
            ("/api/v1/admin/brokers", "Admin Brokers v1"),
            ("/api/v1/admin/topics", "Admin Topics v1"),
            ("/api/v2/admin", "Admin v2"),
            ("/api/v2/admin/cluster", "Admin Cluster v2"),
            ("/api/v2/admin/brokers", "Admin Brokers v2"),
            ("/admin", "Admin Root"),
            ("/api/admin", "Admin API"),
            ("/api/admin/cluster", "Admin Cluster API"),
            ("/api/admin/brokers", "Admin Brokers API"),
        ]
        
        print("🔍 Testing Alternative API Patterns:")
        print("=" * 50)
        
        working_endpoints = []
        failed_endpoints = []
        
        for endpoint, description in api_patterns:
            try:
                print(f"Testing {description} ({endpoint})...", end=" ")
                
                # Test the endpoint
                response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ WORKING")
                    working_endpoints.append((endpoint, description, response.status_code))
                    
                    # Try to get some sample data
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            keys = list(data.keys())[:5]  # First 5 keys
                            print(f"   Sample keys: {keys}")
                        elif isinstance(data, list):
                            print(f"   Array with {len(data)} items")
                    except:
                        print(f"   Response is not JSON")
                        
                elif response.status_code == 404:
                    print("❌ 404 Not Found")
                    failed_endpoints.append((endpoint, description, response.status_code))
                else:
                    print(f"⚠️  {response.status_code}")
                    if response.status_code not in [401, 403, 500]:
                        working_endpoints.append((endpoint, description, response.status_code))
                    else:
                        failed_endpoints.append((endpoint, description, response.status_code))
                        
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
                failed_endpoints.append((endpoint, description, f"Error: {str(e)[:50]}"))
        
        print()
        print("📊 Alternative API Pattern Results:")
        print("=" * 50)
        
        print(f"✅ Working Endpoints ({len(working_endpoints)}):")
        for endpoint, description, status in working_endpoints:
            print(f"   {status} - {description}: {endpoint}")
        
        print(f"\n❌ Failed Endpoints ({len(failed_endpoints)}):")
        for endpoint, description, status in failed_endpoints[:10]:  # Show first 10
            print(f"   {status} - {description}: {endpoint}")
        if len(failed_endpoints) > 10:
            print(f"   ... and {len(failed_endpoints) - 10} more failed endpoints")
        
        # Test some specific patterns that might work
        print(f"\n🔍 Testing Specific SMM Patterns:")
        print("=" * 40)
        
        specific_patterns = [
            # Try different base paths
            ("/smm/api/v1/consumers", "SMM Consumers"),
            ("/smm/api/v1/metrics", "SMM Metrics"),
            ("/smm/api/v1/alerts", "SMM Alerts"),
            ("/smm/api/v1/health", "SMM Health"),
            ("/smm/api/v1/connectors", "SMM Connectors"),
            
            # Try different API versions
            ("/api/v3/consumers", "Consumers v3"),
            ("/api/v3/metrics", "Metrics v3"),
            ("/api/v3/alerts", "Alerts v3"),
            ("/api/v3/health", "Health v3"),
            
            # Try different service names
            ("/api/v1/streams", "Streams API"),
            ("/api/v1/messaging", "Messaging API"),
            ("/api/v1/kafka", "Kafka API"),
            ("/api/v1/monitoring", "Monitoring API"),
        ]
        
        for endpoint, description in specific_patterns:
            try:
                print(f"Testing {description} ({endpoint})...", end=" ")
                response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ WORKING")
                    working_endpoints.append((endpoint, description, response.status_code))
                else:
                    print(f"❌ {response.status_code}")
                    failed_endpoints.append((endpoint, description, response.status_code))
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
                failed_endpoints.append((endpoint, description, f"Error: {str(e)[:50]}"))
        
        return working_endpoints, failed_endpoints
        
    except Exception as e:
        print(f"❌ API exploration failed: {e}")
        return [], []

def main():
    """Main exploration function"""
    print("🧪 Alternative API Patterns Exploration")
    print("=" * 60)
    print("Testing different endpoint structures to find more working APIs")
    print()
    
    working, failed = explore_alternative_apis()
    
    print(f"\n📋 Summary:")
    print("=" * 20)
    print(f"Working Endpoints: {len(working)}")
    print(f"Failed Endpoints: {len(failed)}")
    
    if working:
        print(f"\n🎉 Found {len(working)} additional working endpoints!")
        print("These can be used to update the SMMClient methods.")
        
        # Group by category
        categories = {}
        for endpoint, description, status in working:
            category = description.split()[0]  # First word is usually the category
            if category not in categories:
                categories[category] = []
            categories[category].append((endpoint, description, status))
        
        print(f"\n📊 Working Endpoints by Category:")
        for category, endpoints in categories.items():
            print(f"   {category}: {len(endpoints)} endpoints")
            for endpoint, description, status in endpoints:
                print(f"     - {description}: {endpoint}")
    else:
        print(f"\n⚠️  No additional working endpoints found.")
        print("The SMM instance may have limited API functionality.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
