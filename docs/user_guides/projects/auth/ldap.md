# Login using LDAP

## Introduction
Hopsworks supports different methods of authentication. Here we will look at authentication using LDAP.

## Prerequisites
A Hopsworks cluster with LDAP authentication. 
See [Configure LDAP](../../../../admin/ldap/configure-ldap) on how to configure LDAP on your cluster.

### Step 1: Log in with LDAP
If LDAP is configured you will see a _Log in using_ alternative on the login page. Choose LDAP and type in your 
_username_ and _password_ then click on **Login**.

Note that you need to use your LDAP credentials.
<figure>
  <a  href="../../../../assets/images/admin/ldap/login-ldap.png">
    <img width="400px" src="../../../../assets/images/admin/ldap/login-ldap.png" alt="Log in using LDAP" />
  </a>
  <figcaption>Log in using LDAP</figcaption>
</figure>

### Step 2: Give consent
When logging in with LDAP for the first time Hopsworks will retrieve and save consented claims (firstname, lastname
and email), about the logged in end-user. If you have multiple email addresses registered in LDAP you can choose one to
use with Hopsworks. 

If you do not want your information to be saved in Hopsworks you can click **Cancel**. This will redirect you back 
to the login page.

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
In this guide you learned how to log in to Hopsworks using LDAP.