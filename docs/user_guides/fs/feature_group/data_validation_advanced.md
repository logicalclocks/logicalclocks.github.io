# Advanced Data Validation Options and Best Practices

The introduction to data validation guide can be found [here](data_validation.md). The notebook example to get started with Data Validation in Hopsworks can be found [here](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb).

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

You can do it in the UI in the Expectation section of the Feature Group edit page. Simply tick or untick the enabled checkbox. This will be used as the default option but can be overriden via the API.

#### In the python client

To disable data validation until further notice in the API, you can update the `run_validation` field of the expectation suite. If your suite is registered with Hopsworks, this will persist the change to the server.

```python3
fg.expectation_suite.run_validation = False
```

If you wish to override the default behaviour of the suite when inserting data in the Feature Group, you can do so via the `validate_options` kwarg. The example below will enable validation for this insertion only.

```python3
fg.insert(df_to_validate, validation_options={"run_validation" : True})
```

We recommend to avoid using this option in scheduled job as it silently changes the expected behaviour that is displayed in the UI and prevents changes to the default behaviour to change the behaviour of the job.

### Edit Expectations

The one constant in life is change. If you need to add, remove or edit an expectation you can do it both in the UI or via the python client. Note that changing the expectation type or its corresponding feature will throw an error in order to preserve a meaningful validation history.

#### In Hopworks UI

Go to the Feature Group edit page, in the expectation section. You can click on the expectation you want to edit and edit the json configuration. Check out Great Expectations documentation if you need more information on a particular expectation.

#### In Hopsworks Python Client

There are several way to edit an Expectation in the python client. You can use Great Expectations API or directly go through Hopsworks. In the latter case, if you want to edit or remove an expectation, you will need the Hopsworks expectation ID. It can be found in the UI or in the meta field of an expectation. Note that you must have inserted data in the FG and attached the expectation suite to enable the Expectation API.

Get an expectation with a given id:

```python3
my_expectation = fg.expectation_suite.get_expectation(
    expectation_id = my_expectation_id
)
```

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

### Save Validation Reports

When running validation using Great Expectations, a validation report is generated containing all validation results for the different expectations. Each result provides information about whether the provided DataFrame conforms to the corresponding expectation. These reports can be stored in Hopsworks to save a validation history for the data written to a particular Feature Group.

The boilerplate of uploading report on insertion is taken care of by hopsworks, however for custom pipelines we provide an alternative method in the python client. The UI does not currently support upload of a validation report.

#### In Hopsworks Python Client

```python3
fg.save_validation_report(ge_report)
```

### Monitor and Fetch Validation Reports

A summary of uploaded reports will then be available via an API call or in the Hopsworks UI enabling easy monitoring. For in-depth analysis, it is possible to download the complete report from the UI.

#### In Hopsworks UI

Open the Feature Group overview page and go to the Expectations section. One tab allows you to check the report history with general information, while the other tab allows you to explore a summary of the result for individual expectations.

#### In Hopsworks Python Client

```python3
# convenience method for rapid development
ge_latest_report = fg.get_latest_validation_report()
# fetching the latest summary prints a link to the UI
# where you can download full report if summary is insufficient

# or load multiple reports
validation_history = fg.get_validation_reports()
```

### Validate your data manually

While Hopsworks provides automatic validation on insertion logic, we recognise that some use cases may require a more fine-grained control over the validation process. Therefore, Feature Group objects offers a convenience wrapper around Great Expectations to manually trigger validation using the registered Expectation Suite.

#### In the UI

You can validate data already ingested in the Feature Group by going to the Feature Group overview page. In the top right corner is a button to trigger a validation. The button will lauch a job which will read the Feature Group data, run validation and persist the associated report.

#### In the python client

```python3
ge_report = fg.validate(df, ingestion_result="EXPERIMENT")

# set the save_report parameter to False to skip uploading the report to Hopsworks
# ge_report = fg.validate(df, save_report=False)
```

If you want to apply validation to the data already in the Feature Group you can call the `.validate` without providing data. It will read the data in the Feature Group.

```python3
report = fg.validate()
```

As validation objects returned by Hopsworks are native Great Expectation objects you can run validation using the usual Great Expectations syntax:

```python3
ge_df = ge.from_pandas(df, expectation_suite=fg.get_expectation_suite())
ge_report = ge_df.validate()
```

Note that you should always use an expectation suite that has been saved to Hopsworks if you intend to upload the associated validation report.
