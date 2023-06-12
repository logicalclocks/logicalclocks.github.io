# Using self-managed Kafka

Hopsworks uses Kafka for streaming applications and ingesting data. The users have the opportunity to operate Hopsworks-managed Kafka or integrate their own Kafka service.

## Bringing your own Kafka

To use your existing Kafka cluster changes have to be made both to the Hopsworks Online Feature store and each project.

### Online Feature store configuration

The Online Feature store has to be configured with the necessary properties to consume messages from the self-managed Kafka.
This can be done by providing the Online Feature store with the Kafka configuration file and any other entities (such as certificates) necessary for communication with Kafka.

### Project configuration

The configuration is done for each project to ensure its members have the necessary authentication/authorization to use the service.

To consume and produce Kafka events, Hopsworks relies on storage connectors to contain the required properties.
The accepted configuration can be found here: [apache kafka configuration](https://kafka.apache.org/documentation/#configuration).
If a storage connector was not found, a new one will be created with default values (it can be altered at any time).

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/on_prem/kafka_connector.png" alt="Example Kafka storage connector">
  </figure>
</p>

The name of the storage connector used for this purpose will be the same across the entire cluster.
It is defined in the cluster definition configuration under the property "online_kafka_storage_connector_name".

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/on_prem/kafka_connector_config.png" alt="The name of the Kafka Storage connector used by Hopsworks">
  </figure>
</p>

## Usage

Assuming that the configuration of the previously mentioned components is properly defined the subsequent usage of Hopsworks will remain unchanged. Therefore, the existing workflows will continue working seamlessly.

