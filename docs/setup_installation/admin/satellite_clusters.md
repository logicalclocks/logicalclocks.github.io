---
description: Run the online feature store of some projects in a satellite, a second Hopsworks release next to the central one
---

# Satellite clusters { #satellite-clusters }

## Introduction

A satellite is a second Hopsworks release that holds the online feature store of some projects: its own RonDB, Kafka and Online Feature Store service (OnlineFS), with the MySQL and REST servers that serve online features.
It runs in a namespace of its own in the same Kubernetes cluster as the central release, which keeps everything else: the UI and REST API, the project metadata, the offline feature store and the jobs.
Projects on a satellite get an online feature store that is isolated from the other projects' load and can be sized and placed on its own nodes.

This guide installs a satellite.
Connecting a project to it takes a database account on the satellite, a Kafka topic and a Kafka user of the project's own on the satellite's Kafka, and two data sources in the project, which is done together with Hopsworks support.

## Central { #satellite-clusters-central }

The central release needs three settings before the first satellite, set once:

```yaml
hopsworks:
  variables:
    enable_bring_your_own_kafka: "true"

kafka:
  strimzi-kafka-operator:
    watchAnyNamespace: true

consul:
  consul:
    syncCatalog:
      k8sAllowNamespaces:
        - hopsworks
```

- `enable_bring_your_own_kafka` lets a project use the Kafka of its satellite through the project's data source, as described in [External Kafka cluster][external-kafka-cluster].
  Central's OnlineFS keeps its own connection, to central's Kafka: the satellite's OnlineFS is the one that reads the satellite's Kafka.
- The satellites run no Strimzi operator of their own, so central's operator watches every namespace.
- Consul registers the Services of central's namespace only, `hopsworks` above, so a satellite's Services do not take the names of central's.

## Satellite { #satellite-clusters-values }

A satellite is installed from the same chart and version as central, in its own namespace.
It takes central's cloud values first, such as those of the [AWS getting started guide][aws-getting-started-with-eks] for the cloud provider, the bucket and the image registry, and then the values below in a file of their own.
The example is a satellite named `sat1` in the namespace `onlinefs-sat1`, with a central release in the namespace `hopsworks`:

```yaml
global:
  _hopsworks:
    full_platform: false
    airflow:
      enabled: false
    opensearch:
      enabled: false
    trino:
      enabled: false
    superset:
      enabled: false

hopsworks:
  variables:
    kube_keda_installed: false
    kube_kserve_installed: false

kafka:
  strimzi-kafka-operator:
    enabled: false
  cluster:
    name: sat1
    tlscerts:
      annotations: null
    entityOperator:
      topicOperator: {}
      userOperator: {}
    kafka:
      authorizer:
        type: simple
        authorizerClass: ""
        principalBuilderClass: ""
        superUsers:
          - CN=onlinefs.onlinefs-sat1.svc.cluster.local,OU=,L=onlinefs,ST=Sweden,C=SE
  topics:
    - name: fraud_onlinefs
      replicas: 1
      partitions: 3
  users:
    - name: fraud
      authorization:
        type: simple
        acls:
          - resource:
              type: topic
              name: fraud_onlinefs
              patternType: literal
            operations:
              - All
          - resource:
              type: group
              name: spark-kafka-relation-
              patternType: prefix
            operations:
              - All

onlinefs:
  apiKey:
    secret_name: onlinefs-api-key-sat1
  dependencies:
    kafka:
      url: sat1-kafka-bootstrap.onlinefs-sat1.svc.cluster.local
    mgmd:
      url: mgmds-0.headless-mgmds.onlinefs-sat1.svc.cluster.local
  deployment:
    vectordb:
      enabled: false
  tlscerts:
    commonName: onlinefs.onlinefs-sat1.svc.cluster.local

rondb:
  rondb:
    createPriorityClass: false
    backups:
      pathPrefix: rondb_backup_onlinefs-sat1
    restoreFromBackup:
      pathPrefix: rondb_backup_onlinefs-sat1
    rdrs:
      externalMetadataCluster:
        mgmds:
          - ip: mgmds-0.headless-mgmds.hopsworks.svc.cluster.local

olk:
  filebeat:
    enabled: false
```

