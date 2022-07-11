# How To Configure Inference Logging

## Introduction

Once a model is deployed and starts making predictions as inference requests arrive, logging model inputs and predictions becomes essential to monitor the health of the model and take action if the model's performance degrades over time.

Hopsworks supports logging both inference requests and predictions as events to a Kafka topic for analysis.

!!! warning "Topic schemas vary depending on the serving tool. See [below](#topic-schema)"

## GUI

### Step 1: Create new deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, click on `New deployment` if there are not existing deployments or on `Create new deployment` at the top-right corner to open the deployment creation form.

### Step 2: Go to advanced options

A simplified creation form will appear including the most common deployment fields among all the configuration possible. Inference logging is part of the advanced options of a deployment. To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 85%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Configure inference logging

To enable inference logging, choose `CREATE` as Kafka topic name to create a new topic, or select an existing topic. If you prefer, you can disable inference logging by selecting `NONE`.

If you decide to create a new topic, select the number of partitions and number of replicas for your topic, or use the default values.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_logger.png" alt="Inference logger in advanced deployment form">
    <figcaption>Inference logging configuration with a new kafka topic</figcaption>
  </figure>
</p>

If the deployment is created with KServe enabled, you can specify which inference logs you want to send to the Kafka topic (i.e., `MODEL_INPUTS`, `PREDICTIONS` or both)

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## CODE

### Step 1: Connect to Hopsworks

```python
import hopsworks

connection = hopsworks.connection()

project = connection.get_project("my_project")

# get Hopsworks Model Registry handle
mr = project.get_model_registry()

# get Hopsworks Model Serving handle
ms = project.get_model_serving()
```

### Step 2: Define an inference logger

```python

from hsml.inference_logger import InferenceLogger
from hsml.kafka_topic import KafkaTopic

new_topic = KafkaTopic(name="CREATE",
                       # optional
                       num_partitions=1,
                       num_replicas=1
                       )

my_logger = InferenceLogger(kafka_topic=new_topic, mode="ALL")
```

!!! notice "Use dict for simpler code"
    Similarly, you can create the same logger with:
    
    ```python

    my_logger = InferenceLogger(kafka_topic={"name": "CREATE"}, mode="ALL")
    ```

### Step 3: Create a deployment with the inference logger

```python

my_model = mr.get_model("my_model", version=1)

my_predictor = ms.create_predictor(my_model,
                                   inference_logger=my_logger
                                   )
my_predictor.deploy()

# or

my_deployment = ms.create_deployment(my_predictor)
my_deployment.save()
```

### API Reference

[Inference Logger](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/inference-logger/)

## Topic schema

The schema of Kafka events varies depending on the serving tool. In KServe deployments, model inputs and predictions are logged in separate events, but sharing the same `requestId` field. In non-KServe deployments, the same event contains both the model input and prediction related to the same inference request. 

??? example "Show kafka topic schemas"

    === "KServe"

        ``` json
        {
            "fields": [
                { "name": "servingId", "type": "int" },
                { "name": "modelName", "type": "string" },
                { "name": "modelVersion", "type": "int" },
                { "name": "requestTimestamp", "type": "long" },
                { "name": "responseHttpCode", "type": "int" },
                { "name": "inferenceId", "type": "string" },
                { "name": "messageType", "type": "string" },
                { "name": "payload", "type": "string" }
            ],
            "name": "inferencelog",
            "type": "record"
        }
        ```

    === "Docker / Kubernetes"

        ``` json
        {
            "fields": [
                { "name": "modelId", "type": "int" },
                { "name": "modelName", "type": "string" },
                { "name": "modelVersion", "type": "int" },
                { "name": "requestTimestamp", "type": "long" },
                { "name": "responseHttpCode", "type": "int" },
                { "name": "inferenceRequest", "type": "string" },
                { "name": "inferenceResponse", "type": "string" },
                { "name": "modelServer", "type": "string" },
                { "name": "servingTool", "type": "string" }
            ],
            "name": "inferencelog",
            "type": "record"
        }
        ```
