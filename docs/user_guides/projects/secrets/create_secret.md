# How To Create A Secret

## Introduction

A Secret is a key-value pair used to store encrypted information accessible only to the owner of the secret. 
Also if you wish to, you can share the same secret API key with all the members of a Project.

## UI

### Step 1: Navigate to Secrets

In the `Account Settings` page you can find the `Secrets` section showing a list of all secrets.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/secrets/secrets.png" alt="API Keys">
    <figcaption>List of secrets</figcaption>
  </figure>
</p>

### Step 2: Create a Secret

Click `New Secret` to bring up the dialog for secret creation. Enter a name for the secret to be used for lookup, and the secret value.

If the secret should be private to this user, select `Private`, to share the secret with all members of a project select `Project` and enter the project name.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/secrets/create_new_secret.png" alt="Create API Key">
    <figcaption>Create new secret dialog</figcaption>
  </figure>
</p>

### Step 3: Secret created

Click `New Secret` to bring up the dialog for secret creation. Enter a name for the secret to be used for lookup, and the secret value.

If the secret should be private to this user, select `Private`, to share the secret with all members of a project select `Project` and enter the project name.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/secrets/secret_created.png" alt="Create API Key">
    <figcaption>Secret is now created</figcaption>
  </figure>
</p>

## Code

### Step 1: Get secrets API

```python
import hopsworks

connection = hopsworks.connection()

secrets_api = connection.get_secrets_api()
```

### Step 2: Create secret

```python
secret = secrets_api.create_secret("my_secret", "Fk3MoPlQXCQvPo")
```

### API Reference

[Secrets](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/secrets/)

## Conclusion

In this guide you learned how to create a secret.