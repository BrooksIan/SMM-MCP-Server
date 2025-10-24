#!/usr/bin/env python3
"""
Analyze Working Endpoints
Deep dive into the working endpoints to understand their structure and capabilities
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def analyze_working_endpoints():
    """Analyze the working endpoints to understand their structure"""
    
    print("🔍 Analyzing Working Endpoints")
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
        
        print("✅ SMM client created for endpoint analysis")
        print()
        
        # Analyze the working endpoints
        working_endpoints = [
            ("/api/v1/admin/cluster", "Admin Cluster"),
            ("/api/v1/admin/brokers", "Admin Brokers"),
            ("/api/v1/admin/topics", "Admin Topics"),
        ]
        
        print("🔍 Analyzing Working Endpoints:")
        print("=" * 50)
        
        for endpoint, description in working_endpoints:
            print(f"\n📊 Analyzing {description} ({endpoint})")
            print("-" * 40)
            
            try:
                response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Status: {response.status_code}")
                    print(f"📏 Content-Length: {len(response.content)} bytes")
                    print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    
                    try:
                        data = response.json()
                        print(f"📋 Data Type: {type(data).__name__}")
                        
                        if isinstance(data, dict):
                            print(f"🔑 Keys: {list(data.keys())}")
                            
                            # Analyze each key
                            for key, value in data.items():
                                if isinstance(value, list):
                                    print(f"   {key}: Array with {len(value)} items")
                                    if value and len(value) > 0:
                                        print(f"      Sample item keys: {list(value[0].keys()) if isinstance(value[0], dict) else 'Not a dict'}")
                                elif isinstance(value, dict):
                                    print(f"   {key}: Object with {len(value)} keys")
                                    print(f"      Keys: {list(value.keys())}")
                                else:
                                    print(f"   {key}: {type(value).__name__} = {str(value)[:100]}")
                        
                        elif isinstance(data, list):
                            print(f"📋 Array with {len(data)} items")
                            if data and len(data) > 0:
                                print(f"🔑 Sample item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                                
                                # Show sample items
                                for i, item in enumerate(data[:3]):  # First 3 items
                                    print(f"   Item {i+1}: {item}")
                        
                    except json.JSONDecodeError:
                        print("❌ Response is not valid JSON")
                        print(f"📄 Raw content (first 200 chars): {response.text[:200]}")
                
                else:
                    print(f"❌ Status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Test some variations of the working endpoints
        print(f"\n🔍 Testing Variations of Working Endpoints:")
        print("=" * 50)
        
        variations = [
            # Test with different parameters
            ("/api/v1/admin/cluster?format=json", "Admin Cluster with JSON format"),
            ("/api/v1/admin/cluster?pretty=true", "Admin Cluster with pretty print"),
            ("/api/v1/admin/brokers?format=json", "Admin Brokers with JSON format"),
            ("/api/v1/admin/brokers?pretty=true", "Admin Brokers with pretty print"),
            ("/api/v1/admin/topics?format=json", "Admin Topics with JSON format"),
            ("/api/v1/admin/topics?pretty=true", "Admin Topics with pretty print"),
            
            # Test with different HTTP methods
            ("/api/v1/admin/cluster", "Admin Cluster HEAD"),
            ("/api/v1/admin/brokers", "Admin Brokers HEAD"),
            ("/api/v1/admin/topics", "Admin Topics HEAD"),
        ]
        
        for endpoint, description in variations:
            try:
                print(f"Testing {description} ({endpoint})...", end=" ")
                
                if "HEAD" in description:
                    response = session.head(f"{config.build_smm_base()}{endpoint}", timeout=10)
                else:
                    response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ WORKING")
                else:
                    print(f"❌ {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
        
        # Test some additional patterns that might work
        print(f"\n🔍 Testing Additional Patterns:")
        print("=" * 40)
        
        additional_patterns = [
            # Test different admin endpoints
            ("/api/v1/admin", "Admin Root"),
            ("/api/v1/admin/", "Admin Root with slash"),
            ("/api/v1/admin/configs", "Admin Configs"),
            ("/api/v1/admin/metrics", "Admin Metrics"),
            ("/api/v1/admin/health", "Admin Health"),
            ("/api/v1/admin/alerts", "Admin Alerts"),
            ("/api/v1/admin/consumers", "Admin Consumers"),
            ("/api/v1/admin/connectors", "Admin Connectors"),
            
            # Test different topic-related endpoints
            ("/api/v1/admin/topics/heartbeats", "Admin Topic heartbeats"),
            ("/api/v1/admin/topics/heartbeats/configs", "Admin Topic heartbeats configs"),
            ("/api/v1/admin/topics/heartbeats/partitions", "Admin Topic heartbeats partitions"),
            ("/api/v1/admin/topics/heartbeats/offsets", "Admin Topic heartbeats offsets"),
            
            # Test different broker-related endpoints
            ("/api/v1/admin/brokers/0", "Admin Broker 0"),
            ("/api/v1/admin/brokers/1", "Admin Broker 1"),
            ("/api/v1/admin/brokers/2", "Admin Broker 2"),
            ("/api/v1/admin/brokers/0/configs", "Admin Broker 0 configs"),
            ("/api/v1/admin/brokers/0/metrics", "Admin Broker 0 metrics"),
        ]
        
        working_variations = []
        failed_variations = []
        
        for endpoint, description in additional_patterns:
            try:
                print(f"Testing {description} ({endpoint})...", end=" ")
                response = session.get(f"{config.build_smm_base()}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    print("✅ WORKING")
                    working_variations.append((endpoint, description, response.status_code))
                else:
                    print(f"❌ {response.status_code}")
                    failed_variations.append((endpoint, description, response.status_code))
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
                failed_variations.append((endpoint, description, f"Error: {str(e)[:50]}"))
        
        print(f"\n📊 Additional Pattern Results:")
        print("=" * 40)
        
        if working_variations:
            print(f"✅ Working Variations ({len(working_variations)}):")
            for endpoint, description, status in working_variations:
                print(f"   {status} - {description}: {endpoint}")
        else:
            print("❌ No additional working variations found")
        
        return working_variations, failed_variations
        
    except Exception as e:
        print(f"❌ Endpoint analysis failed: {e}")
        return [], []

def main():
    """Main analysis function"""
    print("🧪 Working Endpoints Analysis")
    print("=" * 60)
    print("Deep dive into working endpoints to understand their structure")
    print()
    
    working, failed = analyze_working_endpoints()
    
    print(f"\n📋 Summary:")
    print("=" * 20)
    print(f"Working Variations: {len(working)}")
    print(f"Failed Variations: {len(failed)}")
    
    if working:
        print(f"\n🎉 Found {len(working)} additional working variations!")
        print("These can be used to expand the SMMClient methods.")
    else:
        print(f"\n⚠️  No additional working variations found.")
        print("The working endpoints may have limited functionality.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
