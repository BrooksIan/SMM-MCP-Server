#!/usr/bin/env python3
"""
Test New Endpoints
Test the newly discovered working endpoints
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_new_endpoints():
    """Test the newly discovered working endpoints"""
    
    print("🧪 Testing New Endpoints")
    print("=" * 60)
    
    try:
        from ssm_mcp_server.client import SMMClient
        from ssm_mcp_server.config import ServerConfig
        from ssm_mcp_server.auth import KnoxAuthFactory
        
        # Create configuration for cloud environment
        config = ServerConfig()
        config.knox_gateway_url = "https://irb-kakfa-only-master0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-kakfa-only/cdp-proxy-api/smm-api"
        config.knox_user = "ibrooks"
        config.knox_password = "Admin12345#"
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
        
        print("✅ SMM client created for new endpoint testing")
        print()
        
        # Test the new endpoints
        new_endpoints = [
            ("get_admin_cluster", "Admin Cluster", []),
            ("get_admin_brokers", "Admin Brokers", []),
            ("get_admin_topics", "Admin Topics", []),
            ("get_admin_topic_details", "Admin Topic Details", ["heartbeats"]),
            ("get_admin_topic_partitions", "Admin Topic Partitions", ["heartbeats"]),
        ]
        
        print("🔍 Testing New Endpoints:")
        print("=" * 50)
        
        successful = 0
        failed = 0
        
        for method_name, description, params in new_endpoints:
            try:
                print(f"Testing {description}...", end=" ")
                
                # Get the method from the client
                method = getattr(client, method_name)
                
                # Call the method with parameters
                if params:
                    result = method(*params)
                else:
                    result = method()
                
                print("✅ SUCCESS")
                successful += 1
                
                # Show some sample data
                if isinstance(result, dict):
                    keys = list(result.keys())[:5]  # First 5 keys
                    print(f"   Sample keys: {keys}")
                elif isinstance(result, list):
                    print(f"   Array with {len(result)} items")
                    if result and len(result) > 0:
                        print(f"   Sample item keys: {list(result[0].keys()) if isinstance(result[0], dict) else 'Not a dict'}")
                
            except Exception as e:
                print(f"❌ FAILED: {str(e)[:50]}...")
                failed += 1
        
        print()
        print("📊 New Endpoints Test Results:")
        print("=" * 40)
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(successful / (successful + failed) * 100):.1f}%")
        
        return successful, failed
        
    except Exception as e:
        print(f"❌ New endpoint testing failed: {e}")
        return 0, 1

def main():
    """Main testing function"""
    print("🧪 New Endpoints Testing")
    print("=" * 60)
    print("Testing newly discovered working endpoints")
    print()
    
    successful, failed = test_new_endpoints()
    
    if successful > 0:
        print(f"\n🎉 {successful} new endpoints are working!")
        print("These can be used to expand the MCP server functionality.")
    else:
        print(f"\n⚠️  No new endpoints are working.")
        print("The new endpoints may need further investigation.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
