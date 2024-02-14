# Best practices

Below is a set of recommendations and code snippets to help our users follow best practices when it comes to integrating a data validation step in your feature engineering pipelines. Rather than being prescriptive, we want to showcase how the API and configuration options can help adapt validation to your use-case.

## Development

Data validation is generally considered to be a production-only feature and as such is often only setup once a project has reached the end of the development phase. At Hopsworks, we think there is a lot of value in setting up validation during early development. That's why we made it quick to get started and ensured that by default data validation is never an obstacle to inserting data.

### Validate Early

As often with data validation, the best piece of advice is to set it up early in your development process. Use this phase to build a history you can then use when it becomes time to set quality requirements for a project in production. We made a code snippet to help you get started quickly:

```python3
# Load sample data. Replace it with your own!
my_data_df = pd.read_csv("https://repo.hops.works/master/hopsworks-tutorials/data/card_fraud_data/credit_cards.csv")

# Use Great Expectation profiler (ignore deprecation warning)
expectation_suite_profiled, validation_report = ge.from_pandas(my_data_df).profile(profiler=ge.profile.BasicSuiteBuilderProfiler)

# Create a Feature Group on hopsworks with an expectation suite attached. Don't forget to change the primary key!
my_validated_data_fg = fs.get_or_create_feature_group(
    name="my_validated_data_fg",
    version=1,
    description="My data",
    primary_key=['cc_num'],
    expectation_suite=expectation_suite_profiled)
```

Any data you insert in the Feature Group from now will be validated and a report will be uploaded to Hopsworks.

```python3
# Insert and validate your data
insert_job, validation_report = my_validated_data_fg.insert(my_data_df)
```

Great Expectations profiler can inspect your data to build a standard Expectation Suite. You can attach this Expectation Suite directly when creating your Feature Group to make sure every piece of data finding its way in Hopsworks gets validated. Hopsworks will default to its `"ALWAYS"` ingestion policy, meaning data are ingested whether validation succeeds or not. This way data validation is not a barrier, just a monitoring tool.

### Identify Unreliable Features

Once you setup data validation, every insertion will upload a validation report to Hopsworks. Identifying Features which often have null values or wild statistical variations can help detecting unreliable Features that need refinements or should be avoided. Here are a few expectations you might find useful:

- `expect_column_values_to_not_be_null`
- `expect_column_(min/max/mean/stdev)_to_be_between`
- `expect_column_values_to_be_unique`

### Get the stakeholders involved

Hopsworks UI helps involve every project stakeholder by enabling both setting and monitoring of data quality requirements. No coding skills needed! You can monitor data quality requirements by checking out the validation reports and results on the Feature Group page.

If you need to set or edit the existing requirements, you can go on the Feature Group edit page. The Expectation suite section allows you to edit individual expectations and set success parameters that match ever changing business requirements.

## Production

Models in production require high-quality data to make accurate predictions for your customers. Hopsworks can use your Expectation Suite as a gatekeeper to make it simple to prevent low-quality data to make its way into production. Below are some simple tips and snippets to make the most of your data validation when your project is ready to enter its production phase.

### Be Strict in Production

Whether you use an existing or create a new (recommended) Feature Group for production, we recommend you set the validation ingestion policy of your Expectation Suite to `"STRICT"`.

```python3
fg_prod.save_expectation_suite(
    my_suite,
    validation_ingestion_policy="STRICT")
```

In this setup, Hopsworks will abort inserting a DataFrame that does not successfully fullfill all expectations in the attached Expectation Suite. This ensures data quality standards are upheld for every insertion and provide downstream users with strong guarantees.

### Avoid Data Loss on materialization jobs

Aborting insertions of DataFrames which do not satisfy the data quality standards can lead to data loss in your materialization job. To avoid such loss we recommend creating a duplicate Feature Group with the same Expectation Suite in `"ALWAYS"` mode which will hold the rejected data.

```python3
job, report = fg_prod.insert(df)

if report["success"] is False:
    job, report = fg_rejected.insert(df)
```

### Take Advantage of the Validation History

You can easily retrieve the validation history of a specific expectation to export it to your favourite visualisation tool. You can filter on time and on whether insertion was successful or not

```python3
validation_history = fg.get_validation_history(
    expectation_id=my_id,
    filters=["REJECTED", "UNKNOWN"],
    ge_type=False
)

timeseries = pd.DataFrame(
    {
        "observed_value": [res.result["observed_value"] for res in validation_histoy]],
        "validation_time": [res.validation_time for res in validation_history]
    }
)

# export to your preferred Dashboard
```

### Setup Alerts

While checking your feature engineering pipeline executed properly in the morning can be good enough in the development phase, it won't make the cut for demanding production use-cases. In Hopsworks, you can setup alerts if ingestion fails or succeeds.

First you will need to configure your preferred communication endpoint: slack, email or pagerduty. Check out [this page](../../../admin/alert.md) for more information on how to set it up. A typical use-case would be to add an alert on ingestion success to a Feature Group you created to hold data that failed validation. Here is a quick walkthrough:

1. Go the Feature Group page in the UI
2. Scroll down and click on the `Add an alert` button.
3. Choose the trigger, receiver and severity and click save.

## Conclusion

Hopsworks completes Great Expectation by automatically running the validation, persisting the reports along your data and allowing you to monitor data quality in its UI. How you decide to make use of these tools depends on your application and requirements. Whether in development or in production, real-time or batch, we think there is configuration that will work for your team. Check out our [quick hands-on tutorial](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb) to start applying what you learned so far.
