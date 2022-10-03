# How to manage your clusters in managed.hopsworks.ai

### Introduction
[Managed.hopsworks.ai](https://managed.hopsworks.ai) is our managed platform for running Hopsworks and the Feature Store in the cloud. On this page, you will get an overview of the different functionalities of the [managed.hopsworks.ai](https://managed.hopsworks.ai) dashboard.

## Prerequisites
If you want to navigate the to the different tabs presented in this document you will need to connect [managed.hopsworks.ai](https://managed.hopsworks.ai) and create a cluster. Instructions about this process can be found in the getting started pages ([AWS](../aws/getting_started.md), [Azure](../azure/getting_started.md), [GCP](../gcp/getting_started.md))

## Dashboard overview
The landing page of [managed.hopsworks.ai](https://managed.hopsworks.ai) can be seen in the picture below. It is composed of three main parts. At the top, you have a menu bar (1) allowing you to navigate between the dashboard and the [settings](./settings.md). Bellow, you have a menu column (2) allowing you to navigate between different functionalities of the dashboard. And finally, in the middle, you find pannels representing your different clusters (3) and a button to [create new clusters](../aws/cluster_creation.md) (4).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/dashboard.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/dashboard.png" alt="Dashboard overview">
    </a>
    <figcaption>Dashboard overview</figcaption>
  </figure>
</p>

The different functionalities of the dashboard are:

- **Clusters**: the landing page which we will detail bellow.
- **Members**: the place to managed the members of your organization ([doc](user_management.md)).
- **Backup**: the place to manage your clusters' backup ([doc](backup.md)).
- **Usage**: the place to get your credits consumption ([doc](usage.md)).

## Managing your clusters in the cluster panel
The cluster panels contain the name of the cluster (1), its state (2) a button to [terminate the cluster](#terminate-the-cluster) (3), a button to [stop the cluster](#stop-the-cluster) (4) and different tabs to manage the cluster (5). You will now learn more details about these actions and tabs.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/cluster_pannel.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/cluster_pannel.png" alt="Cluster pannel structure">
    </a>
    <figcaption>Cluster pannel structure</figcaption>
  </figure>
</p>

### Stop the cluster
To stop a cluster click on the __Stop__ button on the top right part of the cluster panel. Stopping the cluster stop in instances it is running on and delete the workers nodes. This allows you to save credits in [managed.hopsworks.ai](https://managed.hopsworks.ai) and in your cloud provider.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/stop_cluster.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/stop_cluster.png" alt="Stop a cluster">
    </a>
    <figcaption>Stop a cluster</figcaption>
  </figure>
</p>

### Terminate the cluster
To terminate a cluster click on the __Terminate__ button on the top right part of the cluster panel.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/terminate_cluster.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/terminate_cluster.png" alt="Terminate a cluster">
    </a>
    <figcaption>Terminate a cluster</figcaption>
  </figure>
</p>

Terminating the cluster will destroy it and delete all the resources that were automatically created during the cluster creation. To be sure that you are not terminating a cluster by accident you will be asked to confirm that you want to terminate the cluster. To confirm the termination, check the check box and click on __Terminate__.

!!! Note
    Terminating a cluster does not delete or empty the bucket associated with the cluster. This is because this bucket is needed to restore a backup. You can find more information about backups in the [backup documentation](./backup.md).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/terminate_cluster_confirmation.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/terminate_cluster_confirmation.png" alt="Confirm a cluster termination">
    </a>
    <figcaption>Confirm a cluster Termination</figcaption>
  </figure>
</p>

### The general tab
The General tab gives you the basic information about your cluster. If you have created a cluster with managed users it will only give you the URL of the cluster. If you have created a cluster without managed cluster it will also give you the user name and password that were set for the admin user at cluster creation.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/general_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/general_tab.png" alt="General tab">
    </a>
    <figcaption>General tab</figcaption>
  </figure>
</p>

### Manage the services in the services tab
The services tab shows which service ports are open to the internet on your cluster. More details can be found in the [services documentation](./services.md).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/services_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/services_tab.png" alt="Services tab">
    </a>
    <figcaption>Services tab</figcaption>
  </figure>
</p>

### Get information about your cluster state in the Console tab
The console tab display more detailed information about the current state of your cluster. If your cluster is running and everything is as planned it will only say "everything is ok". But, if something failed, this is where you will find more details about the error.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/console_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/console_tab.png" alt="Console tab">
    </a>
    <figcaption>Console tab</figcaption>
  </figure>
</p>


### Manage your backups in the Backups tab
The backups tab is where you create and manage backups for your cluster. You can find more details about the backups, in the [backups documentation](./backup.md).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/backups_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/backups_tab.png" alt="Backups tab">
    </a>
    <figcaption>Backups tab</figcaption>
  </figure>
</p>

### Get more details and manage your workers in the Details tab
The Details tab provides you with details about your cluster setup. It is also where you can [add and remove workers](./adding_removing_workers.md) or [configure the autoscaling](./autoscaling.md).

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/details_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/details_tab.png" alt="Details tab">
    </a>
    <figcaption>Details tab</figcaption>
  </figure>
</p>

### Get more details about your cluster RonDB in the RonDB tab
The RonDB tab provides you with details about the instances running RonDB in your cluster. This is also where you can [scale up Rondb](./scalingup.md) if needed.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/dashboard/rondb_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/dashboard/rondb_tab.png" alt="RonDB tab">
    </a>
    <figcaption>RonDB tab</figcaption>
  </figure>
</p>

## Conclusion
You now have an overview of where your different cluster information can be found and how you can manage your cluster. To go further you can learn how to [add and remove workers](./adding_removing_workers.md) or [configure the autoscaling](./autoscaling.md) on your cluster or how to take and restore [backups](./backup.md).