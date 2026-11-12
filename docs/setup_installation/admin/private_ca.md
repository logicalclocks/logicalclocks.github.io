---
description: How to make Hopsworks trust a private certificate authority, for example for an S3-compatible store served over TLS, through the Kyverno policy the Helm chart ships
---

# Private CA Trust { #private-ca-trust }

## Introduction

Hopsworks connects to external services from the Hopsworks server and from the jobs, notebooks and services it runs.
When a service presents a certificate issued by a private certificate authority (CA), every component that connects to it must trust that CA.
An [S3 data source on an S3-compatible store][data-source-s3-compatible] served over TLS is the common case.

The Hopsworks Helm chart ships a [Kyverno](https://kyverno.io) policy for this.
It mounts a CA bundle, the ConfigMap `ca-pemstore`, over `/etc/ssl/certs` in the pods of the Hopsworks namespace and of the project namespaces, and copies the ConfigMap into project namespaces as they are created.
The bundle replaces the directory, so it holds the public root CAs as well as the private one.

## Prerequisites { #private-ca-prerequisites }

- Kyverno installed in the cluster, engine only.
  The chart is tested with the Kyverno Helm chart 3.3.3 (Kyverno 1.13.1).
- The certificates of the private CA in PEM format, one file each: the root CA, and every intermediate CA between it and the service's certificate, such as an issuing CA.
- `kubectl`, `docker` and `keytool` (from a Java runtime) on the machine that builds the bundle.

## Build the bundle { #private-ca-bundle }

Add the root CA and every intermediate CA to the bundle.
The clients differ in what they accept: boto3 does not trust a service through an intermediate CA alone, and no client fetches an intermediate CA that the service does not send.
`openssl s_client -connect <host>:<port> -showcerts` lists the certificates a service sends.

The bundle has these keys:

- `ca-certificates.crt`: the public root CAs and the private CA certificates, read by Python, DuckDB and other clients that use the system bundle.
- `java-cacerts`: the Java truststore with the private CA certificates added, mounted at `/etc/ssl/certs/java/cacerts`, where the Java runtime of the Hopsworks Spark images looks for it.
- `private-ca.crt`: the root CA alone.
- `private-ca-<n>.crt`: each intermediate CA alone, one key per certificate.
  The Hopsworks server imports every `.crt` and `.pem` file of the bundle into its own truststore when it starts, the first certificate of each file only.

Start from the files of an image the workloads use, so the public roots match theirs, and add the private CA certificates:

```bash
IMAGE=<a Hopsworks Spark image>
ROOT=root-ca.crt
INTERMEDIATES=(issuing-ca.crt)
mkdir bundle

cid=$(docker create "$IMAGE")
docker cp -L "$cid:/etc/ssl/certs/ca-certificates.crt" bundle/ca-certificates.crt
docker cp -L "$cid:/etc/ssl/certs/java/cacerts" bundle/java-cacerts
docker rm "$cid"

files=(--from-file=private-ca.crt="$ROOT")
n=0
for cert in "$ROOT" "${INTERMEDIATES[@]}"; do
  cat "$cert" >> bundle/ca-certificates.crt
  keytool -importcert -noprompt -keystore bundle/java-cacerts -storepass changeit -alias "private-ca-$n" -file "$cert"
  [ "$cert" = "$ROOT" ] || files+=(--from-file="private-ca-$n.crt=$cert")
  n=$((n + 1))
done

kubectl -n hopsworks create configmap ca-pemstore \
  --from-file=ca-certificates.crt=bundle/ca-certificates.crt \
  --from-file=java-cacerts=bundle/java-cacerts \
  "${files[@]}"
```

Create the ConfigMap with `kubectl create`, or with `kubectl apply --server-side`.
A client-side `kubectl apply` stores the whole bundle in an annotation, which exceeds the 256 KiB annotation limit.

## Configure the chart { #private-ca-values }

```yaml
global:
  _hopsworks:
    kyverno:
      enabled: true
      policies:
        addCertificatesVolume:
          enabled: true
          preconditions:
            enabled: false
hw-kyverno:
  policies:
    addCertificatesVolume:
      items:
        - {key: ca-certificates.crt, path: ca-certificates.crt}
        - {key: java-cacerts, path: java/cacerts}
        - {key: private-ca.crt, path: private-ca.crt}
      envs:
        - {name: SSL_CERT_FILE, value: /etc/ssl/certs/ca-certificates.crt}
        - {name: REQUESTS_CA_BUNDLE, value: /etc/ssl/certs/ca-certificates.crt}
        - {name: AWS_CA_BUNDLE, value: /etc/ssl/certs/ca-certificates.crt}
```

- `preconditions.enabled: false` mounts the bundle into every pod of the Hopsworks namespace and of the project namespaces, which covers Spark, Python and notebook workloads.
  With the preconditions on, the policy only reaches the pods that opt in: the admin server, the Arrow Flight server, HopsFS, and the docker and git jobs listed in `hw-kyverno.policies.addCertificatesVolume.labels`.
- `items` places the Java truststore in the `java` subdirectory, which a ConfigMap key cannot name.
  It also lists the other keys to mount, and a key without an entry is not mounted, so add one per intermediate CA key, such as `- {key: private-ca-1.crt, path: private-ca-1.crt}`.
  List only keys the ConfigMap has: a pod waits in `ContainerCreating` while an entry names a missing key.
- `envs` points the clients that do not read `/etc/ssl/certs` at the bundle: boto3 reads `AWS_CA_BUNDLE`, and the `requests` library reads `REQUESTS_CA_BUNDLE`.
- Leave `hw-kyverno.policies.addCertificatesVolume.labels` unset: a value replaces the default list rather than extending it.

All values are listed in [Kyverno values][helm-values-hw-kyverno].

## Apply { #private-ca-apply }

1. Create `ca-pemstore` in the Hopsworks namespace before enabling the policy.
   A pod the policy mutates waits in `ContainerCreating` until the ConfigMap exists in its namespace.
2. Upgrade Hopsworks with the values above.
3. Copy the bundle into the project namespaces that existed before the policy.
   The policy copies it when a namespace is created or updated, so annotate the existing ones:

    ```bash
    for ns in $(kubectl get ns -l hopsworks.ai/project -o jsonpath='{.items[*].metadata.name}'); do
      kubectl annotate ns "$ns" hopsworks.ai/ca-resync="$(date +%s)" --overwrite
    done
    kubectl get configmap ca-pemstore -A
    ```

4. Restart the Hopsworks server instances, so that they copy the truststore that the admin server imported the CA into when the upgrade restarted it.
   Scale them to 0 and back rather than restarting them one by one, which can leave an instance with stale configuration:

    ```bash
    replicas=$(kubectl -n hopsworks get deployment hopsworks-instance -o jsonpath='{.spec.replicas}')
    kubectl -n hopsworks scale deployment hopsworks-instance --replicas=0
    kubectl -n hopsworks rollout status deployment hopsworks-instance
    kubectl -n hopsworks scale deployment hopsworks-instance --replicas="$replicas"
    kubectl -n hopsworks rollout status deployment hopsworks-instance
    ```

5. Restart the Arrow Flight server, `kubectl -n hopsworks rollout restart deployment/arrowflight-deployment`, and any running notebook servers.
   Other pods get the bundle when they are next created.

## Verify { #private-ca-verify }

- In a pod of a project namespace, `/etc/ssl/certs/ca-certificates.crt` and `/etc/ssl/certs/java/cacerts` exist.
- `keytool -list -keystore /etc/ssl/certs/java/cacerts -storepass changeit -alias private-ca-0` finds the root CA.
- An S3 data source on the store, created with its `https://` endpoint, lists the bucket's tables in the data source view.

## Rotate the CA { #private-ca-rotation }

Replace `ca-pemstore` in the Hopsworks namespace.
The policy keeps the copies in the project namespaces in step with it.
Workloads read the bundle when they start, so the change reaches the ones started afterwards.
The Hopsworks server needs the admin server restarted, `kubectl -n hopsworks rollout restart deployment/hopsworks-admin`, then the instances scaled to 0 and back as in [Apply][private-ca-apply].
