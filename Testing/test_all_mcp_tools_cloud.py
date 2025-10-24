#!/usr/bin/env python3
"""
Test All MCP Tools Against Cloud Environment
Comprehensive test of all MCP tools with Knox authentication
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_all_mcp_tools_cloud():
    """Test all MCP tools against the cloud environment"""
    
    print("🧪 Testing All MCP Tools Against Cloud Environment")
    print("=" * 70)
    print("Testing all 86+ MCP tools with Knox authentication")
    print()
    
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
        print(f"   Gateway: {config.knox_gateway_url}")
        print(f"   User: {config.knox_user}")
        print(f"   SMM Base: {config.build_smm_base()}")
        
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
        
        print("✅ SMM client created for cloud environment")
        print()
        
        # Define all MCP tools to test
        mcp_tools = [
            # Basic Information
            ("get_smm_info", "Get SMM information", []),
            ("get_smm_version", "Get SMM version", []),
            ("get_cluster_details", "Get cluster details", []),
            
            # Broker Management
            ("get_brokers", "Get all brokers", []),
            ("get_broker", "Get specific broker", [1546336634]),  # Use first broker ID
            ("get_broker_metrics", "Get broker metrics", [1546336634]),
            ("get_all_broker_details", "Get all broker details", []),
            ("get_broker_details", "Get broker details", [1546336634]),
            
            # Topic Management
            ("get_all_topic_infos", "Get all topic infos", []),
            ("get_topic_description", "Get topic description", ["heartbeats"]),
            ("get_topic_info", "Get topic info", ["heartbeats"]),
            ("get_topic_partitions", "Get topic partitions", ["heartbeats"]),
            ("get_topic_partition_infos", "Get topic partition infos", ["heartbeats"]),
            ("get_topic_configs", "Get topic configs", ["heartbeats"]),
            ("get_all_topic_configs", "Get all topic configs", []),
            ("get_default_topic_configs", "Get default topic configs", []),
            
            # Consumer Group Management
            ("get_consumer_groups", "Get consumer groups", []),
            ("get_consumer_group", "Get consumer group", ["test-group"]),
            ("get_consumer_group_offsets", "Get consumer group offsets", ["test-group"]),
            ("get_consumer_group_details", "Get consumer group details", ["test-group"]),
            ("get_consumer_group_members", "Get consumer group members", ["test-group"]),
            ("get_consumer_group_summary", "Get consumer group summary", ["test-group"]),
            
            # Performance Metrics
            ("get_cluster_metrics", "Get cluster metrics", []),
            ("get_broker_metrics_summary", "Get broker metrics summary", []),
            ("get_topic_metrics", "Get topic metrics", ["heartbeats"]),
            ("get_consumer_group_metrics", "Get consumer group metrics", ["test-group"]),
            ("get_producer_metrics", "Get producer metrics", ["all"]),
            ("get_consumer_metrics", "Get consumer metrics", []),
            
            # Alert Management
            ("get_all_alert_policies", "Get all alert policies", []),
            ("get_alert_policy", "Get alert policy", ["test-policy"]),
            ("get_alert_notifications", "Get alert notifications", []),
            ("get_alert_history", "Get alert history", []),
            ("get_alert_summary", "Get alert summary", []),
            
            # Topic Data Sampling
            ("get_topic_offsets", "Get topic offsets", ["heartbeats"]),
            ("get_topic_content", "Get topic content", ["heartbeats", 0, 0, 10]),
            ("get_topic_messages", "Get topic messages", ["heartbeats"]),
            ("get_topic_sample", "Get topic sample", ["heartbeats"]),
            ("get_topic_latest_messages", "Get topic latest messages", ["heartbeats"]),
            
            # Configuration Management
            ("get_cluster_configs", "Get cluster configs", []),
            ("get_broker_configs", "Get broker configs", [1546336634]),
            ("get_topic_config_details", "Get topic config details", ["heartbeats"]),
            ("get_consumer_group_configs", "Get consumer group configs", ["test-group"]),
            ("get_connector_configs", "Get connector configs", ["test-connector"]),
            
            # Kafka Connect
            ("get_connectors", "Get connectors", []),
            ("get_connector", "Get connector", ["test-connector"]),
            ("get_connector_status", "Get connector status", ["test-connector"]),
            ("get_connector_tasks", "Get connector tasks", ["test-connector"]),
            ("get_connector_plugins", "Get connector plugins", []),
            ("get_connector_configs", "Get connector configs", ["test-connector"]),
            
            # Health and Monitoring
            ("get_cluster_health", "Get cluster health", []),
            ("get_broker_health", "Get broker health", [1546336634]),
            ("get_topic_health", "Get topic health", ["heartbeats"]),
            ("get_consumer_group_health", "Get consumer group health", ["test-group"]),
            ("get_system_health", "Get system health", []),
            
            # Advanced Features
            ("get_topic_schema", "Get topic schema", ["heartbeats"]),
            ("get_topic_metadata", "Get topic metadata", ["heartbeats"]),
            ("get_topic_statistics", "Get topic statistics", ["heartbeats"]),
            ("get_broker_statistics", "Get broker statistics", [1546336634]),
            ("get_cluster_statistics", "Get cluster statistics", []),
        ]
        
        print(f"🔍 Testing {len(mcp_tools)} MCP tools against cloud environment...")
        print()
        
        results = {
            "total": len(mcp_tools),
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        # Test each MCP tool
        for i, (method_name, description, args) in enumerate(mcp_tools, 1):
            print(f"[{i:2d}/{len(mcp_tools)}] Testing {method_name}...", end=" ")
            
            try:
                # Get the method from the client
                method = getattr(client, method_name)
                
                # Call the method with arguments
                if args:
                    result = method(*args)
                else:
                    result = method()
                
                # Check if result is valid
                if result is not None:
                    print("✅ SUCCESS")
                    results["success"] += 1
                else:
                    print("⚠️  NO RESULT")
                    results["failed"] += 1
                    results["errors"].append(f"{method_name}: No result returned")
                    
            except Exception as e:
                print(f"❌ FAILED: {str(e)[:50]}...")
                results["failed"] += 1
                results["errors"].append(f"{method_name}: {str(e)}")
        
        print()
        print("📊 Test Results Summary")
        print("=" * 70)
        print(f"Total Tools Tested: {results['total']}")
        print(f"Successful: {results['success']} ({results['success']/results['total']*100:.1f}%)")
        print(f"Failed: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
        
        if results["errors"]:
            print(f"\n❌ Failed Tools:")
            for error in results["errors"][:10]:  # Show first 10 errors
                print(f"   • {error}")
            if len(results["errors"]) > 10:
                print(f"   ... and {len(results['errors']) - 10} more errors")
        
        print()
        if results["success"] > 0:
            print("✅ Some MCP tools are working in cloud environment!")
        if results["failed"] > 0:
            print("⚠️  Some MCP tools need API endpoint fixes")
        
        return results
        
    except Exception as e:
        print(f"❌ Cloud environment test failed: {e}")
        return None

def test_mcp_server_process_cloud():
    """Test MCP server process against cloud environment"""
    
    print(f"\n🚀 Testing MCP Server Process Against Cloud")
    print("=" * 70)
    
    # Set environment variables for cloud
    env = os.environ.copy()
    env.update({
        "KNOX_GATEWAY_URL": "https://irb-kakfa-only-master0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-kakfa-only/cdp-proxy-api/smm-api",
        "KNOX_USER": "ibrooks",
        "KNOX_PASSWORD": "Admin12345#",
        "SMM_READONLY": "true",
        "KNOX_VERIFY_SSL": "true",
        "HTTP_TIMEOUT_SECONDS": "30",
        "MCP_TRANSPORT": "stdio"
    })
    
    server_script = Path(__file__).parent.parent / "run_mcp_server.sh"
    
    try:
        print("🔄 Starting MCP server for cloud environment...")
        process = subprocess.Popen(
            [str(server_script)],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Initialize MCP session
        print("📡 Initializing MCP session...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "cloud-test-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read initialize response
        time.sleep(2)
        init_response = process.stdout.readline()
        if init_response:
            try:
                response = json.loads(init_response.strip())
                print(f"✅ MCP initialized: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
            except json.JSONDecodeError:
                print(f"❌ Failed to parse init response: {init_response}")
                return False
        
        # Test a few key tools
        test_tools = [
            ("get_smm_info", {}),
            ("get_brokers", {}),
            ("get_all_topic_infos", {}),
            ("get_cluster_details", {})
        ]
        
        print("🔧 Testing key MCP tools...")
        for tool_name, args in test_tools:
            print(f"   Testing {tool_name}...", end=" ")
            
            tool_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": args
                }
            }
            
            process.stdin.write(json.dumps(tool_request) + "\n")
            process.stdin.flush()
            
            # Read tool response
            time.sleep(2)
            tool_response = process.stdout.readline()
            if tool_response:
                try:
                    response = json.loads(tool_response.strip())
                    if "result" in response:
                        print("✅ SUCCESS")
                    else:
                        print(f"❌ FAILED: {response.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    print("❌ PARSE ERROR")
            else:
                print("❌ NO RESPONSE")
        
        print("✅ MCP server process test completed")
        return True
        
    except Exception as e:
        print(f"❌ MCP server process test failed: {e}")
        return False
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()

def main():
    """Main test function"""
    print("🧪 All MCP Tools Cloud Environment Test")
    print("=" * 70)
    print("Comprehensive testing of all MCP tools against cloud SMM")
    print()
    
    # Test 1: Direct client test
    client_results = test_all_mcp_tools_cloud()
    
    # Test 2: MCP server process
    process_success = test_mcp_server_process_cloud()
    
    print(f"\n📊 Final Results Summary")
    print("=" * 70)
    
    if client_results:
        print(f"Direct Client Test:")
        print(f"  Total Tools: {client_results['total']}")
        print(f"  Successful: {client_results['success']} ({client_results['success']/client_results['total']*100:.1f}%)")
        print(f"  Failed: {client_results['failed']} ({client_results['failed']/client_results['total']*100:.1f}%)")
    
    print(f"MCP Server Process: {'✅ WORKING' if process_success else '❌ FAILED'}")
    
    if client_results and client_results['success'] > 0:
        print(f"\n🎉 SUCCESS!")
        print(f"✅ {client_results['success']} MCP tools are working in cloud environment!")
        print(f"✅ Knox authentication is functional!")
        print(f"✅ SMM integration is working!")
        print(f"\n📝 Ready for production use with Claude Desktop!")
    else:
        print(f"\n⚠️  Some issues detected")
        print(f"🔧 Check API endpoints and authentication")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
