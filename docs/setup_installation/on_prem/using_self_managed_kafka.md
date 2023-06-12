# Using self-managed Kafka

Hopsworks uses Kafka for streaming applications and ingesting data. The users have the opportunity to operate Hopsworks-managed Kafka or integrate their own Kafka service.

## Bringing your own Kafka

To use your existing Kafka cluster changes have to be made both to the Hopsworks cluster and each project.

### Cluster configuration

The Online Feature store has to be configured with the necessary properties to consume messages from the self-managed Kafka.
This can be done by providing the Online Feature store with the Kafka configuration file and any other entities (such as certificates) necessary for communication with Kafka.

### Project configuration

The configuration is done for each project to ensure that users have the necessary authentication/authorization to use the service.

To consume and produce Kafka events Hopsworks relies on storage connectors to contain the required properties. The accepted configuration can be found here: [apache kafka configuration](https://kafka.apache.org/documentation/#configuration). If a storage connector was not found a new one will be created with default values (it can be altered at any time).

The name of the storage connector used for this purpose will be the same across the whole cluster, it is defined in the cluster definition configuration under the name "online_kafka_storage_connector_name".

## Usage

Assuming that the configuration of the previously mentioned components is properly defined the subsequent usage of Hopsworks will remain unchanged. Therefore, the existing workflows will continue working seamlessly.

