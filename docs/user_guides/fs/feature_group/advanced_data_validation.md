# Advanced Data Validation Options and Best Practices

The introduction to data vaildation guide can be found [here](data_validation.md). The notebook example to get started with Data Validation in Hopsworks can be found [here](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb).

## Data Validation Configuration Options in Hopsworks

### Validation Ingestion Policy

Depending on your use case you can setup data validation as a monitoring or gatekeeping tool when trying to insert new data in your Feature Group. Switch behaviour by using the `validation_ingestion_policy` kwarg:

- `"ALWAYS"` is the default option and will attempt to insert the data regardless of the validation result. Hassle free, it is ideal to monitor data ingestion in a development setup.
- `"STRICT"` is the best option for production ready projects. This will prevent insertion of DataFrames which do not pass all data quality requirements. Ideal to avoid "garbage-in, garbage-out" scenarios, at the price of a potential loss of data. Check out the best practice section for more on that.

#### In the UI

Go to the Feature Group edit page, in the Expectation section you can choose between the options above.

#### In the python client

```python3
fg.expectation_suite.validation_ingestion_policy = "ALWAYS" # "STRICT"
```

If your suite is registered with Hopsworks, it will persist the change to the server.

### Disable Data Validation

Should you wish to do so, you can disable data validation on a punctual basis or until further notice.

#### In the UI

You can do it in the UI in the Expectation section of the Feature Group edit page. Simply tick or untick the enabled checkbox.

#### In the python client

```python3
fg.expectation_suite.run_validation = False
```

If your suite is registered with Hopsworks, it will persist the change to the server.

### Edit Expectations

The one constant in life is change. If you need to add, remove or edit an expectation you can do it both in the UI or via the python client. Note that changing the expectation type or its corresponding feature will throw an error in order to preserve a meaningful validation history.

#### In Hopworks UI

Go to the Feature Group edit page, in the expectation section. You can click on the expectation you want to edit and edit the json configuration. Check out Great Expectations documentation if you need more information on a particular expectation.

### In Hopsworks Python Client

There are several way to edit an Expectation in the python client. You can use Great Expectations API or directly go through Hopsworks. In the latter case, if you want to edit or remove an expectation, you will need the Hopsworks expectation ID. It can be found in the UI or

Add a new expectation:

```python3
new_expectation = ge.core.ExpectationConfiguration(
    expectation_type="expect_column_values_not_to_be_null",
    kwargs={
        "mostly": 1
    }
)

fg.expectation_suite.add_expectation(new_expectation)
```

Edit expectation kwargs of an existing expectation :

```python3
existing_expectation = fg.expectation_suite.get_expectation(
    expectation_id=existing_expectation_id
)

existing_expectation.kwargs["mostly"] = 0.95

fg.expectation_suite.replace_expectation(existing_expectation)
```

Remove an expectation:

```python3
fg.expectation_suite.remove_expectation(
    expectation_id=id_of_expectation_to_delete
)
```

If you want to deal only with the Great Expectation API:

```python3
my_suite = fg.get_expectation_suite()

my_suite.add_expectation(new_expectation)

fg.save_expectation_suite(my_suite)
```

## Best Practices

Below is a set of recommendations and code snippets to help our users follow best practices when it comes to integrating a data validation step in your feature engineering pipelines. Rather than being prescriptive, we want to showcase how the API and configuration options can help adapt validation to your use-case.

### Development

Data validation is generally considered to be a production-only feature and as such is often only setup once a project has reached the end of the development phase. At Hopsworks, we think there is a lot of value in setting up validation during early development. That's why we made it quick to get started and ensured that by default data validation is never an obstacle to inserting data.

#### Validate Early

As often with data validation, the best piece of advice is to set it up early in your development process. Use this phase to build a history you can then use when it becomes time to set quality requirements for a project in production. We made a code snippet to help you get started quickly:

```
Add quickstart from tutorial
```

Great Expectations profiler can inspect your data to build a standard Expectation Suite. You can attach this Expectation Suite directly when creating your Feature Group to make sure every piece of data finding its way in Hopsworks gets validated. Hopsworks will default to its `"ALWAYS"` ingestion policy, meaning data are ingested whether validation succeeds or not. This way data validation is not a barrier, just a monitoring tool.

#### Identify Unreliable Features

Once you setup data validation, every insertion will upload a validation report to Hopsworks. Identifying Features which often have null values or wild statistical variations can help detecting unreliable Features that need refinements or should be avoided. Here are a few expectations you might find useful:

