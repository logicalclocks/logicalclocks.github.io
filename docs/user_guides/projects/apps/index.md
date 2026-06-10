---
description: How to create, run, and manage Hopsworks Apps
---

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

!!! note "Shared WebSocket capacity"
    Apps share the same per-pod WebSocket session pool as Jupyter and terminals.
    If you see capacity warnings, close unused sessions or see [Session Capacity Warnings](../jupyter/session_capacity_warnings.md).

## Creating an app

The create dialog lets you choose the app type, source, runtime environment, resources, monitoring, and per-app environment variables.

| Setting | Typical value |
| --- | --- |
| App type | `STREAMLIT` or `CUSTOM` |
| Source | Project file or Git repository |
| Environment | `python-app-pipeline` |
| Memory | `2048` MB |
| CPU cores | `1.0` |
| Custom app port | `8080` |

### App types

- **Streamlit** apps are the default choice for dashboards and interactive ML UIs.
- **Custom** apps are any web service that listens on `APP_PORT`.
  Common choices are Flask, FastAPI, Gradio, and JavaScript frameworks such as Express.

### App sources

- **Project file** means a file already stored in HopsFS or the project file browser.
- **Git repository** means the app source is cloned on every start.
  This is useful when you want a proper Git-backed CI/CD flow and when you want local file edits not to affect a running production app.
  The deployed app only sees the repository contents that are present when it starts, so changes in your working tree stay local until you commit, push, and redeploy.

For Streamlit apps, a project file must be a `.py` file.
For Git-backed Streamlit apps, you also need to provide the entrypoint script relative to the repository root.
For custom apps, the entrypoint command is required and the app file is optional.

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

Streamlit apps are launched with `streamlit run` behind the Hopsworks proxy.
If the app is Git-backed, the entrypoint script is relative to the repository root.

### Custom apps

Custom apps should bind to `0.0.0.0` and use the injected `APP_PORT`.
If the app needs to build links back into itself, use `APP_BASE_URL_PATH` so the paths include the Hopsworks proxy prefix.

```python
import os

import uvicorn
from fastapi import FastAPI


APP_BASE_URL_PATH = os.getenv("APP_BASE_URL_PATH", "").rstrip("/")
app = FastAPI()


@app.get(f"{APP_BASE_URL_PATH}/health")
def health():
    return {"status": "ok"}


@app.get(f"{APP_BASE_URL_PATH}/")
def home():
    return {"status": "ready", "base_path": APP_BASE_URL_PATH or "/"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["APP_PORT"]))
```

### Proxy-aware paths

`APP_BASE_URL_PATH` is the proxy prefix that Hopsworks mounts your app under, for example:

`/hopsworks-api/pythonapp/<project>/<app>`

Use it whenever your app defines routes, health checks, or links that point back to itself.
The value may be empty in local development, so a common pattern is to strip the trailing slash and fall back to `/` when rendering content.

```python
APP_BASE_URL_PATH = os.getenv("APP_BASE_URL_PATH", "").rstrip("/")
base = APP_BASE_URL_PATH or "/"
```

Examples from Git-backed apps:

- FastAPI: `@app.get(f"{APP_BASE_URL_PATH}/health")`
- Flask: `Blueprint(..., url_prefix=APP_BASE_URL_PATH or None)`
- Gradio: `demo.launch(..., root_path=APP_BASE_URL_PATH or None)`
- Express: `app.use(APP_BASE_URL_PATH || "/", router)`

If you hardcode `/` in those places, the app may work locally but break behind the Hopsworks proxy because the browser requests must include the proxy prefix.

See the matching examples in [appshopsworkstests](https://github.com/gibchikafa/appshopsworkstests).

## Runtime and environment variables

Apps run inside a project environment and receive the same project context as other Hopsworks services.
Per-app environment variables are applied every time the app starts.

The platform injects app-specific variables such as:

- `APP_BASE_URL_PATH`
- `APP_PORT`
- `STREAMLIT_BASE_URL_PATH`
- `STREAMLIT_PORT`
- `APP_FILE`
- `APP_PATH`
- `APP_KIND`
- `APP_ARGS`

Git-backed apps also receive the Git URL, provider, branch, and Streamlit entrypoint script.

Some runtime names are reserved by the platform and cannot be overridden in the UI.
That includes the app-path and proxy-path variables above, plus other platform-managed names that start with `HOPS_`, `HOPSWORKS_`, `HOPSFS_`, or `AGENT_`.

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

The details page includes:

- App details, type, and description
- App URL
- Public access status for Streamlit apps
- Git source details, if the app is Git-backed
- Monitoring configuration
- Resource requests
- Runtime environment
- Per-app environment variables
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
)

app.run()
print(app.app_url)
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

## See also

- [Python Environments](../python/python_env_overview.md)
- [Clone a Python Environment](../python/python_env_clone.md)
- [Python Deployment](../python-deployment/python-deployment.md)
- [Session Capacity Warnings](../jupyter/session_capacity_warnings.md)
- [Superset](../superset/superset.md)
