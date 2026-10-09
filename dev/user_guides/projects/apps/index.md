# Apps

Apps are long-running applications that run as managed services in Hopsworks.
Use them for Streamlit dashboards or custom web apps such as Flask, FastAPI, Gradio, or JavaScript apps like Express.
Common uses include:

- Interactive data apps that visualize model predictions or project data.
- Predictive analytics dashboards.
- Chatbot UIs for internal or external assistants.
- GenAI front ends, such as a Gradio or Streamlit RAG assistant.
- FastAPI services that expose inference or other application endpoints.

Each app is backed by a Hopsworks job and a Kubernetes deployment, so it can be started, stopped, redeployed, and deleted like any other project service.

## Where to find Apps

1. Open your project in Hopsworks.
2. In the current sidebar, open **AI/ML** and click **Apps**.
3. Click **New App** to create one.

The Apps page lists each app with its name, owner, state, UI link, uptime, and action buttons.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/apps/apps_list.png" alt="Apps list">
    <figcaption>The Apps page with one app serving</figcaption>
  </figure>
</p>

!!! note "Shared WebSocket capacity"
    Apps share the same per-pod WebSocket session pool as Jupyter and terminals.
    If you see capacity warnings, close unused sessions or see [Session Capacity Warnings](../jupyter/session_capacity_warnings.md).

## Creating an app

The create dialog lets you choose the app type, source, runtime environment, app base path, readiness probe path, resources, monitoring, and per-app environment variables.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/apps/create_app.png" alt="New App form">
    <figcaption>The New App form: type, source, app file and resources</figcaption>
  </figure>
</p>

| Setting | Typical value |
| --- | --- |
| App type | `STREAMLIT` or `CUSTOM` |
| Proxy routing mode | `Root routing` for new apps, `Compatibility prefix` for legacy apps |
| App base path | `/` for the app root, `/myapp` for a subpath |
| Readiness probe path | Leave empty to use the platform default |
| Source | Project file or Git repository |
| Environment | `python-app-pipeline` |
| Memory | `2048` MB |
| CPU cores | `1.0` |
| Custom app port | `8080` |

### App types

- **Streamlit** apps are the default choice for dashboards and interactive ML UIs.
- **Custom** apps are any web service that listens on `APP_PORT`.
  Common choices are Flask, FastAPI, Gradio, and JavaScript frameworks such as Express.

Use `App base path` to choose where Hopsworks mounts the app.
Set it to `/` for a root-based app or `/myapp` for a subpath.
Legacy prefix routing is only for older apps that still depend on `APP_BASE_URL_PATH`.
Use `Proxy routing mode` to switch between `Root routing` and `Compatibility prefix`.
The compatibility mode is only for migrating older apps.

### App sources

- **Project file** means a file already stored in HopsFS or the project file browser.
- **Git repository** means the app source is cloned on every start.
  This is useful when you want a proper Git-backed CI/CD flow and when you want local file edits not to affect a running production app.
  The deployed app only sees the repository contents that are present when it starts, so changes in your working tree stay local until you commit, push, and redeploy.

For Streamlit apps, a project file must be a `.py` file.
For Git-backed Streamlit apps, you also need to provide the entrypoint script relative to the repository root.
For custom apps, the entrypoint command is required and the app file is optional.

#### Auto-redeploy on new commits

Git-backed apps can roll themselves to the branch HEAD whenever a new commit is pushed.
Enable **Auto-redeploy on new commits** in the app settings, or pass `git_auto_redeploy=True` to the SDK.

Hopsworks polls the remote branch and, when it moves, rolls the app onto the new commit.
The running app keeps serving until the new version is ready, so there is no gap in availability.
While the roll is in progress the app shows **Redeploying** in the apps list.

The setting only applies to Git-backed apps.
An app without a Git source has nothing to poll, and Hopsworks rejects the flag in that case.

If you do not set a branch, the clone follows the repository's default branch, and the app details page shows the branch it resolved to once the app has run.

### Routing and readiness

The browser URL for every app is the public mount point under `/hopsworks-api/pythonapp/<project>/<app>/`.
If you set `App base path` to `/myapp`, the full public URL becomes `/hopsworks-api/pythonapp/<project>/<app>/myapp/`.

Hopsworks strips the public mount prefix before forwarding requests upstream, so app code can stay root-based.

Hopsworks forwards `X-Forwarded-Prefix` for frameworks that need to generate absolute links.

The proxy routing mode controls whether Hopsworks strips that prefix or preserves the legacy browser path.
Open **App Settings** and change `Proxy routing mode` under **App routing and readiness** to switch an app.

Readiness is separate from browser routing.

Streamlit defaults to `/_stcore/health`.

Custom apps default to `/`.

