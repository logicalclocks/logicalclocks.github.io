HSFS supports monitoring, validation, and alerting for features:

 - transparently compute statistics over features on writing to a feature group;
 - validation of data written to feature groups using Great Expectations
 - alerting users when there was a problem writing or update features. 

### Statistics

When you create a Feature Group in HSFS, you can configure it to compute statistics over the features inserted into the fFeature Group by setting the `statistics_config` dict parameter, see [Feature Group Statistics](../../../../user_guides/fs/feature_group/statistics/) for details. Every time you write to the Feature Group, new statistics will be computed over all of the data in the Feature Group.


### Data Validation

You can define expectation suites in Great Expectations and assoicate them with feature groups. When you write to a feature group, the expectations are executed, then you can define a policy on the feature group for what to do if any expectation fails.

<img src="../../../../assets/images/concepts/fs/fg-expectations.svg">



### Alerting

HSFS also supports alerts, that can be triggered when there are problems in your feature pipelines, for example, when a write fails due to an error or a failed expectation. You can send alerts to different alerting endpoints, such as email or Slack, that can be configured in the Hopsworks UI. For example, you can send a slack message if features being written to a feature group are missing some input data.
