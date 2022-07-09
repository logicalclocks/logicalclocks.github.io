# Scaling up
If you run into limitations due to the instance types you chose during a cluster creation it is possible to scale up the instances to overcome these limitations.

## Scaling up the workers
If spark jobs are not starting in your cluster it may come from the fact that you don't have worker resources to run them. As workers are stateless the best way to solve this problem is to [add new workers](adding_removing_workers.md) with enough resources to handle your job. Or to [configure autoscalling](autoscaling.md) to automatically add the workers when needed.

## Scaling up the head node
You may run into the need to scale up the head node for different reasons. For example:

* You are running a cluster without [dedicated RonDB nodes](../aws/cluster_creation.md#step-12-managed-rondb) and have a workload with a high demand on the online feature store.
* You are running a cluster without [managed containers](../aws/cluster_creation.md#step-7-managed-containers) and want to run an important number of jupyter notebooks simultaneously.

While we are working on implementing a solution to add these features to an existing cluster you can use the following approach to run your head node on an instance with more vcores and memory to handle more load.

To scale up the head node you first have to stop your cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/stop_cluster.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/stop_cluster.png" alt="Stop the cluster">
    </a>
    <figcaption>Stop the cluster</figcaption>
  </figure>
</p>

Once the cluster is stopped you can go to the *Details* tab and click on the head node *instance type*.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/details_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/details_tab.png" alt="Go to details tab an click on the head node instance type">
    </a>
    <figcaption>Go to details tab an click on the head node instance type</figcaption>
  </figure>
</p>

This will open a new window. Select the type of instance you want to change to and click on *Review and submit*

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/node_type_selection.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/node_type_selection.png" alt="Select the new instance type for the heade node">
    </a>
    <figcaption>Select the new instance type for the heade node</figcaption>
  </figure>
</p>

Verify your choice and click on *Modify*

!!! note
    If you set up your account with AWS in a period predating the introduction of this feature you may need to add the indicated permission to your hopsworks.ai role.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/validate_node_type.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/validate_node_type.png" alt="Validate your choice">
    </a>
    <figcaption>Validate your choice</figcaption>
  </figure>
</p>

You can now start your cluster. The head node will be started on an instance type of the new type you chose. 

## Scaling up the RonDB nodes

If you are running a cluster with [dedicated RonDB nodes](../aws/cluster_creation.md#step-12-managed-rondb) and have a workload with a high demand on the online feature store you may need to scale up the RonDB *Datanodes* and *MySQLd* nodes. For this stop the cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/stop_cluster.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/stop_cluster.png" alt="Stop the cluster">
    </a>
    <figcaption>Stop the cluster</figcaption>
  </figure>
</p>

Once the cluster is stopped you can go to the *RonDB* tab.
To scale MySQLd or API nodes, click on the *instance type* for the node you want to scale up.
To scale all datanodes, click on the *Change* button over their instance types.
Datanodes cannot be scaled individually.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/rondb_tab.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/rondb_tab.png" alt="Go to RonDB tab an click on the instance type you want to change">
    </a>
    <figcaption>Go to RonDB tab and click on the instance type you want to change or, for datanodes, click on the Change button</figcaption>
  </figure>
</p>

This will open a new window. Select the type of instance you want to change to and click on *Review and submit*

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/node_type_selection.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/node_type_selection.png" alt="Select the new instance type for the heade node">
    </a>
    <figcaption>Select the new instance type for the heade node</figcaption>
  </figure>
</p>

Verify your choice and click on *Modify*

!!! note
    If you set up your account with AWS in a period predating the introduction of this feature you may need to add the indicated permission to your hopsworks.ai role.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/validate_node_type.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/validate_node_type.png" alt="Validate your choice">
    </a>
    <figcaption>Validate your choice</figcaption>
  </figure>
</p>

You can now start your cluster. The nodes will be started on an instance type of the new type you chose.