- `full_platform: false` installs only the online feature store services, and the optional services are turned off one by one.
- The Kafka cluster takes the satellite's name, and the satellite's OnlineFS is its super user.
- The topic and the user belong to one project, `fraud`, which writes to the satellite's Kafka through them.
  Because of a security fix, each project on the satellite needs Kafka topics of its own and a Kafka user that can use only those topics, each listed by name as in the example, as described in [OnlineFS drops records that arrive on another topic][upgrade-onlinefs-topics].
  Add a topic and a user for each project when it is connected, and an entry in the user's `acls` for each further topic the project gets.
- OnlineFS reads from the satellite's own Kafka and writes to the satellite's own RonDB.
- `rdrs.externalMetadataCluster` points the satellite's REST server at central's RonDB, which holds the feature store metadata and the API keys.
- `createPriorityClass: false`, because central already created the cluster-wide PriorityClass.
- The backup path prefix keeps the satellite's RonDB backups apart from central's, which use `rondb_backup` in the same bucket by default.
- Replace every `sat1` and `onlinefs-sat1` for a satellite of another name, and `hopsworks` when central runs in another namespace.

Size RonDB, Kafka and the replicas of the topic as for any production online feature store.
To run the satellite on its own nodes, apply [Dedicated node pools][dedicated-node-pools] to its values with node labels and taints of its own, such as `Sat1Head` and `Sat1RonDB` in place of `Head` and `RonDB`.
With central's labels and taints, the satellite would run on central's nodes.

### External access { #satellite-clusters-access }

Decide how clients outside the Kubernetes cluster reach the satellite's MySQL server, REST server and Kafka before installing, because the satellite inherits the load balancer settings of the cloud values: with those of the AWS getting started guide it would get internet-facing load balancers of its own.
Put the choice in a third values file, `values.sat1-access.yaml` below, rather than in `values.sat1.yaml`, which already has top-level `global`, `kafka` and `rondb` keys that a second copy would replace.

- For no access from outside the cluster:

    ```yaml
    global:
      _hopsworks:
        externalLoadBalancers:
          enabled: false

    kafka:
      cluster:
        kafka:
          externalLoadBalancer:
            enabled: false

    rondb:
      rondb:
        meta:
          mysqld:
            externalLoadBalancer:
              enabled: false
          rdrs:
            externalLoadBalancer:
              enabled: false
    ```

    The Kafka and RonDB load balancers have switches of their own, which the global one does not override, so the file turns them off as well.

- For a load balancer that you create, follow [Shared load balancers on AWS][shared-load-balancers] with an NLB for this satellite: the file holds that guide's values with the `mysqld`, `rdrs` and `kafka` target groups of this NLB and its DNS name.

## Install { #satellite-clusters-install }

Install central first and wait for it, then each satellite, one at a time, waiting for each before the next.

```bash
kubectl create namespace onlinefs-sat1
kubectl label namespace onlinefs-sat1 hopsworks.ai/onlinefs-cluster=onlinefs-sat1
helm install onlinefs-sat1 hopsworks/hopsworks --version VERSION --namespace onlinefs-sat1 --values values.aws.yaml --values values.sat1.yaml --values values.sat1-access.yaml --wait --timeout=3600s
```

The label adds the satellite's namespace to central's log collection and to central's Kubernetes backup.
That backup needs Velero and `hopsworks.velero.backup.enabled: true` in central's values, as described in [Disaster Recovery][disaster-recovery]; the AWS getting started guide sets it to `false`.
Central adds the namespace to its backup schedule when it is upgraded, or within the hour once central has a project.
Check that the namespace is in the schedule:

```bash
kubectl get schedule k8s-backups-main -n velero -o jsonpath='{.spec.template.includedNamespaces}'
```

Upgrade the satellites and central in the order the [upgrade guide][upgrading-hopsworks] gives for the hop.
