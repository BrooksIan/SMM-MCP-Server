#!/usr/bin/env python3
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
