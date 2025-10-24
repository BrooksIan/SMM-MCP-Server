#!/usr/bin/env python3
"""
Simple Topic Creation Guide
Non-interactive guide for creating new Kafka topics
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def get_broker_info():
    """Get broker information for topic creation"""
    
    print("🔍 Getting Broker Information for Topic Creation")
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
        
        # Get broker information
        brokers = client.get_brokers()
        
        print("✅ Broker Information Retrieved:")
        print(f"   Total Brokers: {len(brokers)}")
        
        broker_list = []
        for i, broker in enumerate(brokers, 1):
            host = broker.get('host', 'Unknown')
            port = broker.get('port', 'Unknown')
            broker_id = broker.get('id', 'Unknown')
            is_controller = broker.get('isController', False)
            
            print(f"   {i}. Broker {broker_id}: {host}:{port}")
            if is_controller:
                print(f"      (Controller)")
            
            broker_list.append(f"{host}:{port}")
        
        bootstrap_servers = ",".join(broker_list)
        print(f"\n🔧 Bootstrap Servers: {bootstrap_servers}")
        
        return {
            "brokers": brokers,
            "bootstrap_servers": bootstrap_servers,
            "controller": next((b for b in brokers if b.get('isController')), brokers[0])
        }
        
    except Exception as e:
        print(f"❌ Failed to get broker info: {e}")
        return None

def create_topic_commands(topic_name, bootstrap_servers):
    """Generate topic creation commands"""
    
    print(f"\n📝 Topic Creation Commands for '{topic_name}'")
    print("=" * 60)
    
    # Basic command
    print("1. 🚀 Basic Topic Creation:")
    print("=" * 40)
    print(f"kafka-topics.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --create \\")
    print(f"  --topic {topic_name} \\")
    print(f"  --partitions 3 \\")
    print(f"  --replication-factor 3 \\")
    print(f"  --command-config client.properties")
    print()
    
    # Advanced command
    print("2. 🔧 Advanced Topic Creation (with configurations):")
    print("=" * 40)
    print(f"kafka-topics.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --create \\")
    print(f"  --topic {topic_name} \\")
    print(f"  --partitions 3 \\")
    print(f"  --replication-factor 3 \\")
    print(f"  --config cleanup.policy=delete \\")
    print(f"  --config retention.ms=604800000 \\")
    print(f"  --config compression.type=snappy \\")
    print(f"  --config max.message.bytes=1000000 \\")
    print(f"  --command-config client.properties")
    print()
    
    # Verification commands
    print("3. 🔍 Verify Topic Creation:")
    print("=" * 40)
    print(f"# List all topics")
    print(f"kafka-topics.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --list \\")
    print(f"  --command-config client.properties")
    print()
    
    print(f"# Describe the new topic")
    print(f"kafka-topics.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --describe \\")
    print(f"  --topic {topic_name} \\")
    print(f"  --command-config client.properties")
    print()
    
    # Test data commands
    print("4. 📊 Test Data Production:")
    print("=" * 40)
    print(f"# Produce test messages")
    print(f"kafka-console-producer.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --topic {topic_name} \\")
    print(f"  --producer-property security.protocol=SSL \\")
    print(f"  --producer-property ssl.truststore.location=<truststore-path> \\")
    print(f"  --producer-property ssl.truststore.password=<truststore-password>")
    print()
    
    print(f"# Consume test messages")
    print(f"kafka-console-consumer.sh \\")
    print(f"  --bootstrap-server {bootstrap_servers} \\")
    print(f"  --topic {topic_name} \\")
    print(f"  --from-beginning \\")
    print(f"  --consumer-property security.protocol=SSL \\")
    print(f"  --consumer-property ssl.truststore.location=<truststore-path> \\")
    print(f"  --consumer-property ssl.truststore.password=<truststore-password>")
    print()

def create_client_properties():
    """Create client.properties template"""
    
    print("5. 📝 Client Properties Configuration:")
    print("=" * 40)
    
    properties_content = '''# Kafka Client Properties Template
# Copy this file and update with your actual values

# Security Protocol
security.protocol=SSL

# SSL Configuration
ssl.truststore.location=<path-to-truststore>
ssl.truststore.password=<truststore-password>
ssl.keystore.location=<path-to-keystore>
ssl.keystore.password=<keystore-password>
ssl.key.password=<key-password>

# Alternative SSL Configuration (if using certificates)
# ssl.ca.location=<path-to-ca-cert>
# ssl.certificate.location=<path-to-client-cert>
# ssl.key.location=<path-to-client-key>

# SASL Configuration (if using SASL)
# sasl.mechanism=PLAIN
# sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="<username>" password="<password>";

# Additional Configuration
request.timeout.ms=30000
retries=3
'''
    
    properties_path = Path(__file__).parent / "client.properties.template"
    
    try:
        with open(properties_path, 'w') as f:
            f.write(properties_content)
        
        print(f"✅ Created: {properties_path}")
        print(f"📝 Copy and update with your actual SSL/SASL settings")
        
    except Exception as e:
        print(f"❌ Failed to create properties template: {e}")

def suggest_topic_names():
    """Suggest some topic names"""
    
    print("💡 Suggested Topic Names:")
    print("=" * 30)
    
    suggestions = [
        "test-topic",
        "mcp-demo-topic", 
        "user-events",
        "data-stream",
        "analytics-events",
        "notification-queue",
        "audit-logs",
        "metrics-data",
        "user-activity",
        "system-events",
        "cursor-test-topic",
        "mcp-integration-test"
    ]
    
    for i, name in enumerate(suggestions, 1):
        print(f"   {i:2d}. {name}")
    
    print(f"\n📝 Choose a topic name or create your own!")

def main():
    """Main function"""
    print("🧪 Create New Kafka Topic Guide")
    print("=" * 60)
    print("Comprehensive guide for creating new Kafka topics")
    print()
    
    # Suggest topic names
    suggest_topic_names()
    
    # Get broker information
    broker_info = get_broker_info()
    
    if not broker_info:
        print("❌ Failed to get broker information")
        return 1
    
    # Create guide for default topic
    topic_name = "mcp-demo-topic"
    bootstrap_servers = broker_info["bootstrap_servers"]
    
    print(f"\n🎯 Creating guide for topic: {topic_name}")
    print(f"   Bootstrap Servers: {bootstrap_servers}")
    
    # Generate commands
    create_topic_commands(topic_name, bootstrap_servers)
    
    # Create client properties template
    create_client_properties()
    
    print(f"\n🎉 Topic creation guide generated for '{topic_name}'!")
    print(f"📝 Choose one of the methods above to create your topic")
    print(f"🔍 Remember to configure SSL/SASL authentication as needed")
    print(f"\n📁 Files created:")
    print(f"   • client.properties.template")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
