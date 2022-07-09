# Cluster creation in Hopsworks.ai (GCP)
This guide goes into detail for each of the steps of the cluster creation in Hopsworks.ai

### Step 1 starting to create a cluster

In Hopsworks.ai, select *Create cluster*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance.png" alt="Create a Hopsworks cluster">
    </a>
    <figcaption>Create a Hopsworks cluster</figcaption>
  </figure>
</p>

### Step 2 setting the General information

Select the *GCP Project* (1) in which you want the cluster to run.

!!! note
    If the *Project* does not appear in the drop-down, make sure that you properly [Connected your GCP account](./getting_started.md#step-1-connecting-your-gcp-account) for this project.

Name your cluster (2). Choose the *Region*(3) and *Zone*(4) in which to deploy the cluster.

Select the *Instance type* (5) and *Local storage* (6) size for the cluster *Head node*.

Enter the name of the bucket in which the hopsworks cluster will store its data in *Cloud Storage Bucket* (7)

!!! warning
    The bucket must be empty and must be in a region accessible from the region in which the cluster is deployed.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-general.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-general.png" alt="General configuration">
    </a>
    <figcaption>General configuration</figcaption>
  </figure>
</p>

### Step 3 workers configuration

In this step, you configure the workers. There are two possible setups: static or autoscaling. In the static setup, the cluster has a fixed number of workers that you decide. You can then add and remove workers manually, for more details: [documentation](../common/adding_removing_workers.md). In the autoscaling setup, you configure conditions to add and remove workers and the cluster will automatically add and remove workers depending on the demand, for more details: [documentation](../common/autoscaling.md).

#### Static workers configuration
You can set the static configuration by selecting *Disabled* in the first drop-down (1). Then you select the number of workers you want to start the cluster with (2). And, select the *Instance type* (3) and *Local storage* size (4) for the *worker nodes*.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance-workers-static.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance-workers-static.png" alt="Create a Hopsworks cluster, static workers configuration">
    </a>
    <figcaption>Create a Hopsworks cluster, static workers configuration</figcaption>
  </figure>
</p>

#### Autoscaling workers configuration
You can set the autoscaling configuration by selecting enabled in the first drop-down (1). You then have access to a two parts form, allowing you to configure the autoscaling. In the first part, you configure the autoscaling for general-purpose compute nodes. In the second part, you configure the autoscaling for nodes equipped with GPUs. In both parts you will have to set up the following:

1. The instance type you want to use. You can decide to not enable the autoscaling for GPU nodes by selecting *No GPU autoscale*.
2. The size of the instances' disk.
3. The minimum number of workers. 
4. The maximum number of workers.
5. The targeted number of standby workers. Setting some resources on standby ensures that there are always some free resources in your cluster. This ensures that requests for new resources are fulfilled promptly. You configure the standby by setting the number of workers you want to be on standby. For example, if you set a value of *0.5* the system will start a new worker every time the aggregated free cluster resources drop below 50% of a worker's resources. If you set this value to 0 new workers will only be started when a job or notebook requests the resources.
6. The time to wait before removing unused resources. One often starts a new computation shortly after finishing the previous one. To avoid having to wait for workers to stop and start between each computation it is recommended to wait before shutting down workers. Here you set the amount of time in seconds resources need to be unused before they get removed from the system.

!!! note
    The standby will not be taken into account if you set the minimum number of workers to 0 and no resources are used in the cluster. This ensures that the number of nodes can fall to 0 when no resources are used. The standby will start to take effect as soon as you start using resources.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance-workers-autoscale.png">
      <img style="border: 1px solid #000;width:700px;width:506px" src="../../../assets/images/setup_installation/managed/common/create-instance-workers-autoscale.png" alt="Create a Hopsworks cluster, autoscale workers configuration">
    </a>
    <figcaption>Create a Hopsworks cluster, autoscale workers configuration</figcaption>
  </figure>
</p>

### Step 4 select the Service Account
Hopsworks cluster store their data in a storage bucket. To let the cluster instances access the bucket we need to attach a *Service Account* to the virtual machines. In this step, you set which *Service Account* to use by entering its *Email*. This *Service Account* needs to have access right to the *bucket* you selected in [Step 2](#step-2-setting-the-general-information). For more details on how to create the *Service Account* and give it access to the bucket refer to [Creating and configuring a storage](getting_started.md#step-2-creating-and-configuring-a-storage)

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-service-account.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-service-account.png" alt="Set the instance service account">
    </a>
    <figcaption>Set the instance service account</figcaption>
  </figure>
</p>

### Step 5 set the backup retention policy

To backup the storage bucket data when taking a cluster backup we need to set a retention policy for the bucket. In this step, you choose the retention period in days. You can deactivate the retention policy by setting this value to 0 but this will block you from taking any backup of your cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-backup.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-backup.png" alt="Choose the backup retention policy">
    </a>
    <figcaption>Choose the backup retention policy</figcaption>
  </figure>
</p>

### Step 6 VPC and Subnet selection

You can select the VPC which will be used by the Hopsworks cluster. 
You can either select an existing VPC or let Hopsworks.ai create one for you.
If you decide to use restricted hopsworks.ai permissions (see [restrictive-permissions](../restrictive_permissions/#create-a-vpc-permissions) for more details) 
you will need to select an existing VPC here. 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/select-vpc.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/select-vpc.png" alt="Select the vpc">
    </a>
    <figcaption>Select the vpc</figcaption>
  </figure>
</p>

If you selected an existing VPC in the previous step, this step lets you select which subnet of this VPC to use.

If you did not select an existing virtual network in the previous step Hopsworks.ai will create a subnet for you. 
You can choose the CIDR block this subnet will use.
Select the *Subnet* to be used by your cluster and press *Next*.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/select-subnet.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/select-subnet.png" alt="Select the subnet">
    </a>
    <figcaption>Select the subnet</figcaption>
  </figure>
</p>


### Step 7 User management selection
In this step, you can choose which user management system to use. You have three choices: 

* *Managed*: Hopsworks.ai automatically adds and removes users from the Hopsworks cluster when you add and remove users from your organization  (more details [here](../common/user_management.md)).
* *OAuth2*: integrate the cluster with your organization's OAuth2 identity provider. See [Use OAuth2 for user management](../common/sso/oauth.md) for more detail.
* *LDAP*: integrate the cluster with your organization's LDAP/ActiveDirectory server. See [Use LDAP for user management](../common/sso/ldap.md) for more detail.
* *Disabled*: let you manage users manually from within Hopsworks.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance-user-management.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance-user-management.png" alt="Choose user management type">
    </a>
    <figcaption>Choose user management type</figcaption>
  </figure>
</p>

### Step 8 Managed RonDB
Hopsworks uses [RonDB](https://www.rondb.com/) as a database engine for its online Feature Store. By default database will run on its
own VM. Premium users can scale-out database services to multiple VMs
to handle increased workload.

For details on how to configure RonDB check our guide [here](../common/rondb.md).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/rondb/configure_database.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/rondb/configure_database.png" alt="Configure RonDB">
    </a>
    <figcaption>Configure RonDB</figcaption>
  </figure>
</p>

If you need to deploy a RonDB cluster instead of a single node please contact [us](mailto:sales@logicalclocks.com).

### Step 9 add tags to your instances.
In this step, you can define tags that will be added to the cluster virtual machines.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance-tags.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance-tags.png" alt="Add tags">
    </a>
    <figcaption>Add tags</figcaption>
  </figure>
</p>

### Step 10 add an init script to your instances.
In this step, you can enter an initialization script that will be run at startup on every instance.

You can select whether this script will run before or after the VM
configuration. **Be cautious** if you select to run it before the VM
configuration as this might affect Cluster creation.

!!! note
    this init script must be a bash script starting with *#!/usr/bin/env bash*

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/init_script.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/init_script.png" alt="Add initialization script">
    </a>
    <figcaption>Add initialization script</figcaption>
  </figure>
</p>

### Step 11 Review and create
Review all information and select *Create*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-review.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-review.png" alt="Review cluster information">
    </a>
    <figcaption>Review cluster information</figcaption>
  </figure>
</p>

The cluster will start. This will take a few minutes:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/booting.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/booting.png" alt="Booting Hopsworks cluster">
    </a>
    <figcaption>Booting Hopsworks cluster</figcaption>
  </figure>
</p>

As soon as the cluster has started, you will be able to log in to your new Hopsworks cluster. You will also be able to stop, restart, or terminate the cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/running.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/running.png" alt="Running Hopsworks cluster">
    </a>
    <figcaption>Running Hopsworks cluster</figcaption>
  </figure>
</p>
