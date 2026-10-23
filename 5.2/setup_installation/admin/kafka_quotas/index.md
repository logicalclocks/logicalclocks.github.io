# Kafka Quotas { #kafka-quotas }

## Introduction

Hopsworks runs its Kafka cluster with the [Strimzi operator](https://strimzi.io/).
Kafka runs one of two mutually exclusive quota plugins, chosen with `kafka.cluster.kafka.quotas.type`.
Almost every question about quotas reduces to which plugin is active, because each enforces something different and ignores the other's settings.

Strimzi's own default is the built-in `kafka` plugin.
The Hopsworks chart defaults to `strimzi`, which releases before 5.0.13 and 5.1.0 used without a choice.
The values are listed in [Kafka values][helm-values-kafka].

## Choosing a plugin { #kafka-quotas-plugin }

| | `strimzi` | `kafka` (built-in) |
| --- | --- | --- |
| Per-tenant ceiling (`KafkaUser.spec.quotas`) | ignored; a user in `kafka.users` fails the render | enforced |
| Rate semantics | a total per broker, shared between clients | per user, per broker, shared by that user's client IDs |
| Disk-fill guard (`minAvailable*`) | yes | no equivalent |
| Exempting principals | `excludedPrincipals` | not possible |
| CPU and mutation-rate limits | no | `requestPercentage`, `controllerMutationRate` |
| Metrics | aggregated only | per user and client ID |

Pick `strimzi` to protect the cluster: cap the total throughput and stop the disks filling up.
Pick `kafka` to isolate tenants from each other, which is the only mode in which a per-user quota has any effect.
You cannot have both.
Selecting `kafka` gives up the disk guard, so the chart requires you to set `minAvailableRatioPerVolume` to 0 explicitly rather than dropping the guard silently.

## Per-tenant limits { #kafka-quotas-per-tenant }

`KafkaUser.spec.quotas` is enforced only under `type: kafka`.
Set a quota on each user:

```yaml
kafka:
  cluster:
    kafka:
      authorizer:
        principalBuilderClass: ""       # required, see below
      quotas:
        type: kafka
        minAvailableRatioPerVolume: 0   # required: the guard exists only under strimzi
  users:
    - name: team_a
      quotas:
        producerByteRate: 5242880
        consumerByteRate: 20971520
        requestPercentage: 20
      authorization: {...}
```

Per-user quotas require the default Kafka principal builder, `authorizer.principalBuilderClass: ""`.
Strimzi stores the quota of a TLS user under the entity `CN=<username>`, and the built-in plugin matches it against the principal name of the connection.
The chart's default builder, `io.hops.kafka.HopsPrincipalBuilder`, yields the bare CN with any differing subject alternative names appended, not `CN=<username>`, so the quota would never match and never be enforced.
The chart therefore fails the render when a user declared in `kafka.users` carries `quotas` under `type: kafka` with the Hops builder.
KafkaUsers created outside the chart are not checked.

Switching the builder changes the principal form that every ACL and every `authorizer.superUsers` entry is matched against, so review `authorizer.superUsers` before you switch.
The default user quota under `quotas.kafka.*` does not depend on the principal form and works under either builder.

A principal without a quota of its own is unlimited.
That is usually what you want for the platform's own clients, such as OnlineFS and the Strimzi Entity Operator, because the built-in plugin cannot exempt anyone.

Optionally, set a default for the users without a quota under `quotas.kafka.*`.
The Strimzi Cluster Operator writes and reconciles it as the default user quota, and a KafkaUser's own quota overrides it.
Size it so that the platform's own clients still work: the default applies to internal users too, and this plugin has no way to exclude them, as [the Strimzi documentation](https://strimzi.io/docs/operators/1.2.0/configuring.html#type-QuotasPluginKafka-reference) warns.

## Cluster-wide limits and the disk guard { #kafka-quotas-cluster-wide }

```yaml
kafka:
  cluster:
    kafka:
      quotas:
        type: strimzi
        minAvailableRatioPerVolume: 0.01
        strimzi:
          producerByteRate: 104857600   # per broker, shared between clients
          consumerByteRate: 209715200
```

The rates are a total per broker, shared between all clients that are not excluded, not a ceiling per client: one busy client can take most of it while the others are idle.
`minAvailableRatioPerVolume` (default 0.01) and `minAvailableBytesPerVolume` (default 0, off) halt producers when the free space on a broker volume falls below them.

`excludedPrincipals` does not work with `io.hops.kafka.HopsPrincipalBuilder`, the chart's default builder.
That builder appends the alternative names of a certificate to its CN, joined with `;`, so a principal is a set of names rather than one name.
Strimzi renders the exclusion list with `;` as the separator and the plugin splits on `;` with no escaping, so such a principal cannot be written as an entry.
The chart fails the render on an entry that contains `;` or lacks the `User:` prefix, rather than rendering an exclusion that can never match.
The multi-name principal is deliberate: it lets a service be named as a superuser by any of its identities.

So with the Hops builder, a rate throttles the platform's own clients too.
Verify the effect with `kafka-consumer-perf-test.sh` rather than by reading the Kafka resource.
A cluster that sets `principalBuilderClass: ""` uses the default Kafka builder, whose principals can be written as entries, and there exclusions work.
The chart renders only the entries you list in `quotas.strimzi.excludedPrincipals`, so when you set a rate, list the platform's own principals there yourself, in the exact form the broker sees.
A superuser is exempt from ACLs, not from quotas.
Strimzi adds its own broker and Cruise Control principals.

## Verifying the quotas in force { #kafka-quotas-verify }

Check which plugin a broker runs: the `strimzi` plugin installs a callback class, and the built-in plugin configures nothing.

```sh
kubectl get configmap <cluster>-kafka-0 -n <namespace> -o jsonpath='{.data.server\.config}' | grep quota
```

Then inspect the live quota entities:

```sh
kafka-configs.sh --bootstrap-server <broker>:9091 --command-config <cfg> --describe --entity-type users
kafka-configs.sh --bootstrap-server <broker>:9091 --command-config <cfg> --describe --entity-type clients
```

Kafka resolves the most specific entity first, so a quota on a user beats a default.
Measure with `kafka-consumer-perf-test.sh` over at least 30 seconds.
A quota window is 11 samples of 1 second (`quotas.window`), and a shorter run reports well above the configured rate because of the burst allowed at the start.

## Migrating from the quota defaults { #kafka-quotas-defaults-migration }

Charts before 5.0.13 and 5.1.0 had `quotas.defaults.*`, which drove a post-install Job that wrote a default quota for client IDs with `kafka-configs.sh`.
5.0.13 and 5.1.0 removed that Job.
Setting `quotas.defaults.enabled: true` together with `type: kafka` fails the render, because a client-ID default left behind by the old Job takes effect under the built-in plugin.
Under `type: strimzi` the flag is ignored, so existing values keep rendering.

The Job wrote a lower-precedence entity (`/config/clients/<default>`) than the one Strimzi manages (`/config/users/<default>`), ran once per Helm operation, and was never reconciled.
Under the `strimzi` plugin that those charts always used, the brokers never read what it wrote, so on most clusters it enforced nothing.
The exception is a cluster with Strimzi 0.39 CRDs, the `strimzi-0.39` case of [Before you start][kafka4-before-you-start].
Those CRDs dropped the `quotas` block when the Kafka resource was stored, the brokers ran the built-in plugin, and the Job's default applied to every client, OnlineFS included, while `defaults.enabled: true` was set.
The CRD upgrade of the 5.2 upgrade fixes those CRDs, after which the `strimzi` callback takes over and that limit lapses.

Replace the defaults with the fields of the plugin you choose.
Do not copy the numbers across, because the three blocks limit different things:

- `quotas.defaults.*` set a default per client ID, so each application had an allowance of its own.
- `quotas.kafka.*` sets a default per user, per broker, and every client ID that authenticates as that user shares it.
- `quotas.strimzi.*` sets one total per broker, shared by every client that is not excluded.

The same figure is therefore tighter as a user default than as a client-ID default, and tighter again as a broker total.
Applications that share a principal can be throttled by a user default that matches the old client-ID default.

Before you upgrade an existing cluster, check what the Job already wrote.
On a cluster that ran an earlier release with `defaults.enabled: true`, a client-ID default is still stored in Kafka.
Under `strimzi`, with current CRDs, it has no effect, and it takes effect the moment the plugin changes to `kafka`.
On a cluster with Strimzi 0.39 CRDs it has been in effect all along, and the upgrade lifts it, so choose the replacement rates before you upgrade.
Check for it:

```sh
kafka-configs.sh --bootstrap-server <broker>:9091 --command-config <cfg> --describe --entity-type clients
```

To remove it:

```sh
kafka-configs.sh --bootstrap-server <broker>:9091 --command-config <cfg> \
  --entity-type clients --entity-default --alter \
  --delete-config producer_byte_rate,consumer_byte_rate,request_percentage
```

The chart does not remove it for you, because an operator may have set client-ID quotas deliberately.