- `expect_column_values_to_not_be_null`
- `expect_column_(min/max/mean/stdev)_to_be_between`
- `expect_column_values_to_be_unique`

#### Get the stakeholders involved

Hopsworks UI helps involve every project stakeholder by enabling both setting and monitoring of data quality requirements. No coding skills needed! You can monitor data quality requirements by checkint out the validation reports and results on the Feature Group page.

If you need to set or edit the existing requirements, you can go on the Feature Group edit page. The Expectation suite section allows you to edit individual expectations and set success parameters that match ever changing business requirements.

### Production

Models in production require high-quality data to make accurate predictions for your customers. Hopsworks can use your Expectation Suite as a gatekeeper to make it simple to prevent low-quality data to make its way into production. Below are some simple tips and snippets to make the most of your data validation when your project is ready to enter its production phase.

#### Be Strict in Production

Whether you use an existing or create a new (recommended) Feature Group for production, we recommend you set the validation ingestion policy of your Expectation Suite to `"STRICT"`.

```python3
fg_prod.save_expectation_suite(
    my_suite,
    validation_ingestion_policy="STRICT")
```

In this setup, Hopsworks will abort inserting a DataFrame that does not successfully fullfill all expectations in the attached Expectation Suite. This ensures data quality standards are upheld for every insertion and provide downstream users with strong guarantees.

#### Avoid Data Loss on Backfill jobs

Aborting insertions of DataFrames which do not satisfy the data quality standards can lead to data loss in your backfill job. To avoid such loss we recommend creating a duplicate Feature Group with the same Expectation Suite in `"ALWAYS"` mode which will hold the rejected data.

```python3
job, report = fg_prod.insert(df)

if report["success"] is False:
    job, report = fg_rejected.insert(df)
```

#### Take Advantage of the Validation History

You can easily retrieve the validation history of a specific expectation to export it to your favourite visualisation tool. You can filter on time and on whether insertion was successful or not

```python3
validation_history = fg.get_validation_history(
    expectation_id=my_id,
    ingested=true,
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

#### Setup Alerts

While checking your feature engineering pipeline executed properly in the morning can be good enough in the development phase, it won't make the cut for demanding production use-cases. In Hopsworks, you can setup alerts if validation fails.

First you will need to configure your preferred communication endpoint: slack, email or pagerduty. Check out [this page](../../../admin/alert.md) for more information on how to set it up. You can then set an alert on data ingestion success in the Feature Group holding rejected data for example.

## Conclusion

Hopsworks completes Great Expectation by automatically running the validation, persisting the reports along your data and allowing you to monitor data quality in its UI. How you decide to make use of these tools depends on your application and requirements. Whether in development or in production, real-time or batch, we think there is configuration that will work for your team. Check out our [quick hands-on tutorial](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb) to start applying what you learned so far.

### Step 4: Integrating Great Expectations with Hopsworks

Hopsworks can automatically run your expectation suite whenever you are inserting new data in your Feature Group. Your suite and reports are saved as part of your Feature Group with your data.

#### Attach an Expectation Suite to a Feature Group

The first step is to attach the GE expectation suite to your Feature Group. It enables both persistence of the expectation suite to the Hopsworks backend and automatic validation on insertion.

```python3
fg.save_expectation_suite(expectation_suite)

# or directly when creating your Feature Group

fg = fs.create_feature_group(
    ...,
    expectation_suite=expectation_suite
)
```

### TODO validation on insertion.

### TODO monitoring

### TODO Extra boring stuff about using the API in other ways

This suite can then easily be retrieved during a different session or deleted whenever you are working with this Feature Group by calling:

```python3
ge_expectation_suite = fg.get_expectation_suite()
# or delete with
fg.delete_expectation_suite()
```

#### Validate your data

As validation objects returned by Hopsworks are native Great Expectation objects you can run validation using the usual Great Expectations syntax:

```python3
ge_df = ge.from_pandas(df, expectation_suite=fg.get_expectation_suite())
ge_report = ge_df.validate()
```

Note that you should always use an expectation suite that has been saved to Hopsworks if you intend to upload the associated validation report. You can use a convenience wrapper method provided by Hopsworks to validate using the attached suite:

```python3
ge_report = fg.validate(df)
# set the save_report parameter to False to skip uploading the report to Hopsworks
# ge_report = fg.validate(df, save_report=False)
```

This will run the validation using the expectation suite attached to this Feature Group and raise an exception if no attached suite is found.

#### Save Validation Reports

When running validation using Great Expectations, a validation report is generated containing all validation results for the different expectations. Each result provides information about whether the provided DataFrame conforms to the corresponding expectation. These reports can be stored in Hopsworks to save a validation history for the data written to a particular Feature Group.

```python3
fg.save_validation_report(ge_report)
```

A summary of these reports will then be available via an API call or in the Hopsworks UI enabling easy monitoring. For in-depth analysis, it is possible to download the complete report from the UI.

```python3
# convenience method for rapid development
ge_latest_report = fg.get_latest_validation_report()
# fetching the latest summary prints a link to the UI
# where you can download full report if summary is insufficient