You can override the readiness probe path in the app settings dialog or API when needed.

### Example structure

Most apps follow the same pattern:

1. Put the app code in your project or Git repository.
2. Choose the `python-app-pipeline` environment or clone it if you need extra libraries.
3. Set the resources the pod should reserve.
4. Add monitoring routes if you want Envoy metrics for specific paths.
5. Start the app and wait for it to reach `Serving`.

!!! tip "Default environment"
    The `python-app-pipeline` environment is the default runtime for Apps.
    If your app needs additional dependencies, clone that environment and install the extra packages there instead of modifying the base image.

## Writing app code

### Streamlit apps

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/apps/streamlit_app.png" alt="A Streamlit app served by Hopsworks">
    <figcaption>A Streamlit dashboard reading a feature group, served through the Hopsworks proxy</figcaption>
  </figure>
</p>

Streamlit apps are launched with `streamlit run` behind the Hopsworks proxy.
Hopsworks manages the mount prefix for you, so Streamlit apps can stay root-based.
If the app is Git-backed, the entrypoint script is relative to the repository root.
The default readiness probe for Streamlit is `/_stcore/health`.

### Custom apps

Custom apps should bind to `0.0.0.0` and use the injected `APP_PORT`.
Define routes at `/` and `/health`.
Use legacy prefix-aware routes only while migrating an older app that still depends on `APP_BASE_URL_PATH`.

```python
import os

import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"status": "ready"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["APP_PORT"]))
```

### App base path

`APP_BASE_URL_PATH` is deprecated and should not be used in new apps.

For new apps, use `App base path` in the UI or API and let Hopsworks handle the browser mount prefix.
Keep `Proxy routing mode` set to `Root routing` for new apps.

Examples:

- FastAPI: `@app.get("/health")`
- Flask: `Blueprint(..., url_prefix="/")`
- Gradio: `demo.launch(..., root_path=None)`
- Express: `app.use("/", router)`

If you are migrating an older app that still depends on `APP_BASE_URL_PATH`, keep the legacy pattern only until the app code can move to root-based routing.
In that case, use `Compatibility prefix` in the app settings dialog during the migration period.

