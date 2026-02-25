---
description: Documentation on how to attach model evaluation images to a model.
---

# How To Save Model Evaluation Images

## Introduction

In this guide, you will learn how to attach ==model evaluation images== to a model.
Model evaluation images are images that visually describe model performance metrics.
For example, **confusion matrices**, **ROC curves**, **model bias tests**, and **training loss curves** are examples of common model evaluation images.
By attaching model evaluation images to your versioned model, other users can better understand the model performance and evaluation metrics.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

    ```python
    import hopsworks

    project = hopsworks.login()

    # get Hopsworks Model Registry handle
    mr = project.get_model_registry()
    ```

### Step 2: Generate model evaluation images

Generate an image that visualizes model performance and evaluation metrics

=== "Python"

    ```python
    import seaborn
    from sklearn.metrics import confusion_matrix

    # Predict the training data using the trained model
    y_pred_train = model.predict(X_train)

    # Predict the test data using the trained model
    y_pred_test = model.predict(X_test)

    # Calculate and print the confusion matrix for the test predictions
    results = confusion_matrix(y_test, y_pred_test)

    # Create a DataFrame for the confusion matrix results
    df_confusion_matrix = pd.DataFrame(
        results,
        ['True Normal', 'True Fraud'],
        ['Pred Normal', 'Pred Fraud'],
    )

    # Create a heatmap using seaborn with annotations
    heatmap = seaborn.heatmap(df_confusion_matrix, annot=True)

    # Get the figure and display it
    fig = heatmap.get_figure()
    fig.show()
    ```

### Step 3: Save the figure to a file inside the model directory

Save the figure to a file with a common filename extension (for example, .png or .jpeg), and place it in a directory called `images` - a subdirectory of the model directory that is registered to Hopsworks.

=== "Python"

    ```python
    # Specify the directory name for saving the model and related artifacts
    model_dir = "./model"

    # Create a subdirectory of model_dir called 'images' for saving the model evaluation images
    model_images_dir = model_dir + "/images"
    if not os.path.exists(model_images_dir):
        os.mkdir(model_images_dir)

    # Save the figure to an image file in the images directory
    fig.savefig(model_images_dir + "/confusion_matrix.png")

    # Register the model
    py_model = mr.python.create_model(name="py_model")
    py_model.save("./model")
    ```
