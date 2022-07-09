# Configure your hopsworks cluster to use OAuth2 for user management.
 
If you want to use your organization's OAuth 2.0 identity provider to manage users in your hopsworks cluster this document
will guide you through the necessary steps to register your identity provider in Hopsworks.ai.
 
Before registering your identity provider in Hopsworks you need to create a client application in your identity provider and
acquire a _client id_ and a _client secret_. Examples on how to create a client using [Okta](https://www.okta.com/)
and [Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory) identity providers can be found
[here](../../../../admin/oauth2/create-okta-client/) and [here](../../../../admin/oauth2/create-azure-client/) respectively.
 
In the User management step of cluster creation ([AWS](../../../aws/cluster_creation/#step-11-user-management-selection),
[Azure](../../../azure/cluster_creation/#step-10-user-management-selection)) you can choose which user management system to use. Select
_OAuth2 (OpenId)_ from the dropdown and configure your identity provider.
 
<p align="center">
 <figure>
   <a  href="../../../../assets/images/setup_installation/managed/common/sso/oauth.png">
     <img style="border: 1px solid #000" src="../../../../assets/images/setup_installation/managed/common/sso/oauth.png" alt="Setup OAuth">
   </a>
   <figcaption>Setup OAuth</figcaption>
 </figure>
</p>
 
Register your identity provider by setting the following fields:

- _Create Administrator password user_: if checked an administrator that can log in to the hopsworks cluster, with email and password,
will be created for the user creating the cluster. If **Not** checked a group mapping that maps at least one group in the identity provider to _HOPS_ADMIN_ is required. 
- _ClientId_: the client id generated when registering hopsworks in your identity provider.
- _Client Secret_: the client secret generated when registering hopsworks in your identity provider.
- _Provider URI_: is the base uri of the identity provider (URI should contain scheme http:// or https://).
- _Provider Name_: a unique name to identify the identity provider in your hopsworks cluster.
                  This name will be used in the login page as an alternative login method if _Provider DisplayName_ is not set.
 
 
Optionally you can also set:
 
- _Provider DisplayName_: the name to display for the alternative login method (if not set _Provider Name_ will be used)
- _Provider Logo URI_: a logo URL to an image. The logo will be shown on the login page with the provider name.
- _Code Challenge Method_: if your identity provider requires a code challenge for authorization request check the code challenge check box.
                        This will allow you to choose a code challenge method that can be either plain or S256.
- _Group Mapping_: will allow you to map groups in your identity provider to groups in hopsworks.
                  You can choose to map all users to HOPS_USER or HOPS_ADMIN. Alternatively you can add mappings as in the example below.
                  ```
                  IT->HOPS_ADMIN;DATA_SCIENCE->HOPS_USER
                  ```
                  This will map users in the IT group in your identity provider to HOPS_ADMIN and users in the DATA_SCIENCE group to HOPS_USER.
- _Verify Email_: if checked only users with verified email address (in the identity provider) can log in to Hopsworks.
- _Activate user_: if not checked an administrator in hopsworks needs to activate users before they can login.
- _Need consent_: if checked, users will be asked for consent when logging in for the first time.
- _Disable registration_: if unchecked users will have the possibility to create accounts in the hopsworks cluster using user name and password instead of OAuth.
- _Provider Metadata Endpoint Supported_: if your provider defines a discovery mechanism, called OpenID Connect Discovery,
                                         where it publishes its metadata at a well-known URL, typically
```
https://server.com/.well-known/openid-configuration
```
you can check this and the metadata will be discovered by hopsworks.
If your provider does not publish its metadata you need to supply these values manually.
 
<p align="center">
 <figure>
   <a  href="../../../../assets/images/setup_installation/managed/common/sso/provider-metadata.png">
     <img style="border: 1px solid #000" src="../../../../assets/images/setup_installation/managed/common/sso/provider-metadata.png" alt="provider metadata">
   </a>
   <figcaption>Setup Provider</figcaption>
 </figure>
</p>
 
- _Authorization Endpoint_: the authorization endpoint of your identity provider, typically
```
https://server.com/oauth2/authorize
```
- _End Session Endpoint_: the logout endpoint of your identity provider, typically
```
https://server.com/oauth2/logout
```
- _Token Endpoint_: the token endpoint of your identity provider, typically
```
https://server.com/oauth2/token
```
- _UserInfo Endpoint_: the user info endpoint of your identity provider, typically
```
https://server.com/oauth2/userinfo
```
- _JWKS URI_: the JSON Web Key Set endpoint of your identity provider, typically
```
https://server.com/oauth2/keys
```
 
After configuring OAuth2 you can click on **Next** to configure the rest of your cluster.

You can also configure OAuth2 once you have created a Hopsworks cluster. For instructions on how to configure OAUth2 on Hopsworks see 
[Authentication Methods](../../../../admin/oauth2/create-client/).
