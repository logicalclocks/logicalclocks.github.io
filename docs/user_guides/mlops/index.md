# Model Registry & Serving Guides

A model goes from training into the registry, out through a deployment, and stays under monitoring.
The guides below follow that path.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-package-variant-closed:{ .lg .middle } **Start here**

    ---

    Register a trained model with its metrics, then deploy it in one call.

    ```python
    mr = project.get_model_registry()
    model = mr.python.create_model(
        name="fraud_detector",
        metrics={{"f1": 0.92}},
    )
    model.save("model_dir")
    deployment = model.deploy()
    ```

    [Model registry](registry/index.md) · [Deployment creation](serving/deployment.md) · [Model monitoring](model_monitoring/index.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-package-variant:{ .hops-role-ico } Register
{ .hops-role-cap }

- [Model registry](registry/index.md)
  Save a model with metrics, a schema and an input example, one version per save.
- [Frameworks](registry/frameworks/python.md)
  TensorFlow, PyTorch, scikit-learn, LLM and plain Python models.
- [Import from Hugging Face](registry/import_huggingface.md)
  Bring a Hub model into the registry without training it here.
- [Evaluation images](registry/model_evaluation_images.md)
  Attach plots and confusion matrices to a model version.

</div>

<div class="hops-task-group" markdown>
:material-cloud-upload-outline:{ .hops-role-ico } Serve
{ .hops-role-cap }

- [Deployment creation](serving/deployment.md)
  Deploy a registered model and check its state.
- [Predictor and transformer](serving/predictor.md)
  Custom inference code and pre/post-processing on KServe.
- [Logging and batching](serving/inference-logger.md)
  Log requests to a feature group, batch them for throughput.
- [Resources and autoscaling](serving/resources.md)
  CPU, memory, GPU and replica bounds, with scheduling constraints.
- [Reach the endpoint](serving/rest-api.md)
  API protocol, REST access from outside, troubleshooting.

</div>

<div class="hops-task-group" markdown>
:material-monitor-eye:{ .hops-role-ico } Observe
{ .hops-role-cap }

- [Model monitoring](model_monitoring/index.md)
  Compare logged inference data against the training dataset on a schedule.
- [Provenance](provenance/provenance.md)
  Trace a model back to its training data and features.
- [Vector database](../fs/vector_similarity_search.md)
  Similarity search over embeddings stored in the feature store.
- [Agents](../agents/index.md)
  Agent tasks as jobs and served interactive agents.

</div>

</div>
