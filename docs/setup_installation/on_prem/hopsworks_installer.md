# Hopsworks Installer


The _hopsworks-installer.sh_ script downloads, configures, and installs Hopsworks. It is typically run interactively, prompting the user about details of what to be is installed and where. It can also be run non-interactively (no user prompts) using the '-ni' switch.


## Requirements

You need at least one server or virtual machine on which Hopsworks will be installed with at least the following specification:

* Centos/RHEL 7.x or Ubuntu 18.04;
* at least 32GB RAM,
* at least 8 CPUs,
* 100 GB of free hard-disk space,
* outside Internet access (if this server is air-gapped, contact us for support),
* a UNIX user account with sudo privileges.


## Quickstart


To install on your single server or VM, run the following bash commands from your user account with sudo privileges:

```bash

wget https://raw.githubusercontent.com/logicalclocks/karamel-chef/master/hopsworks-installer.sh
chmod +x hopsworks-installer.sh
./hopsworks-installer.sh
```

Installation takes roughly 1 hr, or slower if your server/VM has a low-bandwidth Internet connection.

Once your installation is finished, you can stop (and start) Hopsworks using the commands:

```bash

sudo /srv/hops/kagent/kagent/bin/shutdown-all-local-services.sh
sudo /srv/hops/kagent/kagent/bin/start-all-local-services.sh
```

Note that all services in Hopsworks are systemd services that are enabled by default, that is, they will restart when VM/server is rebooted.

## Multi-node installation

### Configure installer ssh access


You need to identify a set of servers/VMs and create the same user account with sudo privileges on all the servers. You should identify one server as the head server from which you will perform the installation. You need to ensure that the nodes can communicate with each other on every port and to configure password-less SSH Access from the Head node to Worker nodes. First, on the head node, you should create an openssh keypair without a password:

```bash

cat /dev/zero | ssh-keygen -m PEM -q -N ""
cat ~/.ssh/id_rsa.pub

```

The second line above will print the public key for the sudo account on the head node. Copy that public key, and append it to the ~/.ssh/authorized_keys files on all worker nodes, so that that the sudo account on the head node can SSH into the worker nodes without a password. It may be that you need to configure your sshd daemon (sshd_config and sshlogin) to allow openssh-key based login, depending on how your server is configured:

<a href="https://linuxize.com/post/how-to-setup-passwordless-ssh-login/">How to setup passwordless ssh</a>

For both Ubuntu and Centos/RHEL, and assuming the sudo account is 'ubuntu' and our three worker nodes have hostnames 'vm1', 'vm2', and 'vm3', then you could run the following:

```bash

ssh-copy-id -i $HOME/.ssh/id_rsa.pub ubuntu@vm1
ssh-copy-id -i $HOME/.ssh/id_rsa.pub ubuntu@vm2
ssh-copy-id -i $HOME/.ssh/id_rsa.pub ubuntu@vm3

```

Test that you now have passwordless SSH access to all the worker nodes from the head node (assuming 'ubuntu' is the sudo account):

```bash

# from the head VM
ssh ubuntu@vm1
ssh ubuntu@vm2
ssh ubuntu@vm3
```


### Start installation


On the head node, in the sudo account, download and run this script that installs Hopsworks on all hosts. It will ask you to enter the IP address of all the workers during installation:

```bash

wget https://raw.githubusercontent.com/logicalclocks/karamel-chef/master/hopsworks-installer.sh
chmod +x hopsworks-installer.sh
./hopsworks-installer.sh
```

The above script will download and install Karamel on the same server that runs the script. Karamel will install Hopsworks across all hosts. Installation takes roughly 1 hr, slightly longer for large clusters. To find out more about Karamel, read more below.


## Purge an Existing Cluster Installation


```bash

./hopsworks-installer.sh -i purge -ni

```


## Installation from behind an HTTP Proxy (firewall)


Installation will not work if your http proxy has a self-signed certificate.
You can explicitly specify the http proxy by passing the '-p' switch to the installer.

```bash

./hopsworks-installer.sh -p https://1.2.3.4:3283

```

If you have set the environment variable http_proxy or https_proxy, hopsworks-installer.sh will use it, even if you don't specify the '-p-' switch. The '-p' switch overrides the environment variable, if both are set. If both http_proxy and https_proxy environment variables are set, it will favour the http_proxy environment variable. You can change this behavior using the following arguments '-p $https_proxy'.

## Air-gapped installation

Hopsworks can be installed in an air-gapped environment. We recommend that you submit a <a href="https://www.hopsworks.ai/contact">contact form</a> for help in installing in an environment without outbound Internet access.

## Installation Script Options

```bash

usage: [sudo] ./hopsworks-installer.sh 
 [-h|--help]      help message
 [-i|--install-action localhost|localhost-tls|cluster|enterprise|karamel|purge|purge-all] 
                 'localhost' installs a localhost Hopsworks cluster
                 'localhost-tls' installs a localhost Hopsworks cluster with TLS enabled
                 'cluster' installs a multi-host Hopsworks cluster
                 'enterprise' installs a multi-host Enterprise  Hopsworks cluster
                 'kubernetes' installs a multi-host Enterprise Hopsworks cluster with Kubernetes
                 'karamel' installs and starts Karamel
                 'purge' removes Hopsworks completely from this host
                 'purge-all' removes Hopsworks completely from ALL hosts
 [-cl|--clean]    removes the karamel installation
 [-dr|--dry-run]  does not run karamel, just generates YML file
 [-nvme|--nvme num_disks] Number of NVMe disks on worker nodes (for NDB/HopsFS)
 [-c|--cloud      on-premises|gcp|aws|azure]
 [-w|--workers    IP1,IP2,...,IPN|none] install on workers with IPs in supplied list (or none). Uses default mem/cpu/gpus for the workers.
 [-de|--download-enterprise-url url] downloads enterprise binaries from this URL.
 [-dc|--download-opensource-url url] downloads open-source binaries from this URL.
 [-du|--download-user username] Username for downloading enterprise binaries.
 [-dp|--download-password password] Password for downloading enterprise binaries.
 [-gs|--gem-server] Run a local gem server for chef-solo (for air-gapped installations).
 [-ni|--non-interactive)] skip license/terms acceptance and all confirmation screens.
 [-p|--http-proxy) url] URL of the http(s) proxy server. Only https proxies with valid certs supported.
 [-pwd|--password password] sudo password for user running chef recipes.
 [-y|--yml yaml_file] yaml file to run Karamel against.

```