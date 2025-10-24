#!/usr/bin/env python3
"""
Quick Test of MCP Tools in Cloud Environment
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def quick_test():
    """Quick test of MCP tools"""
    
    print("🧪 Quick MCP Tools Test")
    print("=" * 40)
    
    try:
        from ssm_mcp_server.client import SMMClient
        from ssm_mcp_server.config import ServerConfig
        from ssm_mcp_server.auth import KnoxAuthFactory
        
        # Create configuration for cloud environment
        config = ServerConfig()
        config.knox_gateway_url = os.getenv("KNOX_GATEWAY_URL", "https://irb-kakfa-only-master0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-kakfa-only/cdp-proxy-api/smm-api")
        config.knox_user = os.getenv("KNOX_USER", "ibrooks")
        config.knox_password = os.getenv("KNOX_PASSWORD", "Admin12345#")
        config.smm_readonly = True
        config.knox_verify_ssl = True
        
        print("✅ Configuration created")
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
        
        print("✅ SMM client created")
        
        # Test a few key tools
        test_tools = [
            ("get_smm_info", "SMM Info"),
            ("get_cluster_details", "Cluster Details"),
            ("get_brokers", "Brokers"),
            ("get_all_topic_infos", "Topics"),
            ("get_admin_cluster", "Admin Cluster"),
        ]
        
        print("\n🔍 Testing Key MCP Tools:")
        print("-" * 30)
        
        successful = 0
        failed = 0
        
        for method_name, description in test_tools:
            try:
                print(f"Testing {description}...", end=" ")
                
                # Get the method from the client
                method = getattr(client, method_name)
                
                # Call the method
                result = method()
                
                print("✅ SUCCESS")
                successful += 1
                
                # Show some sample data
                if isinstance(result, dict):
                    keys = list(result.keys())[:3]
                    print(f"   Sample keys: {keys}")
                elif isinstance(result, list):
                    print(f"   Array with {len(result)} items")
                
            except Exception as e:
                print(f"❌ FAILED: {str(e)[:50]}...")
                failed += 1
        
        print(f"\n📊 Test Results:")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Success Rate: {(successful / (successful + failed) * 100):.1f}%")
        
        if successful > 0:
            print("\n🎉 MCP tools are working in cloud environment!")
        else:
            print("\n⚠️  MCP tools are not working. Check your configuration.")
        
        return successful, failed
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 0, 1

def main():
    """Main function"""
    print("🚀 Quick MCP Tools Test")
    print("=" * 40)
    print("Testing key MCP tools against cloud environment")
    print()
    
    successful, failed = quick_test()
    
    if successful > 0:
        print(f"\n✅ {successful} tools are working!")
    else:
        print(f"\n❌ No tools are working. Check your configuration.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