See the matching examples in [appshopsworkstests](https://github.com/gibchikafa/appshopsworkstests).

## Runtime and environment variables

Apps run inside a project environment and receive the same project context as other Hopsworks services.
Per-app environment variables are applied every time the app starts.

The platform injects app-specific variables such as:

- `APP_BASE_URL_PATH` for legacy prefix-mode apps only
- `APP_PORT`
- `STREAMLIT_BASE_URL_PATH`
- `STREAMLIT_PORT`
- `APP_FILE`
- `APP_PATH`
- `APP_KIND`
- `APP_ARGS`

Git-backed apps also receive the Git URL, provider, branch, and Streamlit entrypoint script.

`APP_BASE_URL_PATH` is only injected for legacy prefix-mode apps during migration.

Some runtime names are reserved by the platform and cannot be overridden in the UI.
That includes the app-path and routing variables above, plus other platform-managed names that start with `HOPS_`, `HOPSWORKS_`, `HOPSFS_`, or `AGENT_`.

## Database and feature store access

Every app can reach the project's feature store data from inside the pod:

- the project's **online feature store database** on RonDB (MySQL protocol), where the online feature group tables live and where the app can keep its own tables: sessions, settings, agent memory, job results. This is on by default and controlled by **Database access** in the create dialog, `db_access` in the SDK and `--no-db-access` in the CLI;
- the project's **offline feature groups**. A Python app reads them with the Hopsworks Python SDK, as any other Hopsworks client does: [feature group](../../fs/feature_group/index.md) reads and [feature view](../../fs/feature_view/batch-data.md) batch data. When Trino is enabled on the cluster, the app also gets the [Trino query engine](../trino/query_engine.md) as an SQL path to the same tables, which is what an app in another language uses. This does not depend on the database access flag: an app created with `db_access=False` still gets the Trino variables.

The database is created on demand the first time an app with database access starts, so it works in a project that never created an online feature group. The app finds everything in its environment; nothing has to be configured.

| Variable | Value |
| --- | --- |
| `MYSQL_HOST`, `MYSQL_PORT` | the online feature store MySQL server |
| `MYSQL_DB` | the project database, the project name in lowercase |
| `MYSQL_USER` | the MySQL user of the person who **started** the app |
| `MYSQL_PASSWORD_SECRET_NAME` | the Hopsworks secret holding that user's password |
| `TRINO_HOST`, `TRINO_PORT` | the Trino coordinator (HTTPS), when Trino is enabled |
| `TRINO_USER` | the Trino user of the person who started the app, `<project>__<username>` |
| `TRINO_PASSWORD_SECRET_NAME` | the Hopsworks secret holding that user's Trino password |
| `TRINO_SCHEMA` | the project's offline feature store schema, `<project>_featurestore` |
| `LIBHDFS_ROOT_CA_BUNDLE`, `NODE_EXTRA_CA_CERTS` | the cluster CA as a PEM file, so any HTTP client can verify the Hopsworks REST API and the Trino coordinator |

Passwords are never placed in the environment. They are private secrets of the user who started the app, and the app reads them with its own credentials, through the Python SDK or the REST API. The privileges follow that user's project role: an app started by a Data Owner can create tables and write, an app started by a Data Scientist has read-only access. There is no `TRINO_CATALOG` because the catalog depends on each feature group's format: `delta` for Delta feature groups, `hudi` for Hudi ones.

The variables are listed on the app details page under **Environment variables**, next to the per-app ones.

### Python

Read offline feature groups with the Hopsworks Python SDK first. It is what the rest of the platform uses, it knows the feature group's format and location, and a feature view adds point-in-time joins and the model's transformations, so a dashboard and the model it shows stay consistent.

```python
import hopsworks


project = hopsworks.login()  # in-cluster: no prompt
fs = project.get_feature_store()

# Offline feature group: a DataFrame, filtered and projected on the server side
transactions = fs.get_feature_group("transactions", version=1)
recent = (
    transactions.select(["cc_num", "amount", "event_time"])
    .filter(transactions.event_time >= "2025-01-01")
    .read()
)

# Feature view: batch data with the point-in-time joins and transformations of the model
fv = fs.get_feature_view("fraud_model", version=1)
batch = fv.get_batch_data(start_time="2025-01-01", end_time="2025-02-01")
```

The online database is for the app's own tables and for primary-key lookups on the online feature group tables:

```python
import os

import pymysql

password = project.get_secrets_api().get(os.environ["MYSQL_PASSWORD_SECRET_NAME"])
conn = pymysql.connect(
    host=os.environ["MYSQL_HOST"],
    port=int(os.environ["MYSQL_PORT"]),
    user=os.environ["MYSQL_USER"],
    password=password,
    database=os.environ["MYSQL_DB"],
)
```

Create the app's own tables with an explicit `ENGINE=NDBCLUSTER`, a primary key, and an `app_` prefix so they never collide with feature group tables (`<feature_group>_<version>`). Write features through `feature_group.insert()`, not straight into the online tables; reading them with SQL is fine.

Trino is an extra option for a Python app: ad-hoc SQL over the offline tables, a join with another Trino catalog, or a query the SDK does not express. The SDK wraps the connection:

```python
trino = project.get_trino_api().connect(
    catalog="delta", schema=os.environ["TRINO_SCHEMA"]
)
cursor = trino.cursor()
cursor.execute(
    "SELECT * FROM transactions_1 WHERE event_time >= DATE '2025-01-01' LIMIT 100"
)
rows = cursor.fetchall()
```

### JavaScript

A [custom app](#custom-apps) can run Node.js: the `python-app-pipeline` environment ships Node and the `@hopsworks/app` module, which turns the variables above into ready-to-use connections. Import it from any app without adding it to `package.json`.

```js
import mysql from "mysql2/promise";
import { mysqlConfig, trinoClient, query, getSecret } from "@hopsworks/app";

// Online feature store / the app's own tables
const pool = mysql.createPool({ ...(await mysqlConfig()), connectionLimit: 5 });
const [rows] = await pool.execute("SELECT * FROM transactions_1 WHERE cc_num = ?", [ccNum]);

// Offline feature groups through Trino; the catalog is the feature group's format
const trino = await trinoClient({ catalog: "delta" });
const recent = await query(trino,
  "SELECT cc_num, amount, event_time FROM transactions_1 WHERE event_time >= DATE '2025-01-01' LIMIT 100");

// Any other secret of the user who started the app
const apiKey = await getSecret("openai_api_key");
```

`mysqlConfig()` returns `{ host, port, user, password, database }` for `mysql2`, `mysql` or `knex`. `trinoClient()` returns a client authenticated as the starting user that speaks the [Trino REST protocol](https://trino.io/docs/current/develop/client-protocol.html); `query()` collects a result as an array of row objects and `streamQuery()` yields rows page by page for large results, cancelling the query if you stop early. Integers above 2^53 come back as `BigInt`, so identifiers are never rounded. Both resolve the password once per process from the Hopsworks secret, and TLS to the platform works out of the box through `NODE_EXTRA_CA_CERTS`. Outside a Hopsworks pod the functions throw an error naming the missing variable; guard local development on `inHopsworks()`.

```python
node_app = apps.create_app(
    "node_api",
    app_kind="CUSTOM",
    git_url="https://github.com/my-org/node-api.git",
    git_provider="GitHub",
    entrypoint_command='bash -lc "npm ci --omit=dev && exec node server.js"',
    app_port=8080,
)
```

Trino is the right path for scans and aggregations over the offline tables; primary-key lookups belong on the online tables. Trino's HTTP protocol has no bound parameters, so never interpolate user input into SQL text.

## Managing an app

The Apps list and the app details page expose the same lifecycle actions:

- **Start** launches the current app configuration.
- **Stop** stops the running execution.
- **Restart / Redeploy** rolls the Kubernetes deployment and starts a fresh execution with the same configuration.
- **Open App** opens the serving URL in a new tab.
- **Logs** shows stdout and stderr for the latest execution.
- **Kubernetes status** shows the deployment and pod health.
- **Edit** opens the app settings dialog.
- **Delete** removes the app entirely.

Edit and delete are only available when the app is stopped.
The app URL is only shown once the backend confirms that the app is actually serving.
That means `RUNNING` and `Serving` are not the same thing: `Serving` is the state where the Hopsworks proxy can reach the app end to end.

### What the app details page shows

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/apps/app_details.png" alt="App details page">
    <figcaption>The app details page: lifecycle actions, source, URL and metrics</figcaption>
  </figure>
</p>

The details page includes:

- App details, type, and description
- App URL
- App base path, proxy routing mode, and readiness probe path
- Public access status for Streamlit apps
- Git source details, if the app is Git-backed, including the branch, the deployed commit, and whether auto-redeploy is enabled
- Monitoring configuration
- Resource requests
- Runtime environment
- Environment variables: the per-app ones and the database and feature store access variables the platform injects
- App metrics and Kubernetes health

## Public access for Streamlit apps

!!! warning "Public Streamlit links are not read-only"
    Anyone with the link can use the app with the app's own credentials, secrets, and data access.
    Disabling public access revokes all live links immediately.

Public access is only available when all of the following are true:

- The app is a Streamlit app.
- You are a Data Owner in the project.
- The administrator has enabled the `streamlit_sharing` feature flag.
- The app is currently serving.

When public access is enabled, Hopsworks shows a share link in the UI.
The link is built through the Hopsworks proxy, so users still access the app through the platform rather than directly.

## Monitoring and metrics

Apps can publish Envoy-based request metrics.
Monitoring is enabled by default, and route filters are optional.

- Use exact or prefix route matches to narrow the traffic that gets counted.
- Leave routes empty if you want the default behavior.
- For Streamlit apps, the platform automatically ignores framework noise such as static assets, health checks, and websocket handshake traffic.
- For custom apps, route filters are useful for paths such as `/api` or `/predict`.

The app details page embeds metrics for request count, request rate, latency, CPU usage, and memory usage.

## Python SDK

Use the Python SDK when you want to create or manage apps from code.

```python
import hopsworks


project = hopsworks.login()
apps = project.get_app_api()

app = apps.create_app(
    "customer_dashboard",
    app_path="Resources/app.py",
    db_access=True,  # default: the online database, see above
)

app.run()
print(app.app_url)
```

A Git-backed app that redeploys itself on every push:

```python
app = apps.create_app(
    "customer_dashboard",
    app_kind="STREAMLIT",
    git_url="https://github.com/my-org/my-app.git",
    git_provider="GitHub",
    git_branch="main",
    git_auto_redeploy=True,
    entrypoint_script="src/app.py",
)
```

Common SDK methods:

- `project.get_app_api()`
- `apps.create_app(...)`
- `app.run()`
- `app.redeploy()`
- `app.stop()`
- `app.delete()`
- `app.make_public()` / `app.make_private()`
- `app.app_url`

## CLI

The `hops` CLI wraps the same app lifecycle API:

```bash
hops app list
hops app info <name>
hops app url <name>
hops app create <name> --path /Projects/<project>/Resources/app.py --start
hops app start <name>
hops app redeploy <name>
hops app stop <name>
hops app logs <name>
hops app delete <name> --yes
```

Use `--git-url` and `--entrypoint-script` for Git-backed Streamlit apps.
Use `--entrypoint-command` and `--app-port` for custom apps.
Add `--git-auto-redeploy` to roll a Git-backed app onto every new commit.
Pass `--no-db-access` for an app that must not get the online database variables; Trino access does not depend on it.

## See also

- [Python Environments](../python/python_env_overview.md)
- [Clone a Python Environment](../python/python_env_clone.md)
- [Python Deployment](../python-deployment/python-deployment.md)
- [Session Capacity Warnings](../jupyter/session_capacity_warnings.md)
- [Superset](../superset/superset.md)
- [Query Engine (Trino)](../trino/query_engine.md)
- [Secrets](../secrets/create_secret.md)
