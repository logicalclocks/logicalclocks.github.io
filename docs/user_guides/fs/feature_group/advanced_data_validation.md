# Advanced Data Validation Options and Best Practices

The introduction to data vaildation guide can be found [here](data_validation.md). The notebook example to get started with Data Validation in Hopsworks can be found [here](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb)

##

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
