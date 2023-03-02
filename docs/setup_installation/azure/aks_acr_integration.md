# Integration with Azure AKS

This guide shows how to create a cluster in [managed.hopsworks.ai](https://managed.hopsworks.ai) with integrated support for Azure Kubernetes Service (AKS). This enables Hopsworks to launch Python jobs, Jupyter servers, and serve models on top of AKS.

This guide provides an example setup with a private AKS cluster and [public ACR registry](getting_started.md#step-3-create-an-acr-container-registry).
!!! note
    A public AKS cluster means the Kubernetes API server is accessible outside the virtual network it is deployed in. Similarly, a public ACR is accessible through the internet.


## Step 1: Create an AKS cluster
Go to *Kubernetes services* in the azure portal and click *Add* then *Add Kubernetes cluster*. Place the Kubernetes cluster in the same resource group and region as the Hopsworks cluster and choose a name for the Kubernetes cluster.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-base.png" alt="AKS general configuration">
    <figcaption>AKS general configuration</figcaption>
  </figure>
</p>

Next, click on the *Authentication* tab and verify the settings are as follow:

* Authentication method: System-assigned managed identity
* Role-based access control (RBAC): Enabled
* AKS-managed Azure Active Directory: Disabled

!!! note
    Currently, AKS is only supported through managed identities. Contact the Logical Clocks sales team if you have a self-managed Kubernetes cluster.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-authentication.png" alt="AKS authentication configuration">
    <figcaption>AKS authencation configuration</figcaption>
  </figure>
</p>

Next, go to the networking tab and check **Azure CNI**. The portal will automatically fill in the IP address ranges for the Kubernetes virtual network. Take note of the virtual network name that is created, in this example the virtual network name was hopsworksstagevnet154. Lastly, check the **Enable private cluster** option. 

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-network.png" alt="AKS network configuration">
    <figcaption>AKS network configuration</figcaption>
  </figure>
</p>

Next press *Review + create*, then click *Create*.

### Step 1.1: Add role assignment to the managed identity

Go to the managed identity created in [Step 2.2](getting_started#step-22-creating-a-user-assigned-managed-identity). Click on *Azure role assignments* in the left column. Click on *Add role assignment*. For the *Scope* select *Resource group* or *Subscription* depending on your preference. Select the *Role* *Azure Kubernetes Service Cluster User Role* and click on *Save*.

Once finished the role assignments should look similar to the picture below. 

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-permissions.png" alt="AKS permissions">
    <figcaption>AKS permissions</figcaption>
  </figure>
</p>


## Step 2: create a virtual network for the Hopsworks cluster

Because the Kubernetes API service is private the Hopsworks cluster must be able to reach it over a private network. There are two options to integrate with a private AKS cluster. The first option (*A*) is to put the Hopsworks cluster in a pre-defined virtual network with a peering setup to the Kubernetes network. The second option (*B*) is to create a subnet inside the Kubernetes virtual network where the Hopsworks cluster will be placed.

### Option *A*: Peering setup

To establish virtual peering between the Kubernetes cluster and Hopsworks, you need to select or create a virtual network for Hopsworks. Go to **virtual networks** and press create.
Choose a name for the new virtual network and select the same resource group you are planning to use for your Hopsworks cluster.

Next, go to the *IP Addresses* tab. Create an address space that does not overlap with the address space in the Kubernetes network. In the previous example, the automatically created Kubernetes network used the address space *10.0.0.0/8*. Hence, the address space *172.18.0.0/16* can safely be used.

Next click *Review + Create*, then *Create*.

Next, go to the created virtual network and go to the *Peerings* tab. Then click *Add*. 

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-peering.png" alt="Virtual network peering">
    <figcaption>Virtual network peering</figcaption>
  </figure>
</p>

Choose a name for the peering link. Check the *Traffic to remote virtual network* as *Allow*, and *Traffic forwarded from remote virtual network* to *Block*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-peering1.png" alt="Virtual network peering">
    <figcaption>Virtual network peering configuration</figcaption>
  </figure>
</p>

For the virtual network select the virtual network which was created by AKS, in our example this was *hopsworksstagevnet154*. Then press *Add*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-peering2.png" alt="Virtual network peering">
    <figcaption>Virtual network peering configuration continuation</figcaption>
  </figure>
</p>

The last step is to set up a DNS private link to be able to use DNS resolution for the Kubernetes API servers. Go to resource groups in the Azure portal and find the resource group of the Kubernetes cluster. This will be in the form of *MC_<resouce_group>_<cluster_name>_<region>* in this example it was *MC_hopsworks-stage_hopsworks-aks_northeurope*. Open the resource group and click on the DNS zone.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-private-dns.png" alt="Virtual network peering">
    <figcaption>Private DNS link setup</figcaption>
  </figure>
</p>

In the left plane there is a tab called *Virtual network links*, click on the tab. Next press *Add*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-vnet-link.png" alt="">
    <figcaption>Private DNS link configuration</figcaption>
  </figure>
</p>

Choose a name for the private link and select the **virtual network** you will use for the Hopsworks cluster, then press OK.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-vnet-link-config.png" alt="">
    <figcaption>Private DNS link configuration</figcaption>
  </figure>
</p>

The setup is now finalized and you can create the Hopsworks cluster.

### Option *B*: Subnet in AKS network

With this setup, the Hopsworks cluster will reside in the same virtual network as the AKS cluster. The difference is that a new subnet in the virtual network will be used for the Hopsworks cluster.

To set up the subnet, first, go to the virtual network that was created by AKS. In our example, this was hopsworksstagevnet154. Next, go to the subnets tab.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-subnet.png" alt="">
    <figcaption>AKS subnet setup</figcaption>
  </figure>
</p>

Press *+ Subnet*. Choose a name for the subnet, for example, "hopsworks" and an IP range that does not overlap with the Kubernetes network. Then save.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-subnet-config.png" alt="">
    <figcaption>AKS subnet setup</figcaption>
  </figure>
</p>

## Step 3: Create the Hopsworks cluster

This step assumes you are creating your Hopsworks cluster using [managed.hopsworks.ai](https://managed.hopsworks.ai). The AKS configuration can be set under the *Managed containers* tab. Set *Use Azure AKS* as enabled. One new field will pop up. Fill it with the name of the AKS you created above. In the previous example, we created an AKS cluster with the name *hopsaks-cluster*. Hence, the configuration should look similar to the picture below

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/aks-hops-config.png" alt="">
    <figcaption>Hopsworks AKS configuration</figcaption>
  </figure>
</p>

In the virtual network tab, you have to select either the virtual network you created for the peering setup or the Kubernetes virtual network depending on which approach you choose. Under the subnet tab, you have to choose the default subnet if you choose the peering approach or the subnet you created if you choose to create a new subnet inside the AKS virtual network.

