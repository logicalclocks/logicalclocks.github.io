# Hopsworks Quick Setup Guide

## Quick Start Script
Get up and running with a single command:
```bash
curl -O https://raw.githubusercontent.com/logicalclocks/hopsworks-k8s-installer/master/install-hopsworks.py
python3 install-hopsworks.py
```

## Essential Information
Hopsworks is an enterprise-grade distributed AI Lakehouse platform with a feature store. Currently supports:

* Amazon Web Services (EKS)

* Google Cloud Platform (GKE)

* Microsoft Azure (AKS)

* OVHCloud

## Technical Requirements

* Kubernetes cluster version ≥ 1.27.0

* 4-5 nodes minimum

* Required tools:
  * kubectl
  * helm
  * Cloud CLI (aws/gcloud/az)

## For the Startups and Enthusiasts
Want to dive deeper? Here's what you need:

### Default Setup

* AWS: m6i.2xlarge instances, EBS GP3 storage

* GCP: n2-standard-8 instances

* Azure: Standard_D8_v4 instances

### Access Points
Once installed, find your services at:

* UI: https://<load-balancer>:28181

* API: https://<load-balancer>:8182

* Default login: admin@hopsworks.ai / admin

## Enterprise & Production
For enterprise deployment, including:

* Production environments

* Custom configurations

* Enterprise SLAs

* Sovereign cloud options

[Contact our team](https://www.hopsworks.ai/contact) for enterprise deployment options.