# Configure Alerts

## Introduction
Alerts are sent from Hopsworks using Prometheus' 
[Alert manager](https://prometheus.io/docs/alerting/latest/alertmanager/).
In order to send alerts we first need to configure the _Alert manager_.

## Prerequisites
Administrator account on a Hopsworks cluster.

### Step 1: Go to alerts configuration
To configure the _Alert manager_ click on your name in the top right corner of the navigation bar and choose
Cluster Settings from the dropdown menu. In the Cluster Settings' Alerts tab you can configure the alert 
manager to send alerts via email, slack or pagerduty.

<figure>
  <img src="../../../assets/images/alerts/configure-alerts.png" alt="Configure alerts"/>
  <figcaption>Configure alerts</figcaption>
</figure>

### Step 2: Configure Email Alerts
To send alerts via email you need to configure an SMTP server. Click on the _Configure_ 
button on the left side of the **email** row and fill out the form that pops up.

<figure>
  <img src="../../../assets/images/alerts/smtp-config.png" alt="Configure Email Alerts"/>
  <figcaption>Configure Email Alerts</figcaption>
</figure>

- _Default from_: the address used as sender in the alert email.
- _SMTP smarthost_: the Simple Mail Transfer Protocol (SMTP) host through which emails are sent.
- _Default hostname (optional)_: hostname to identify to the SMTP server.
- _Authentication method_: how to authenticate to the SMTP server.
  CRAM-MD5, LOGIN or PLAIN.

Optionally cluster wide Email alert receivers can be added in _Default receiver emails_.
These receivers will be available to all users when they create event triggered [alerts](../../../user_guides/fs/feature_group/data_validation_best_practices#setup-alerts).

### Step 3: Configure Slack Alerts
Alerts can also be sent via Slack messages. To be able to send Slack messages you first need to configure
a Slack webhook. Click on the _Configure_ button on the left side of the **slack** row and past in your
[Slack webhook](https://api.slack.com/messaging/webhooks) in _Webhook_.

<figure>
  <img src="../../../assets/images/alerts/slack-config.png" alt="Configure slack Alerts"/>
  <figcaption>Configure slack Alerts</figcaption>
</figure>

Optionally cluster wide Slack alert receivers can be added in _Slack channel/user_.
These receivers will be available to all users when they create event triggered [alerts](../../../user_guides/fs/feature_group/data_validation_best_practices/#setup-alerts).

### Step 4: Configure Pagerduty Alerts
Pagerduty is another way you can send alerts from Hopsworks. Click on the _Configure_ button on the left side of 
the **pagerduty** row and fill out the form that pops up. 

<figure>
  <img src="../../../assets/images/alerts/pagerduty-config.png" alt="Configure Pagerduty Alerts"/>
  <figcaption>Configure Pagerduty Alerts</figcaption>
</figure>

Fill in Pagerduty URL: the URL to send API requests to.

Optionally cluster wide Pagerduty alert receivers can be added in _Service key/Routing key_.
By first choosing the PagerDuty integration type:

- _global event routing (routing_key)_: when using PagerDuty integration type `Events API v2`.
- _service (service_key)_: when using PagerDuty integration type `Prometheus`.

Then adding the Service key/Routing key of the receiver(s). PagerDuty provides 
[documentation](https://www.pagerduty.com/docs/guides/prometheus-integration-guide/) on how to integrate with 
Prometheus' Alert manager.

### Step 5: Configure Webhook Alerts

You can also use webhooks to send alerts. A Webhook Alert is sent as an HTTP POST command with a JSON-encoded parameter payload.
Click on the _Configure_ button on the left side of the **webhook** row and fill out the form that pops up. 

<figure>
  <img src="../../../assets/images/alerts/webhook-config.png" alt="Configure Webhook Alerts"/>
  <figcaption>Configure Webhook Alerts</figcaption>
</figure>

Fill in the unique URL of your Webhook: the endpoint to send HTTP POST requests to.

A global receiver is created when a webhook is configured and can be used by any project in the cluster. 

### Step 6: Advanced configuration
If you are familiar with Prometheus' [Alert manager](https://prometheus.io/docs/alerting/latest/alertmanager/) 
you can also configure alerts by editing the _yaml/json_ file directly by going to the advaced page and clicking the edit button.
 
The advanced page shows the configuration currently loaded on the alert manager. After editing the configuration it takes some time to propagate changes to the alertmanager. 

The reload button can be used to validate the changes made to the configuration. 
It will try to load the new configuration to the alertmanager and show any errors that might prevent the configuration from being loaded. 

<figure>
  <img src="../../../assets/images/alerts/advanced-config.png" alt="Advanced configuration"/>
  <figcaption>Advanced configuration</figcaption>
</figure>

!!!warning

    If you make any changes to the configuration ensure that the changes are valid by reloading the configuration until the changes are loaded and visible in the advanced page. 

_Example:_ Adding the yaml snippet shown below in the global section of the alert manager configuration will
have the same effect as creating the SMTP configuration as shown in [section 1](#1-email-alerts) above.

```yaml
global:
    smtp_smarthost: smtp.gmail.com:587
    smtp_from: hopsworks@gmail.com
    smtp_auth_username: hopsworks@gmail.com
    smtp_auth_password: XXXXXXXXX
    smtp_auth_identity: hopsworks@gmail.com
 ...
```

To test the alerts by creating triggers from Jobs and Feature group validations see [Alerts](../../../user_guides/fs/feature_group/data_validation_best_practices/#setup-alerts).

The yaml syntax in the UI is slightly different in that it does not allow double quotes (it will ignore the values but give no error). 
Below is an example configuration, that can be used in the UI, with both email and slack receivers configured for system alerts.

```yaml
global:
    smtp_smarthost: smtp.gmail.com:587
    smtp_from: hopsworks@gmail.com
    smtp_auth_username: hopsworks@gmail.com
    smtp_auth_password: XXXXXXXXX
    smtp_auth_identity: hopsworks@gmail.com
    resolveTimeout: 5m
templates:
  - /srv/hops/alertmanager/alertmanager-0.17.0.linux-amd64/template/*.tmpl
route:
  receiver: default
  routes:
    - receiver: email
      continue: true
      match:
        type: system-alert
    - receiver: slack
      continue: true
      match:
        type: system-alert
  groupBy:
    - alertname
  groupWait: 10s
  groupInterval: 10s
receivers:
  - name: default
  - name: email
    emailConfigs:
      - to: someone@logicalclocks.com
        from: hopsworks@logicalclocks.com
        smarthost: mail.hello.com
        text: >-
          summary: {{ .CommonAnnotations.summary }} description: {{
          .CommonAnnotations.description }}
  - name: slack
    slackConfigs:
      - apiUrl: >-
          https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
        channel: '#general'
        text: >-
          <!channel> summary: {{ .Annotations.summary }} description: {{
          .Annotations.description }}
```
