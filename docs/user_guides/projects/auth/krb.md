# Login using Kerberos

## Introduction
Hopsworks supports different methods of authentication. Here we will look at authentication using Kerberos.

## Prerequisites

A Hopsworks cluster with Kerberos authentication. 
See [Configure Kerberos](../../../../admin/ldap/configure-krb) on how to configure Kerberos on your cluster.

### Step 1: Log in with Kerberos
If Kerberos is configured you will see a _Log in using_ alternative on the login page. Choose Kerberos and click on 
**Go to Hopsworks** to login. 

<figure>
  <img width="400px" src="../../../../assets/images/admin/ldap/login-using-krb.png" alt="Log in using Kerberos" />
  <figcaption>Log in using Kerberos</figcaption>
</figure>

If password login is disabled you only see the _Log in using Kerberos/SSO_ alternative. Click on
**Go to Hopsworks** to login.
<figure>
  <img width="400px" src="../../../../assets/images/admin/ldap/krb-login.png" alt="Kerberos only" />
  <figcaption>Kerberos only authentication</figcaption>
</figure>

To be able to authenticate with Kerberos you need to configure your browser to use Kerberos. 
Note that without a properly configured browser, the Kerberos token is not sent to the server and so SSO will not work.

If Kerberos is not configured properly you will see **Wrong credentials** message when trying to log in.
<figure>
  <img width="400px" src="../../../../assets/images/admin/ldap/no-ticket.png" alt="Browser not configured" />
  <figcaption>Missing Kerberos ticket</figcaption>
</figure>

### Step 2: Give consent
When logging in with Kerberos for the first time Hopsworks will retrieve and save consented claims (firstname, lastname
and email), about the logged in end-user. If you have multiple email addresses registered in Kerberos you can choose 
one to use with Hopsworks.

If you do not want your information to be saved in Hopsworks you can click **Cancel**. This will redirect you back
to the login page.

<figure>
  <img width="400px" src="../../../../assets/images/auth/consent.png" alt="OAuth2 consent" />
  <figcaption>Give consent</figcaption>
</figure>

After clicking on **Register** you will be redirected to the landing page:
  <figure>
    <img alt="landing page" src="../../../../assets/images/auth/landing-page.png">
    <figcaption>Landing page</figcaption>
  </figure>

In the landing page, you will find two buttons. Use these buttons to either create a 
_demo project_ or [a new project](../../../projects/project/create_project).

## Conclusion
In this guide you learned how to log in to Hopsworks using Kerberos.