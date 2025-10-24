#!/usr/bin/env python3
"""
Discover Real SMM API Endpoints
Use the working Swagger discovery to find actual API endpoints
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def discover_real_endpoints():
    """Discover real SMM API endpoints using Swagger analysis"""
    
    print("🔍 Discovering Real SMM API Endpoints")
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
        
        print("✅ SMM client created for endpoint discovery")
        print()
        
        # Test various endpoint patterns
        endpoint_tests = [
            # Consumer Groups
            ("/api/v1/admin/consumers", "Consumer Groups"),
            ("/api/v1/admin/consumer-groups", "Consumer Groups Alt"),
            ("/api/v1/admin/consumerGroups", "Consumer Groups Camel"),
            ("/api/v1/consumers", "Consumers Short"),
            ("/api/v1/consumer-groups", "Consumer Groups Short"),
            
            # Metrics
            ("/api/v1/admin/metrics", "Metrics Root"),
            ("/api/v1/admin/metrics/cluster", "Cluster Metrics"),
            ("/api/v1/admin/metrics/brokers", "Broker Metrics"),
            ("/api/v1/admin/metrics/topics", "Topic Metrics"),
            ("/api/v1/metrics", "Metrics Short"),
            ("/api/v1/metrics/cluster", "Cluster Metrics Short"),
            
            # Alerts
            ("/api/v1/admin/alerts", "Alerts Root"),
            ("/api/v1/admin/alerts/policies", "Alert Policies"),
            ("/api/v1/admin/alerts/notifications", "Alert Notifications"),
            ("/api/v1/alerts", "Alerts Short"),
            
            # Health
            ("/api/v1/admin/health", "Health Root"),
            ("/api/v1/admin/health/cluster", "Cluster Health"),
            ("/api/v1/admin/health/brokers", "Broker Health"),
            ("/api/v1/health", "Health Short"),
            
            # Connectors
            ("/api/v1/admin/connectors", "Connectors"),
            ("/api/v1/admin/kafka-connect", "Kafka Connect"),
            ("/api/v1/connectors", "Connectors Short"),
            ("/api/v1/kafka-connect", "Kafka Connect Short"),
            
            # Topic Data
            ("/api/v1/admin/topics/heartbeats/messages", "Topic Messages"),
            ("/api/v1/admin/topics/heartbeats/offsets", "Topic Offsets"),
            ("/api/v1/admin/topics/heartbeats/sample", "Topic Sample"),
            
            # Advanced Features
            ("/api/v1/admin/topics/heartbeats/schema", "Topic Schema"),
            ("/api/v1/admin/topics/heartbeats/metadata", "Topic Metadata"),
            ("/api/v1/admin/topics/heartbeats/statistics", "Topic Statistics"),
            
            # Configuration
            ("/api/v1/admin/configs", "Configs Root"),
            ("/api/v1/admin/configs/cluster", "Cluster Configs"),
            ("/api/v1/admin/configs/brokers", "Broker Configs"),
            ("/api/v1/configs", "Configs Short"),
        ]
        
        print("🔍 Testing API Endpoints:")
        print("=" * 40)
        
        working_endpoints = []
        failed_endpoints = []
        
        for endpoint, description in endpoint_tests:
            try:
                print(f"Testing {description} ({endpoint})...", end=" ")
                
                # Test the endpoint
                response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ WORKING")
                    working_endpoints.append((endpoint, description, response.status_code))
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
        print("📊 Endpoint Discovery Results:")
        print("=" * 40)
        
        print(f"✅ Working Endpoints ({len(working_endpoints)}):")
        for endpoint, description, status in working_endpoints:
            print(f"   {status} - {description}: {endpoint}")
        
        print(f"\n❌ Failed Endpoints ({len(failed_endpoints)}):")
        for endpoint, description, status in failed_endpoints[:10]:  # Show first 10
            print(f"   {status} - {description}: {endpoint}")
        if len(failed_endpoints) > 10:
            print(f"   ... and {len(failed_endpoints) - 10} more failed endpoints")
        
        # Try to get Swagger documentation
        print(f"\n🔍 Looking for Swagger Documentation:")
        print("=" * 40)
        
        swagger_endpoints = [
            "/swagger",
            "/swagger.json",
            "/api-docs",
            "/api-docs/swagger.json",
            "/api/v1/swagger",
            "/api/v1/swagger.json",
            "/docs",
            "/api-docs.json"
        ]
        
        swagger_found = False
        for swagger_endpoint in swagger_endpoints:
            try:
                print(f"Testing {swagger_endpoint}...", end=" ")
                response = session.get(f"{config.build_smm_base()}{swagger_endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ FOUND")
                    swagger_found = True
                    
                    # Try to parse as JSON
                    try:
                        swagger_data = response.json()
                        print(f"   Swagger JSON found with {len(swagger_data.get('paths', {}))} paths")
                        
                        # Extract some key paths
                        paths = swagger_data.get('paths', {})
                        print(f"   Sample paths:")
                        for i, path in enumerate(list(paths.keys())[:10]):
                            print(f"     {path}")
                        if len(paths) > 10:
                            print(f"     ... and {len(paths) - 10} more paths")
                            
                    except json.JSONDecodeError:
                        print(f"   Response is not JSON (likely HTML)")
                        
                    break
                else:
                    print(f"❌ {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
        
        if not swagger_found:
            print("❌ No Swagger documentation found")
        
        return working_endpoints, failed_endpoints
        
    except Exception as e:
        print(f"❌ Endpoint discovery failed: {e}")
        return [], []

def main():
    """Main discovery function"""
    print("🧪 Real SMM API Endpoints Discovery")
    print("=" * 60)
    print("Discovering actual working API endpoints")
    print()
    
    working, failed = discover_real_endpoints()
    
    print(f"\n📋 Summary:")
    print("=" * 20)
    print(f"Working Endpoints: {len(working)}")
    print(f"Failed Endpoints: {len(failed)}")
    
    if working:
        print(f"\n🎉 Found {len(working)} working endpoints!")
        print("These can be used to update the SMMClient methods.")
    else:
        print(f"\n⚠️  No working endpoints found beyond the basic ones.")
        print("The SMM instance may have limited API functionality.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
