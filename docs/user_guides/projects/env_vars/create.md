# Account-level Environment Variables

## Introduction

Account-level environment variables are user-scoped, encrypted `name=value` pairs
that Hopsworks injects into every runtime you start in any project where you
are an active member:

- Jobs (Python, Spark, Ray)
- Jupyter notebooks
- Streamlit / Python apps
- Model deployments (KServe, sklearn, TensorFlow, Python predictors)
- Python / agent serving
- Terminal pods

Values are encrypted at rest with the same mechanism as project [Secrets][secrets].
A user can store up to 64 account-level variables; names must match
`^[A-Za-z_][A-Za-z0-9_]*$` and must not collide with platform-reserved names
such as `API_KEY`, `MATERIAL_DIRECTORY`, `PROJECT_ID`, or any name starting with
`HOPS_`, `HOPSWORKS_`, or `HOPSFS_`.

## Precedence

Environment variables resolve in this order, **highest first**:

1. **Per-execution** variables passed at run time
   (`Execution.run_env_vars`) where supported.
2. **Per-runtime** variables supplied at create or update time
   (`Job.envVars`, deployment `predictor_env_vars` / `transformer_env_vars`,
   app `env_vars`).
3. **Account-level** variables defined here.
4. Platform-injected image / runtime defaults (protected by the reserved-name
   list at validation time).

In other words: a value defined for a specific job, deployment, or app
**always overrides** the account-level value with the same name for that one
runtime. To clear an account-level value for a single run, set it to an empty
string at the runtime level.

## UI

### Step 1: Open Account settings

Click your avatar in the top right of Hopsworks and choose **Account settings**.

### Step 2: Open the Environment variables tab

In **Account settings**, click the **Environment variables** tab. You'll see a
list of your existing variables, one per row.

### Step 3: Add a variable

Type a `NAME` and a `value` in the trailing empty row, then click the green
checkmark to save. The value is hidden by default if the name contains
`key` or `token` (case-insensitive); for those rows an eye icon toggles
visibility. All other names render as plain text.

To **edit** a value, change it inline and click the checkmark again. To
**remove** one, click the trash icon.

### Pre-fill in New Job / New Deployment / New App

When you create a new Job, Deployment, or App, the **Environment variables**
section in those dialogs is pre-filled with your account-level variables so
you can see exactly what will be injected. Any value you change in those
dialogs becomes a per-runtime override (precedence #2 above) for that one
runtime; deleting a row from the dialog sends an empty value as a per-runtime
override, effectively clearing the account-level value for that runtime only.

To remove a variable everywhere, delete it from **Account settings → Environment
variables**.

## Python SDK

```python
import hopsworks

hopsworks.login()
api = hopsworks.get_env_vars_api()

# Add
api.create_env_var("OPENAI_API_KEY", "sk-...")

# Add or update (idempotent — safe in setup scripts)
api.set_env_var("HF_TOKEN", "hf_...")

# Read
api.get("OPENAI_API_KEY")              # -> "sk-..." or None
api.get_env_var("OPENAI_API_KEY")      # -> EnvVar object or None

# List
for v in api.get_env_vars():
    print(v.name)

# Update
api.update_env_var("OPENAI_API_KEY", "sk-new")

# Remove
api.delete_env_var("OPENAI_API_KEY")

# Remove all
api.delete_all()
```

`get_env_var` and `get` return `None` for missing names instead of raising,
so they're convenient for "set if missing" patterns. `delete_env_var` raises
`RestAPIError` with `ENV_VAR_NOT_FOUND` if the name doesn't exist.

## Notes

- Account-level variables are **per-user**. They are never shared with other
  users in your project — to share configuration with project members, use
  project-scoped [Secrets][secrets] instead.
- Removing yourself from a project does **not** remove these variables; they
  follow your account, not your project membership.
- Values are encrypted at rest, mirroring Secrets. They are not exposed in
  audit logs or error messages.

[secrets]: ../secrets/create_secret.md
