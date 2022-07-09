# Data Validation

## Introduction

Clean, high quality feature data is of paramount importance to being able to train and serve high quality models. Hopsworks offers integration with [Great Expectations](https://greatexpectations.io/) to enable a smooth data validation workflow. This guide is designed to help you integrate a data validation step when inserting new DataFrames into a Feature Group. Note that validation is performed inline as part of your feature pipeline (on the client machine) - it is not executed by Hopsworks after writing features.

## UI

### Step 1: Create or Edit a Feature Group

You can attach at most one expectation suite to a Feature Group. It can be done on creation or at a later point in time. Data validation is an optional step and is not required to write to a Feature Group. You can find out more information about creating a Feature Group [here](create.md).

Click on the Feature Group section in the navigation menu. Click on `New Feature Group` if you want to create a brand new Feature Group. If you already created your Feature Group you can use the search bar to find and open it. Select `edit` at the top or scroll to Expectations section and click on `Edit Expectations`.

### Step 2: Edit General Expectation Suite Settings

Scroll to the Expectation Suite section. You can pick a name for your suite as well as two general options.

- enabled checkbox controls whether validation will be run automatically before writing a DataFrame to a Feature Group. Note that validation is executed by the client.
- 'ALWAYS' vs. 'STRICT' mode. This option controls what happens after validation. Hopsworks defaults to 'ALWAYS', where data is written to the Feature Group regardless of the validation result. This means that even if expectations are failing or throw an exception, Hopsworks will attempt to insert the data into the Feature Group. In 'STRICT' mode, Hopsworks will only write data to the Feature Group if each individual expectation has been successful.

### Step 3: Add new expectations

By clicking on `Add another expectation` one can choose an expectation type from a dropdown menu. Currently, only the built-in expectations from the Great Expectations framework are supported. For user-defined expectations, please use the Rest API or python client. All default kwargs associated to the selected expectation type are populated as a json below the dropdown menu. Edit the json and click the tick button to save the change locally.

!!! info
    Click the `Save and Create New Version` button to persist your changes!

### Step 4: Save new data to a Feature Group

Use the python client to write a DataFrame to the Feature Group. Note that if an expectation suite is enabled for a Feature Group, calling the `insert` method will run validation and default to uploading the corresponding validation report to Hopsworks. The report is uploaded even if validation fails and 'STRICT' mode is selected.

### Step 5: Check Validation Results Summary

Hopsworks shows a visual summary of validation reports. To check it out, go to your Feature Group overview and scroll to the expectation section. Click on the `Validation Results` tab and check that all went according to plan. Each row corresponds to an expectation in the suite. Features can have several corresponding expectations and the same type of expectation can be applied to different features.

You can navigate to older reports using the dropdown menu. Should you need more than the information displayed in the UI for e.g., debugging, the full report can be downloaded by clicking on the corresponding button.

### Step 6: Check Validation History

The `Validation Reports` tab in the Expectations secion displays a brief history of recent validations. Each row corresponds to a validation report, with some summary information about the success of the validation step. You can download the full report by clicking the download icon button that appears at the end of the row.

## Code 

### Step 1: Setup

In order to define and validate an expectation when writing to a Feature Group, you will need:
- A pandas DataFrame to validate
- A Hopsworks project
- great_expectations installed in your client

#### DataFrame to validate

Here is a small DataFrame to validate. You could also create your own Pandas DataFrame using your own data.

```python3
import pandas as pd

df = pd.DataFrame({
    "foo_id": [1, 2, 3, 4, 5], 
    "bar_name": ["alice", "bob", "carl", "dylan", "e"]
})
```

#### Create an Expectation Suite

Create (or import an existing) expectation suite using the Great Expectations library.

```python3
import great_expectations as ge

expectation_suite = ge.core.ExpectationSuite(
    expectation_suite_name="validate_on_insert_suite"
)
```

#### Add Expectations in the Source Code

Add some expectation to your suite to validate columns:
```python3
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

expectation_suite.add_expectation(
    ge.core.ExpectationConfiguration(
        expectation_type="expect_column_value_lengths_to_be_between",
        kwargs={
            "column": "bar_name",
            "min_value": 3,
            "max_value": 10
        }
    )
)
```

#### Using Great Expectations Profiler

```python3
ge_profiler = ge.profile.BasicSuiteBuilderProfiler()
expectation_suite_profiler, _ = ge_profiler.profile(ge.from_pandas(df))
```


#### Hopsworks

 You can then setup a connection to your Hopsworks Feature Store. 

```python3
import hsfs

conn = hsfs.connection()
fs = conn.get_feature_store()
```

Before writing data to Hopsworks, we first need to create a Feature Group. For more information see [create Feature Group](create.md).

```python3
fg = fs.create_feature_group(
  "fg_with_data_validation",
  version=1,
  description="Validated data",
  primary_key=['foo_id'],
  online_enabled=False
  # Uncomment below to attach a GE suite when creating this Feature Group
  # expectation_suite=expectation_suite
)

# Create empty Feature Group in the backend
fg.insert(df.head(0))
```

### Step 2: Integrating Great Expectations with Hopsworks

Hopsworks provides different support functions to ease adding a data validation step to your feature pipeline. By default, validation objects returned by Hopsworks are a native great_expectations object that you can use directly. Hopsworks works with vanilla Great Expectations code - without additional Hopsworks abstractions - but for flexibility, you can also access the underlying Hopsworks abstractions by setting `ge_type=False`.

#### Attach an Expectation Suite to a Feature Group

The first step is to attach an expectation suite to your Feature Group. It enables persistence of the expectation suite to the hopsworks backend.

```python3
fg.save_expectation_suite(expectation_suite)

# or directly when creating your Feature Group

fg = fs.create_feature_group(
    ...,
    expectation_suite=expectation_suite
)
```

Note that the expectation suite object is modified in place to populate it with necessary information to further upload validation reports. When fetching an expectation suite from Hopsworks the meta field of each expectation contained in the suite is populated with an `expectationId` field. This id is used in the backend to link a particular expectation to its validation history.

This suite can easily be retrieved during a different session or deleted whenever you are working with this Feature Group by calling:

```python3
ge_expectation_suite = fg.get_expectation_suite()
# or delete with
fg.drop_expectation_suite()
```

#### Validate your data

As validation objects returned by Hopsworks are native Great Expectation objects you can run validation using the usual Great Expectations syntax:

```python3
ge_df = ge.from_pandas(df, expectation_suite=fg.get_expectation_suite())
ge_report = ge_df.validate()
```

Note that you should always use an expectation suite that has been saved to Hopsworks if you inted to upload the associated validation report. You can use a convenience wrapper method provided by Hopsworks to validate using the attached suite:

```python3
ge_report = fg.validate(df)
# set the save_report parameter to False to skip uploading the report to Hopsworks
# ge_report = fg.validate(df, save_report=False)
```

This will run the validation using the expectation suite attached to this Feature Group and raise an exception if no attached suite is found.


#### Save Validation Reports

When running validation using Great Expectations, a validation report is generated containing all validation results for the different expectations. Each result provides informations about whether the provided DataFrame conforms to the corresponding expectation. These reports can be stored in Hopsworks to save a validation history for the data written to a particular Feature Group. 

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

By default, attaching an expectation suite to a Feature Group enables automatic validation on insertion. Meaning calling `fg.insert` after attaching an expectation suite to a Feature Group will perform validation under the hood (on the client) and upload the validation report. This approach enables you, the developpe, to write cleaner more maintainable code while Hopsworks manages the operational problem of storing your data validation history alongside the data itself.

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

Hopsworks is focused on making the transition from development to production as seamless as possible. To switch between these two behaviours you can simply use the `validation_insertion_policy` parameter. By default, expectation suites are attached to Feature Groups as a monitoring tool. This default choice is made as it corresponds to development setup and avoids any loss of data on insertion.

```python3
fg.save_expectation_suite(expectation_suite)
# defaults to the monitoring behaviour
fg.save_expectation_suite(expectation_suite, validation_insertion_policy="ALWAYS")
```

When you want to switch from development to production, you can enable gatekeeping by setting:

```python3
fg.save_expectation_suite(fg.get_expectation_suite(), validation_insertion_policy="STRICT")
```
