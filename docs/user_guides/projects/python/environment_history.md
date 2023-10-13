# Python Environment History
The Hopsworks installation ships with a Miniconda environment that comes preinstalled with the most popular libraries you can find in a data scientist toolkit, including TensorFlow, PyTorch and sci-kit-learn. The environment may be managed using the Hopsworks Python service to install or manage libraries which may then be used in Jupyter or the Jobs service in the platform.

The Python virtual environment is shared by different members of the project. When a member of the project introduces a change to the environment i.e., installs/uninstalls a library, a new environment is created and it becomes a defacto environment for everyone in the project. It is therefore important to track how the environment has been changing over time i.e., what libraries were installed, uninstalled, upgraded, or downgraded when the environment was created and who introduced the changes. 

In this guide, you will learn how you can track the changes of your Python environment.

## Viewing python environment history in the UI
The Python environment evolves over time as libraries are installed, uninstalled, upgraded, and downgraded. To assist in tracking the changes in the environment, you can see the environment history in the UI. You can view what changes were introduced at each point a new environment was created. Hopsworks will keep a version of a YAML file for each environment so that if you want to restore an older environment you can use it. To see the differences between environments click on the button as shown in figure 1. You will then see the difference between the environment and the previous environment it was created from.
<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/environment_history.png" alt="Python environment history">
    <figcaption>Figure 1: You can see the difference between the two environments by clicking on the button pointed. </figcaption>
  </figure>
</p>

If you had built the environment using custom commands you can go back to see what commands were run during the build as shown in figure 2. 
<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/environment_history_with_custom_commands.png" alt="Python environment history with custom commands">
    <figcaption>Figure 2:  You can see custom commands that were used to create the environment by clicking on the button pointed. </figcaption>
  </figure>
</p>

# Conclusion
In this guide, you have learned how you can track the changes of your Python environment.
