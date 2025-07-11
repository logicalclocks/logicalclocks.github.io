# How To Use AWS IAM Roles on EC2 instances

## Introduction

When deploying Hopsworks on EC2 instances you might need to assume different roles to access resources on AWS. 
These roles can be configured in AWS and mapped to a project in Hopsworks.

## Prerequisites
Before you begin this guide you'll need the following:

- A Hopsworks cluster running on EC2.
- [Role chaining](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-role-chaining) setup in AWS.
- Configure role mappings in Hopsworks. For a guide on how to configure this see [AWS IAM Role Chaining](../../../../setup_installation/admin/roleChaining).

## UI
In this guide, you will learn how to use a mapped IAM role in your project.

### Step 1: Navigate to your project's IAM Role Chaining tab

In the _Project Settings_ page you can find the _IAM Role Chaining_ section showing a list of all IAM roles mapped to your project.

<figure>
  <img src="../../../../assets/images/guides/iam_role/project-settings.png" alt="Role Chaining"/>
  <figcaption>Role Chaining</figcaption>
</figure>

### Step 2: Use the IAM role 

You can now use the IAM roles listed in your project when creating a Data Source with [Temporary Credentials](../../../fs/data_source/creation/s3/#temporary-credentials).