# or load multiple reports
validation_history = fg.get_validation_reports()
```

### Step 3: Data validation in development or production environments

Depending on your context, you might want to use (or not use) data validation in different ways. Hopsworks aims to provide both a smooth development experience as well as an easy and robust path to a production pipeline. This is achieved through two key mechanisms:

- Validation On Insertion
- Monitoring Or Gatekeeping

#### Validation On Insertion

By default, attaching an expectation suite to a Feature Group enables automatic validation on insertion. Meaning calling `fg.insert` after attaching an expectation suite to a Feature Group will perform validation under the hood (on the client) and upload the validation report. This approach enables you, the developer, to write cleaner more maintainable code while Hopsworks manages the operational problem of storing your data validation history alongside the data itself.

In your expectation suite script:

```python3
expectation_suite = ge.core.ExpectationSuite(
    expectation_suite_name="validate_on_insert_suite"
)

expectation_suite.add_expectation(
    ge.core.ExpectationConfiguration(
        expectation_type="expect_column_minimum_value_to_be_between",
        kwargs={
            "column": "foo_id",
            "min_value": 0,
            "max_value": 1
        }
    )
)

# run_validation kwarg defaults to True
fg.save_expectation_suite(expectation_suite, run_validation=True)
```

In your insertion script:

```python3
# With Hopsworks: clean and simple
fg.insert(df)
```

```python3
# Without Hopsworks: lots of boiler plate code for managing

# validation reports as JSON objects and files.
expectation_suite_path = Path("./my_expectation_suite.json")
report_path = Path("./my_validation_report.json")

with expectation_suite_path.open("r") as f:
    expectation_suite = json.load(expectation_suite_path)

ge_df = ge.from_pandas(df, expectation_suite=expectation_suite)
report = ge_df.validate()

with report_path.open("w") as f:
    json.dumps(f, report.to_json())
```

For your convenience, Hopsworks also provides a link to the UI with a summary of the latest validation.

There is a variety of use cases where performing data validation on insertion is not desirable, e.g., when rapid prototyping or when backfilling a large amount of pre-validated data for a time-sensitive project deadline. In these cases, you can skip validation for `fg.insert` using:

```python3
# skip validation for a single run
fg.insert(df, validation_options={"run_validation": False})

# or skip validation until specified otherwise
fg.save_expectation_suite(fg.get_expectation_suite(), run_validation=False)
```

### Step 4: Monitoring or Gatekeeping

Data validation steps in a feature engineering pipeline has two complementary use cases, monitoring and gatekeeping. In the first case, you use validation primarily as a reporting tool. The aim is to gather metrics on the ingested data and create a history that can inform the user about the evolution of certain trends in the feature data. This use case is typical in a development setup where the data is still being characterized and reliable quality is not yet required. Setting it up during development also enables an easier transition towards a production setup. Indeed, it remains useful in production to detect feature drift and log information about incoming data.

In contrast, a production setup often requires additional protection to prevent bad quality data finding its way into the Feature Group. A typical example is preventing the Online Feature Store returning a feature vector containing NaN values that could lead to problems in inference pipelines. In such cases data validation can be used as a gatekeeper to prevent erroneous data from finding its way into an Online Feature Store.

Hopsworks is focused on making the transition from development to production as seamless as possible. To switch between these two behaviours you can simply use the `validation_ingestion_policy` parameter. By default, expectation suites are attached to Feature Groups as a monitoring tool. This default choice is made as it corresponds to development setup and avoids any loss of data on insertion.

```python3
fg.save_expectation_suite(expectation_suite)
# defaults to the monitoring behaviour
fg.save_expectation_suite(expectation_suite, validation_ingestion_policy="ALWAYS")
```

When you want to switch from development to production, you can enable gatekeeping by setting:

```python3
fg.save_expectation_suite(fg.get_expectation_suite(), validation_ingestion_policy="STRICT")
```
