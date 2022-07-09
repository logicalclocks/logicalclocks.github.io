# Login Using A Third-party Identity Provider

## Introduction
Hopsworks supports different methods of authentication. Here we will look at authentication using Third-party Identity Provider.

## Prerequisites
A Hopsworks cluster with OAuth authentication. 
See [Configure OAuth2](../../../../admin/oauth2/create-client) on how to configure OAuth on your cluster.

### Step 1: Log in with OAuth
If OAuth is configured a **Login with ** button will appear in the login page. Use this button to log in to Hopsworks
using your OAuth credentials.

  <figure>
    <a  href="../../../../assets/images/auth/oauth2.png">
      <img width="400px" src="../../../../assets/images/auth/oauth2.png" alt="OAuth2 login" />
    </a>
    <figcaption>Login with OAuth2</figcaption>
  </figure>

### Step 2: Give consent
When logging in with OAuth for the first time Hopsworks will retrieve and save consented claims (firstname, lastname 
and email), about the logged in end-user.

  <figure>
    <a  href="../../../../assets/images/auth/consent.png">
      <img width="400px" src="../../../../assets/images/auth/consent.png" alt="OAuth2 consent" />
    </a>
    <figcaption>Give consent</figcaption>
  </figure>

After clicking on **Register** you will be redirected to the landing page:
  <figure>
    <a  href="../../../../assets/images/auth/landing-page.png">
      <img alt="landing page" src="../../../../assets/images/auth/landing-page.png">
    </a>
    <figcaption>Landing page</figcaption>
  </figure>

In the landing page, you will find two buttons. Use these buttons to either create a 
_demo project_ or [a new project](../../../projects/project/create_project).

## Conclusion
In this guide you learned how to log in to Hopsworks using Third-party Identity Provider.