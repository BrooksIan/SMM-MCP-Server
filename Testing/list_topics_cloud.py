#!/usr/bin/env python3
"""
List Topics from Cloud Environment
Demonstrate listing topics using the working MCP server
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def list_topics_cloud():
    """List topics from the cloud environment"""
    
    print("📋 Listing Topics from Cloud Environment")
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
        
        print("✅ Connected to cloud SMM environment")
        print(f"   Gateway: {config.knox_gateway_url}")
        print(f"   User: {config.knox_user}")
        print()
        
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
        
        # Get all topics
        print("🔍 Retrieving topics from SMM...")
        topics = client.get_all_topic_infos()
        
        print(f"✅ Found {len(topics)} topics:")
        print()
        
        # Display topics in a nice format
        for i, topic in enumerate(topics, 1):
            topic_name = topic.get('resourceName', 'Unknown')
            topic_type = topic.get('type', 'Unknown')
            is_internal = topic.get('internal', False)
            
            # Format the display
            status = "🔒 INTERNAL" if is_internal else "📊 USER"
            print(f"{i:2d}. {status} {topic_name}")
            
            # Show additional details if available
            if 'partitions' in topic:
                partition_count = len(topic['partitions'])
                print(f"     Partitions: {partition_count}")
            
            if 'configs' in topic and topic['configs']:
                print(f"     Configs: {len(topic['configs'])} settings")
        
        print()
        print("📊 Topic Summary:")
        print(f"   Total Topics: {len(topics)}")
        
        # Count internal vs user topics
        internal_count = sum(1 for topic in topics if topic.get('internal', False))
        user_count = len(topics) - internal_count
        
        print(f"   User Topics: {user_count}")
        print(f"   Internal Topics: {internal_count}")
        
        # List user topics separately
        if user_count > 0:
            print()
            print("📋 User Topics (Non-Internal):")
            user_topics = [topic for topic in topics if not topic.get('internal', False)]
            for i, topic in enumerate(user_topics, 1):
                topic_name = topic.get('resourceName', 'Unknown')
                print(f"   {i}. {topic_name}")
        
        return topics
        
    except Exception as e:
        print(f"❌ Failed to list topics: {e}")
        return None

def get_topic_details(topic_name):
    """Get detailed information about a specific topic"""
    
    print(f"\n🔍 Getting Details for Topic: {topic_name}")
    print("-" * 50)
    
    try:
        from ssm_mcp_server.client import SMMClient
        from ssm_mcp_server.config import ServerConfig
        from ssm_mcp_server.auth import KnoxAuthFactory
        
        # Create configuration
        config = ServerConfig()
        config.knox_gateway_url = "https://irb-kakfa-only-master0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-kakfa-only/cdp-proxy-api/smm-api"
        config.knox_user = "ibrooks"
        config.knox_password = "Admin12345#"
        config.smm_readonly = True
        config.knox_verify_ssl = True
        
        # Create client
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
        
        # Get topic information
        try:
            topic_info = client.get_topic_info(topic_name)
            print(f"✅ Topic Information for '{topic_name}':")
            print(f"   Partitions: {len(topic_info.get('partitions', []))}")
            print(f"   Internal: {topic_info.get('internal', False)}")
            
            if 'partitions' in topic_info:
                print(f"   Partition Details:")
                for i, partition in enumerate(topic_info['partitions']):
                    print(f"     Partition {i}: {partition}")
            
            return topic_info
            
        except Exception as e:
            print(f"❌ Failed to get topic details: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to create client: {e}")
        return None

def main():
    """Main function"""
    print("🧪 List Topics from Cloud Environment")
    print("=" * 60)
    print("Demonstrating topic listing with working MCP server")
    print()
    
    # List all topics
    topics = list_topics_cloud()
    
    if topics:
        print("\n🎉 Successfully listed topics from cloud environment!")
        
        # Get details for a specific topic if available
        user_topics = [topic for topic in topics if not topic.get('internal', False)]
        if user_topics:
            sample_topic = user_topics[0].get('resourceName')
            if sample_topic:
                get_topic_details(sample_topic)
    else:
        print("\n❌ Failed to list topics")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
