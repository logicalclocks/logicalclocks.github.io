# How To Export a LLM Model

## Introduction

In this guide you will learn how to export a [Large Language Model (LLM)](https://www.hopsworks.ai/dictionary/llms-large-language-models) and register it in the Model Registry.

## Code

### Step 1: Connect to Hopsworks

=== "Python"
    ```python
    import hopsworks

    project = hopsworks.login()

    # get Hopsworks Model Registry handle
    mr = project.get_model_registry()
    ```

### Step 2: Download the LLM

Download your base or fine-tuned LLM. LLMs can typically be downloaded using the official frameworks provided by their creators (e.g., HuggingFace, Ollama, ...)

=== "Python"
    ```python
    # Download LLM (e.g., using huggingface to download Llama-3.1-8B base model)
    from huggingface_hub import snapshot_download

    model_dir = snapshot_download(
                    "meta-llama/Llama-3.1-8B",
                    ignore_patterns="original/*"
                )
    ```

### Step 3: (Optional) Fine-tune LLM

If necessary, fine-tune your LLM with an [instruction set](https://www.hopsworks.ai/dictionary/instruction-datasets-for-fine-tuning-llms). A LLM can be fine-tuned fully or using [Parameter Efficient Fine Tuning (PEFT)](https://www.hopsworks.ai/dictionary/parameter-efficient-fine-tuning-of-llms) methods such as LoRA or QLoRA.

=== "Python"
    ```python
    # Fine-tune LLM using PEFT (LoRA, QLoRA) or other methods
    model_dir = ...
    ```

### Step 4: Register model in registry

Use the `ModelRegistry.llm.create_model(..)` function to register a model as LLM. Define a name, and attach optional metrics for your model, then invoke the `save()` function with the parameter being the path to the local directory where the model was exported to.

=== "Python"
    ```python
    # Model evaluation metrics
    metrics = {'f1-score': 0.8, 'perplexity': 31.62, 'bleu-score': 0.73}

    llm_model = mr.llm.create_model("llm_model", metrics=metrics)

    llm_model.save(model_dir)
    ```

## Going Further

You can attach an [Input Example](../input_example.md) and a [Model Schema](../input_example.md) to your model to document the shape and type of the data the model was trained on.
