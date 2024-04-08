# How To Save Model Evaluation Images

## Introduction

In this guide, you will learn how to attach ==model evaluation images== to a model. Model evaluation images contain **confusion matrices**, **ROC curves** or other graphs that help visualizing model evaluation metrics. By attaching model evaluation images to your model version, other users can better understand the experiment results obtained during model training.

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks

project = hopsworks.login()

# get Hopsworks Model Registry handle
mr = project.get_model_registry()
```

### Step 2: Generate model evaluation figures

Generate a figure that visualizes a model metric. 

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

### Step 3: Save the figures as images inside the model directory

Save the figure to an image file, and place it in a directory with name ´images´ inside the model directory to be exported.

```python
# Specify the directory name for saving the model and related artifacts
model_dir = "./model"

# Create a directory with name 'images' for saving the model evaluation images
model_images_dir = model_dir + "/images"
if not os.path.exists(model_images_dir):
    os.mkdir(model_images_dir)

# Save the figure to an image file in the images directory
fig.savefig(model_images_dir + "/confusion_matrix.png")

# Register the model
py_model = mr.python.create_model(name="py_model")
py_model.save("./model")
```

## Conclusion

In this guide you learned how to attach model evaluation images to a model, helping better understand the experiment results obtained during model training.