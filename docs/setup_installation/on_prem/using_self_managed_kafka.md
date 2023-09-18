# Using self-managed Kafka

Hopsworks uses Kafka for streaming applications and ingesting data.
The users have the opportunity to operate Hopsworks-managed Kafka or integrate their own Kafka service.

## Bringing your own Kafka

By default, Hopsworks comes with a Kafka cluster, but it is possible to use your own. 
For this, the cluster configuration ‘enable_bring_your_own_kafka’ value has to be set to ‘true’.
Furthermore, additional changes must be made to the Hopsworks Online Feature Store service (OnlineFS) and each project.

### Online Feature Store service configuration

The OnlineFS has to be configured with the necessary properties to consume messages from the self-managed Kafka.
This can be done by providing the OnlineFS with the Kafka configuration file and any other entities (such as certificates) necessary for communication.
When relying on more than one Kafka cluster it is necessary to define a new instance of OnlineFS for each of them.

### Project configuration

The configuration is done for each project to ensure its members have the necessary authentication/authorization to use the service.

To consume and produce Kafka events, Hopsworks relies on storage connectors to contain the required properties.
The accepted configuration can be found here: [apache kafka configuration](https://kafka.apache.org/documentation/#configuration).
If a storage connector is not found in the project, default values referring to hopsworks-managed Kafka will be used.

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/on_prem/kafka_connector.png" alt="Example Kafka storage connector">
    <figcaption>Example Kafka Storage connector</figcaption>
  </figure>
</p>

The name reserved for this storage connector is "kafka_connector".

## Usage

Assuming that the configuration of the previously mentioned components is properly defined the subsequent usage of Hopsworks will remain mostly unchanged.
The only exception is that the management of topics is the users' responsibility.
