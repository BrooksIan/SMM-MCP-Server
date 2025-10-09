# SMM MCP Server - Limitations and Non-Working Features

This document details the current limitations and non-working features of the SMM MCP Server.

## Current Status

**Overall Success Rate**: 25.6% (22 out of 86 MCP tools working)

## SMM Topic Creation Limitations

**Important**: SMM (Streams Messaging Manager) is primarily a **monitoring and management tool**, not a topic creation tool. While the MCP server can send topic creation requests to SMM (which returns HTTP 204 "No Content"), SMM does not actually create topics.

### What SMM Does:
- ✅ **Monitors** existing topics and their configurations
- ✅ **Tracks** topic metrics, consumer groups, and broker health
- ✅ **Manages** topic configurations and partitions
- ✅ **Provides** comprehensive monitoring and alerting

### What SMM Does NOT Do:
- ❌ **Create** new topics (API accepts requests but doesn't create topics)
- ❌ **Delete** topics (API accepts requests but doesn't delete topics)
- ❌ **Modify** topic structure (partitions, replication factor)

### Working Solutions for Topic Creation:

**Option 1: Kafka Admin Tools (Recommended)**
```bash
# Create topics using kafka-topics.sh
kafka-topics.sh --create \
  --topic CursorTest \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092 \
  --config cleanup.policy=delete
```

**Option 2: Kafka Admin API (Programmatic)**
```python
from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers=['localhost:9092']
)

topic = NewTopic(
    name='CursorTest',
    num_partitions=3,
    replication_factor=1
)

admin_client.create_topics([topic])
```

**Option 3: SMM Web Interface**
- Use the SMM web interface at `http://localhost:9991` for topic management
- SMM will monitor topics created via other means

### Best Practices:
- **Use Kafka admin tools** for topic creation and deletion
- **Use SMM** for monitoring, configuration, and management
- **Use MCP server** for reading topic information and metrics
- **SMM + MCP server** = powerful monitoring solution

## Non-Working MCP Tools (API Endpoint Issues)

The following MCP tools are currently not working due to API endpoint issues and return 404/405 errors:

### **Consumer Group Management (0% working)**
- `get_consumer_groups()` - List all consumer groups
- `get_consumer_group_names()` - Get consumer group names
- `get_consumer_group_info()` - Get consumer group information
- `get_all_consumer_info()` - Get all consumer information
- `get_consumer_info()` - Get specific consumer information
- `reset_offset()` - Reset consumer group offset

### **Metrics and Monitoring (0% working)**
- `get_cluster_with_broker_metrics()` - Cluster metrics with broker data
- `get_cluster_with_topic_metrics()` - Cluster metrics with topic data
- `get_all_consumer_group_metrics()` - All consumer group metrics
- `get_consumer_group_metrics()` - Specific consumer group metrics
- `get_all_producer_metrics()` - All producer metrics
- `get_producer_metrics()` - Specific producer metrics
- `get_topic_metrics()` - Topic metrics
- `get_topic_partition_metrics()` - Topic partition metrics

### **Alert Management (0% working)**
- `get_all_alert_policies()` - List all alert policies
- `get_alert_policy()` - Get specific alert policy
- `add_alert_policy()` - Add new alert policy
- `update_alert_policy()` - Update existing alert policy
- `delete_alert_policy()` - Delete alert policy
- `get_alert_notifications()` - Get alert notifications
- `get_alert_notifications_by_entity_type()` - Get notifications by entity type
- `get_alert_notifications_by_entity_type_and_name()` - Get notifications by entity
- `mark_alert_notifications()` - Mark notifications as read
- `unmark_alert_notifications()` - Unmark notifications

### **Alert Management Enhanced (0% working)**
- `disable_alert_policy()` - Disable alert policy
- `enable_alert_policy()` - Enable alert policy
- `get_alert_policy_automata()` - Get alert policy automata
- `get_alert_notifications_by_entity()` - Get notifications by entity
- `mark_alert_notifications_read()` - Mark notifications as read

### **End-to-End Latency Monitoring (0% working)**
- `get_topic_etelatency()` - Get topic end-to-end latency
- `get_topic_group_etelatency()` - Get topic and group latency

### **Replication Statistics (20% working)**
- `get_replication_stats()` - Get replication statistics
- `get_replication_stats_by_cluster()` - Get replication stats by cluster
- `get_topic_replication_stats()` - Get topic replication stats
- `get_topic_replication_stats_simple()` - Get simple replication stats
- ✅ `is_replication_configured()` - Check replication configuration (working)

### **Schema Registry (0% working)**
- `get_schema_registry_info()` - Get schema registry information
- `get_schema_meta_for_topic()` - Get schema metadata for topic
- `get_key_schema_version_infos()` - Get key schema version info
- `get_value_schema_version_infos()` - Get value schema version info
- `register_topic_schema_meta()` - Register topic schema metadata

### **Kafka Connect (14.3% working)**
- `get_connectors()` - List all connectors
- `get_connector()` - Get specific connector
- `create_connector()` - Create new connector
- `delete_connector()` - Delete connector
- `get_connector_config_def()` - Get connector config definition
- `get_connector_permissions()` - Get connector permissions
- ✅ `get_connect_worker_metrics()` - Get connect worker metrics (working)

### **Kafka Connect Enhanced (62.5% working)**
- ✅ `get_connector_templates()` - Get connector templates (working)
- ✅ `get_connector_config_definitions()` - Get config definitions (working)
- ✅ `get_connector_config_sample()` - Get config sample (working)
- ✅ `is_connect_configured()` - Check connect configuration (working)
- ✅ `get_connect_worker_metrics()` - Get worker metrics (working)
- `validate_connector_config()` - Validate connector configuration
- `perform_connector_action()` - Perform connector actions
- `get_connector_sink_metrics()` - Get connector sink metrics

### **Lineage Tracking (0% working)**
- `get_topic_lineage()` - Get topic lineage
- `get_topic_partition_lineage()` - Get topic partition lineage
- `get_consumer_group_lineage()` - Get consumer group lineage
- `get_producer_lineage()` - Get producer lineage

### **Authentication (0% working)**
- `get_access()` - Get access information
- `login()` - Login to SMM
- `logout()` - Logout from SMM

### **Topic Management Write Operations (0% working)**
- `create_topics()` - Create new topics (SMM limitation)
- `create_partitions()` - Create additional partitions
- `delete_topics()` - Delete topics (SMM limitation)
- `alter_topic_configs()` - Alter topic configurations

## Working MCP Tools (25.6% success rate)

The following MCP tools are currently working and functional:

### **Core Information (100% working)**
- ✅ `get_smm_info()` - SMM system information
- ✅ `get_smm_version()` - SMM version information

### **Cluster and Broker Management (100% working)**
- ✅ `get_cluster_details()` - Cluster details and information
- ✅ `get_brokers()` - All brokers in the cluster
- ✅ `get_broker()` - Specific broker details
- ✅ `get_broker_metrics()` - Broker metrics
- ✅ `get_all_broker_details()` - All broker details
- ✅ `get_broker_details()` - Detailed broker information

### **Topic Management Read Operations (62.5% working)**
- ✅ `get_all_topic_infos()` - All topic information
- ✅ `get_topic_description()` - Topic description
- ✅ `get_topic_info()` - Basic topic information
- ✅ `get_topic_partitions()` - Topic partition information
- ✅ `get_topic_partition_infos()` - Detailed partition information
- ✅ `get_topic_configs()` - Topic configuration
- ✅ `get_all_topic_configs()` - All topic configurations
- ✅ `get_default_topic_configs()` - Default topic configurations

### **Notifiers Management (66.7% working)**
- ✅ `get_notifiers()` - All notifiers
- ✅ `get_notifier_provider_configs()` - Notifier provider configurations
- `get_notifier()` - Specific notifier (not working)

## Resolution Status

**Root Cause**: Most non-working tools fail due to incorrect API endpoints in the SMMClient class.

**Progress Made**: Success rate improved from 10.2% to 25.6% after fixing core API endpoints.

**Next Steps**: Continue fixing API endpoints for remaining tools to achieve 95%+ success rate.

## Contributing to Fixes

If you encounter issues with specific MCP tools:

1. **Check the API endpoint** in `src/ssm_mcp_server/client.py`
2. **Verify the SMM API documentation** for correct endpoints
3. **Test the endpoint directly** using curl or similar tools
4. **Submit a pull request** with the corrected endpoint

## Support

For questions about limitations or to report issues:
- Check the main [README.md](README.md) for general information
- Review the [Testing/README.md](Testing/README.md) for testing procedures
- Open an issue on GitHub for specific problems
