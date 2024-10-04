# Configure your Hopsworks cluster to use LDAP for user management.

If you want to use your organization's LDAP as an identity provider to manage users in your Hopsworks cluster this document
will guide you through the necessary steps to configure [managed.hopsworks.ai](https://managed.hopsworks.ai) to use LDAP.

The LDAP attributes below are used to configure JNDI resources in the Hopsworks server. 
The JNDI resource will communicate with your LDAP server to perform the authentication.
<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/setup_installation/managed/common/sso/ldap.png" alt="Setup ldap">
    <figcaption>Setup LDAP</figcaption>
  </figure>
</p>

- _jndilookupname_: should contain the LDAP domain.
- _hopsworks.ldap.basedn_: the LDAP domain, it should be the same as _jndilookupname_
- _java.naming.provider.url_: url of your LDAP server with port.
- _java.naming.ldap.attributes.binary_: is the binary unique identifier that will be used in subsequent logins to identify the user.
- _java.naming.security.authentication_: how to authenticate to the LDAP server.
- _java.naming.security.principal_: contains the username of the user that will be used to query LDAP.
- _java.naming.security.credentials_: contains the password of the user that will be used to query LDAP.
- _java.naming.referral_: whether to follow or ignore an alternate location in which an LDAP Request may be processed.

After configuring LDAP and creating your cluster you can log into your Hopsworks cluster and edit the LDAP _attributes to field names_ to match
your server. By default all _attributes to field names_ are set to the values in [OpenLDAP](https://www.openldap.org/). 
See [Configure LDAP](../../../user_guides/projects/auth/ldap.md) on how to edit the LDAP default configurations.


!!!Note

     A default admin user that can log in with **username** and **password** will be created for the user that is creating the cluster. 
     This user can be removed after making sure users can log in using LDAP. 