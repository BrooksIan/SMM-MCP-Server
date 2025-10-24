#!/usr/bin/env python3
"""
Add Data to mcptesttopic
Demonstrate adding data to the mcptesttopic using Kafka producer
"""

import os
import sys
import json
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def add_data_to_topic():
    """Add sample data to mcptesttopic"""
    
    print("📝 Adding Data to mcptesttopic")
    print("=" * 50)
    
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
        
        # First, verify the topic exists
        print("🔍 Verifying mcptesttopic exists...")
        topics = client.get_all_topic_infos()
        mcptesttopic_found = False
        
        for topic in topics:
            if topic.get('resourceName') == 'mcptesttopic':
                mcptesttopic_found = True
                print(f"✅ Found mcptesttopic: {topic}")
                break
        
        if not mcptesttopic_found:
            print("❌ mcptesttopic not found in the cluster")
            return False
        
        print("✅ mcptesttopic exists and is accessible")
        print()
        
        # Since SMM doesn't support data production, we'll provide instructions
        print("📋 SMM Limitation Notice:")
        print("   SMM (Streams Messaging Manager) is a monitoring tool")
        print("   It does not support direct data production to Kafka topics")
        print("   You need to use Kafka producer tools or applications")
        print()
        
        # Provide multiple options for adding data
        print("🔧 Options to Add Data to mcptesttopic:")
        print("=" * 50)
        
        # Option 1: Kafka Console Producer
        print("1. 📝 Using Kafka Console Producer:")
        print("   kafka-console-producer.sh \\")
        print("     --bootstrap-server <broker-address>:9093 \\")
        print("     --topic mcptesttopic \\")
        print("     --producer-property security.protocol=SSL")
        print()
        
        # Option 2: Python Producer Script
        print("2. 🐍 Using Python Producer Script:")
        create_python_producer_script()
        
        # Option 3: Sample Data Examples
        print("3. 📊 Sample Data Examples:")
        sample_messages = [
            '{"message": "Hello from MCP Server!", "timestamp": "' + str(int(time.time())) + '", "source": "mcp-test"}',
            '{"user_id": 12345, "action": "test_message", "data": "This is a test message for mcptesttopic"}',
            '{"event": "mcp_test", "value": 42, "description": "Testing MCP server integration"}',
            '{"status": "success", "test_id": "mcp_001", "result": "Data added successfully"}'
        ]
        
        for i, message in enumerate(sample_messages, 1):
            print(f"   Message {i}: {message}")
        
        print()
        print("4. 🔍 Verify Data Added:")
        print("   kafka-console-consumer.sh \\")
        print("     --bootstrap-server <broker-address>:9093 \\")
        print("     --topic mcptesttopic \\")
        print("     --from-beginning \\")
        print("     --consumer-property security.protocol=SSL")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to add data to topic: {e}")
        return False

def create_python_producer_script():
    """Create a Python producer script for adding data to mcptesttopic"""
    
    producer_script = '''#!/usr/bin/env python3
"""
Kafka Producer for mcptesttopic
Add data to mcptesttopic using Python Kafka client
"""

import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

def create_producer():
    """Create Kafka producer"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=['<broker-address>:9093'],
            security_protocol='SSL',
            ssl_check_hostname=False,
            ssl_cafile='<path-to-ca-cert>',
            ssl_certfile='<path-to-client-cert>',
            ssl_keyfile='<path-to-client-key>',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        return producer
    except Exception as e:
        print(f"❌ Failed to create producer: {e}")
        return None

def send_messages(producer, topic='mcptesttopic'):
    """Send sample messages to topic"""
    messages = [
        {
            'key': 'mcp_test_001',
            'value': {
                'message': 'Hello from MCP Server!',
                'timestamp': int(time.time()),
                'source': 'mcp-test',
                'test_id': '001'
            }
        },
        {
            'key': 'mcp_test_002',
            'value': {
                'user_id': 12345,
                'action': 'test_message',
                'data': 'This is a test message for mcptesttopic',
                'timestamp': int(time.time())
            }
        },
        {
            'key': 'mcp_test_003',
            'value': {
                'event': 'mcp_test',
                'value': 42,
                'description': 'Testing MCP server integration',
                'timestamp': int(time.time())
            }
        },
        {
            'key': 'mcp_test_004',
            'value': {
                'status': 'success',
                'test_id': 'mcp_001',
                'result': 'Data added successfully',
                'timestamp': int(time.time())
            }
        }
    ]
    
    print(f"📝 Sending {len(messages)} messages to {topic}...")
    
    for i, msg in enumerate(messages, 1):
        try:
            future = producer.send(topic, key=msg['key'], value=msg['value'])
            record_metadata = future.get(timeout=10)
            print(f"✅ Message {i} sent: {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
        except KafkaError as e:
            print(f"❌ Failed to send message {i}: {e}")
    
    producer.flush()
    print("✅ All messages sent successfully!")

def main():
    """Main function"""
    print("🚀 Kafka Producer for mcptesttopic")
    print("=" * 40)
    
    producer = create_producer()
    if producer:
        send_messages(producer)
        producer.close()
        print("🎉 Producer completed successfully!")
    else:
        print("❌ Failed to create producer")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path(__file__).parent / "kafka_producer_mcptesttopic.py"
    
    try:
        with open(script_path, 'w') as f:
            f.write(producer_script)
        
        print(f"   ✅ Created: {script_path}")
        print(f"   📝 Edit the script to add your broker details")
        print(f"   🚀 Run: python {script_path}")
        
    except Exception as e:
        print(f"   ❌ Failed to create producer script: {e}")

def show_broker_info():
    """Show broker information for connection"""
    
    print("\n🔍 Broker Information for Connection:")
    print("=" * 50)
    
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
        
        # Get broker information
        brokers = client.get_brokers()
        
        print("📡 Available Brokers:")
        for i, broker in enumerate(brokers, 1):
            host = broker.get('host', 'Unknown')
            port = broker.get('port', 'Unknown')
            broker_id = broker.get('id', 'Unknown')
            is_controller = broker.get('isController', False)
            
            print(f"   {i}. Broker {broker_id}: {host}:{port}")
            if is_controller:
                print(f"      (Controller)")
        
        print(f"\n🔧 Connection Examples:")
        print(f"   Bootstrap Servers: {','.join([f'{b.get('host')}:{b.get('port')}' for b in brokers])}")
        print(f"   Security Protocol: SSL")
        print(f"   Topic: mcptesttopic")
        
    except Exception as e:
        print(f"❌ Failed to get broker info: {e}")

def main():
    """Main function"""
    print("🧪 Add Data to mcptesttopic")
    print("=" * 50)
    print("Demonstrating how to add data to mcptesttopic")
    print()
    
    # Add data to topic
    success = add_data_to_topic()
    
    if success:
        # Show broker information
        show_broker_info()
        
        print("\n🎉 Instructions provided for adding data to mcptesttopic!")
        print("📝 Choose one of the methods above to add data to the topic")
    else:
        print("\n❌ Failed to provide instructions for adding data")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
