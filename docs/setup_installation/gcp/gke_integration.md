# Integration with Goolge GKE

This guide demonstrates the step-by-step process to create a cluster in [managed.hopsworks.ai](https://managed.hopsworks.ai) with integrated support for Google Kubernetes Engine (GKE). This enables Hopsworks to launch Python jobs, Jupyter servers, and serve models on top of GKE.

!!! note
    Currently, we don't support sharing GKE clusters between Hopsworks clusters. That is, a GKE cluster can be only used by one Hopsworks cluster. Also, we only support integration with GKE in the same project as Hopsworks cluster.

## Step 1: Attach Kuberentes developer role to the service account for cluster instances

Ensure that the Hopsworks cluster has access to the GKE cluster by attaching the Kubernetes Engine Developer role  to the [service account you will attach to the cluster nodes](getting_started.md#step-3-creating-a-service-account-for-your-cluster-instances). Execute the following gcloud command to attach `roles/container.developer` to the cluster service account. Replace *\$PROJECT_ID* with your GCP project id and *\$SERVICE_ACCOUNT* with your service account that you have created during getting started [Step 3](getting_started.md#step-3-creating-a-service-account-for-your-cluster-instances).

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID --member=$SERVICE_ACCOUNT --role="roles/container.developer"
```

## Steps 2: Create a virtual network to be used by Hopsworks and GKE

You need to create a virtual network and a subnet in which Hopsworks and the GKE nodes will run.To do this run the following commands, replacing *\$PROJECT_ID* with your GCP project id in which you will run your cluster and *\$SERVICE_ACCOUNT* with the service account that you have updated in [Step 1](#step-1-attach-kuberentes-developer-role-to-the-service-account-for-cluster-instances). In this step, we will create a virtual network `hopsworks`, a subnetwork `hopsworks-eu-north`, and 3 firewall rules to allow communication within the virtual network and allow inbount http and https traffic.

```bash
gcloud compute networks create hopsworks --project=$PROJECT_ID --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

gcloud compute networks subnets create hopsworks-eu-north --project=$PROJECT_ID --range=10.1.0.0/24 --stack-type=IPV4_ONLY --network=hopsworks --region=europe-north1

gcloud compute firewall-rules create hopsworks-nodetonode --network=hopsworks --allow=all --direction=INGRESS --target-service-accounts=$SERVICE_ACCOUNT --source-service-accounts=$SERVICE_ACCOUNT --project=$PROJECT_ID

gcloud compute firewall-rules create hopsworks-inbound-http --network=hopsworks --allow=all --direction=INGRESS --target-service-accounts=$SERVICE_ACCOUNT --allow=tcp:80 --source-ranges="0.0.0.0/0" --project=$PROJECT_ID

gcloud compute firewall-rules create hopsworks-inbound-https --network=hopsworks --allow=all --direction=INGRESS --target-service-accounts=$SERVICE_ACCOUNT --allow=tcp:443 --source-ranges="0.0.0.0/0" --project=$PROJECT_ID

```

## Step 3: Create a GKE cluster

In this step, we create a GKE cluster and we set the cluster pod CIDR to `10.124.0.0/14`. GKE offers two different modes of operation for clusters: `Autopilot` and `Standard` clusters. Choose one of the two following options to create a GKE cluster.

### Option 1: Standard cluster 

Run the following gcloud command to create a zonal standard GKE cluster. Replace *\$PROJECT_ID* with your GCP project id in which you will run your cluster.

```bash
gcloud container clusters create hopsworks-gke  --project=$PROJECT_ID --machine-type="e2-standard-8" --num-nodes=1 --zone="europe-north1-c" --network="hopsworks" --subnetwork="hopsworks-eu-north"  --cluster-ipv4-cidr="10.124.0.0/14" --cluster-version="1.27.3-gke.100"
```

Run the following gcloud command to allow all incoming traffic from the GKE cluster to Hopsworks.

```bash	
gcloud compute firewall-rules create hopsworks-allow-traffic-from-gke-pods  --project=$PROJECT_ID --network="hopsworks" --direction=INGRESS --priority=1000  --action=ALLOW --rules=all --source-ranges="10.124.0.0/14"
```

### Option 2: Autopilot cluster

Run the following gcloud command to create an autopilot cluster. Replace *\$PROJECT_ID* with your GCP project id in which you will run your cluster.

```bash
gcloud container clusters create-auto hopsworks-gke --project $PROJECT_ID --region="europe-north1"  --network="hopsworks" --subnetwork="hopsworks-eu-north" --cluster-ipv4-cidr="10.124.0.0/14"
```

Run the following gcloud command to allow all incoming traffic from the GKE cluster to Hopsworks.

```bash	
gcloud compute firewall-rules create hopsworks-allow-traffic-from-gke-pods  --project=$PROJECT_ID --network="hopsworks" --direction=INGRESS --priority=1000  --action=ALLOW --rules=all --source-ranges="10.124.0.0/14"
```

## Step 4: Create a Hopsworks cluster

In [managed.hopsworks.ai](https://managed.hopsworks.ai), follow the same instructions as in [the cluster creation guide](cluster_creation.md) except when setting *Region*, *Managed Containers*, *VPC* and *Subnet*.

- On the General tab, choose the same region as what we use in [Step 2](#steps-2-create-a-virtual-network-to-be-used-by-hopsworks-and-gke) and [Step 3](#step-3-create-a-gke-cluster) (`europe-north1`)
- On the *Managed Containers* tab, choose **Enabled** and input the name of the GKE cluster that we have created in [Step 3](#step-3-create-a-gke-cluster) (`hopsworks-gke`)
- On the VPC and Subnet tabs, choose the name of the network and subnetwork that we have created in [Step 2](#steps-2-create-a-virtual-network-to-be-used-by-hopsworks-and-gke) (`hopsworks`, `hopsworks-eu-north`).

## Step 5: Configure DNS

### Option 1: Standard cluster 
In the setup described in [Step 3](#option-1-standard-cluster), we are using the default DNS which is `kube-dns`. Hopsworks automatically configures `kube-dns` during cluster initialization, so there is no extra steps that needs to be done here. 

Alterntively, if you configure `Cloud DNS` while creating the standard GKE cluster, then you would need to add the following firewall rule to allow the incoming traffic from `Cloud DNS` on port `53` to Hopsworks. `35.199.192.0/19` is the ip range used by Cloud DNS to issue DNS requests, check [this guide](https://cloud.google.com/dns/docs/zones/forwarding-zones#firewall-rules) for more details.

```bash
gcloud compute --project=$PROJECT_ID firewall-rules create hopsworks-clouddns-forward-consul --direction=INGRESS --priority=1000 --network="hopsworks" --action=ALLOW --rules=udp:53 --source-ranges="35.199.192.0/19"
```


### Option 2: Autopilot cluster 

Hopsworks internally uses consul for service discovery and we automically forward traffic from Standard GKE clusters to the corresponding Hopsworks cluster. However,Autopilot clusters don't allow updating the DNS configurations through `kube-dns` and they use Cloud DNS by default. Therefore, in order to allow seamless communication between pods running on GKE and Hopsworks, we would need to add a [forwarding zone](https://cloud.google.com/dns/docs/zones/forwarding-zones) to Cloud DNS to forward `.consul` taffic to Hopsworks head node.

First, we need to get the ip of the Hopsworks head node of your cluster. Replace *\$PROJECT_ID* with your GCP project id in which you will run your cluster, *\$CLUSTER_NAME* with the name you gave to your Hopsworks cluster duing creation in [Step 4](#step-4-create-a-hopsworks-cluster). Using the following gcloud command, we will be able to get the internal ip of Hopsworks cluster

```bash
HOPSWORKS_HEAD_IP=`gcloud compute instances describe --project=$PROJECT_ID $CLUSTER_NAME-master --format='get(networkInterfaces[0].networkIP)'`
```

Use the *\$HOPSWORKS_HEAD_IP* you just got from the above command to create the following forwarding zone on Cloud DNS

```bash
gcloud dns --project=$PROJECT_ID managed-zones create hopsworks-consul --description="Forward .consul DNS requests to Hopsworks" --dns-name="consul." --visibility="private" --networks="hopsworks" --forwarding-targets=$HOPSWORKS_HEAD_IP
```

Finally, you would need to add the following firewall rule to allow the incoming traffic from `Cloud DNS` on port `53` to Hopsworks. `35.199.192.0/19` is the ip range used by Cloud DNS to issue DNS requests, check [this guide](https://cloud.google.com/dns/docs/zones/forwarding-zones#firewall-rules) for more details.

```bash
gcloud compute --project=$PROJECT_ID firewall-rules create hopsworks-clouddns-forward-consul --direction=INGRESS --priority=1000 --network="hopsworks" --action=ALLOW --rules=udp:53 --source-ranges="35.199.192.0/19"
```