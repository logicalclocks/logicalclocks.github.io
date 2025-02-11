# How To Export a Torch Model

## Introduction

In this guide you will learn how to export a Torch model and register it in the Model Registry.


## Code

### Step 1: Connect to Hopsworks

=== "Python"
    ```python
    import hopsworks

    project = hopsworks.login()

    # get Hopsworks Model Registry handle
    mr = project.get_model_registry()
    ```

### Step 2: Train

Define your Torch model and run the training loop.

=== "Python"
    ```python
    # Define the model architecture
    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 6, 5)
            ...

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            ...
            return x

    # Instantiate the model
    net = Net()

    # Run the training loop
    for epoch in range(n):
        ...
    ```

### Step 3: Export to local path

Export the Torch model to a directory on the local filesystem.

=== "Python"
    ```python
    model_dir = "./model"

    torch.save(net.state_dict(), model_dir)
    ```

### Step 4: Register model in registry

Use the `ModelRegistry.torch.create_model(..)` function to register a model as a Torch model. Define a name, and attach optional metrics for your model, then invoke the `save()` function with the parameter being the path to the local directory where the model was exported to.  

=== "Python"
    ```python
    # Model evaluation metrics
    metrics = {'accuracy': 0.92}

    tch_model = mr.torch.create_model("tch_model", metrics=metrics)

    tch_model.save(model_dir)
    ```

## Going Further

You can attach an [Input Example](../input_example.md) and a [Model Schema](../model_schema.md) to your model to document the shape and type of the data the model was trained on.
