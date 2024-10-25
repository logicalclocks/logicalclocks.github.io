# Log in To Hopsworks

## Introduction
Hopsworks supports different methods of authentication. Here we will look at authentication using username and password.

## Prerequisites
An account on a Hopsworks cluster.

### Step 1: Log in with email and password
After your account is validated by an administrator you can use your email and password to login.

  <figure>
    <img width="400px" src="../../../../assets/images/auth/login.png" alt="Login" />
    <figcaption>Login with password</figcaption>
  </figure>

### Step 2: Two-factor authentication

If two-factor authentication is enabled you will be presented with a two-factor authentication window after you 
enter your password. Use your authenticator app
(example. [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en&gl=US))
on your phone to get a one-time password.

<figure>
  <img width="400px" src="../../../../assets/images/auth/otp.png" alt="Two-factor" />
  <figcaption>One time password</figcaption>
</figure>

Upon successful login, you will arrive at the landing page:

  <figure>
    <img alt="landing page" src="../../../../assets/images/auth/landing-page.png">
    <figcaption>Landing page</figcaption>
  </figure>

In the landing page, you will find two buttons. Use these buttons to either create a 
_demo project_ or [a new project](../../../projects/project/create_project).
