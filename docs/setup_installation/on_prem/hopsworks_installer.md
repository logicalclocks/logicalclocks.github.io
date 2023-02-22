# Hopsworks On premises

It is possible to us Hopsworks on-premises, which means that companies can run their machine learning workloads on their own hardware and infrastructure, rather than relying on a cloud provider. This can provide greater flexibility, control, and cost savings, as well as enabling companies to meet specific compliance and security requirements.

Working on-premises with Hopsworks typically involves collaboration with the Hopsworks engineering teams, as each infrastructure is unique and requires a tailored approach to deployment and configuration. The process begins with an assessment of the company's existing infrastructure and requirements, including network topology, security policies, and hardware specifications.

For further details about on-premise installations; [contact us](https://www.hopsworks.ai/contact).

## Minimum Requirements

You need at least one server or virtual machine on which Hopsworks will be installed with at least the following specification:

* Centos/RHEL 7.x or Ubuntu 18.04;
* at least 32GB RAM,
* at least 8 CPUs,
* 100 GB of free hard-disk space,
* outside Internet access (if this server is air-gapped, contact us for support),
* a UNIX user account with sudo privileges.

Further details about the on-premise installation of Hopsworks:

* If a multi-node installation is possible;
* Installation takes approximately one hour or more, depending on the server/VM specifications and internet connection bandwidth,
* Once the installation is finished, users can log in to the Hopsworks UI using the provided admin credentials,
* All services in Hopsworks are systemd services that are enabled by default, meaning they will restart when the VM/server is rebooted,
* Hopsworks can be installed in an air-gapped environment.
