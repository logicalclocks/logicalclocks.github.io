# Compute Guides

Compute is where code runs inside a project: notebooks, a terminal, jobs, schedules and served apps, all on the project's Python environments.
The guides go from writing code interactively to running it on a schedule.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-play-circle-outline:{ .lg .middle } **Start here**

    ---

    Upload a script and run it as a job from any Python session.
    Inside the project, Jupyter and the terminal are already logged in.

    ```python
    jobs_api = project.get_job_api()
    config = jobs_api.get_configuration("PYTHON")
    config["appPath"] = "Resources/script.py"
    job = jobs_api.create_job("py_job", config)
    execution = job.run(await_termination=True)
    ```

    [Run a Python job](../projects/jobs/python_job.md) · [Jupyter](../projects/jupyter/python_notebook.md) · [Python environments](../projects/python/python_env_overview.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-code-tags:{ .hops-role-ico } Write code
{ .hops-role-cap }

- [Jupyter](../projects/jupyter/python_notebook.md)
  Python, PySpark and Ray notebooks running against the project.
- [Terminal](terminal.md)
  A shell in the project with the CLI, Git and coding agents preinstalled.
- [Python environments](../projects/python/python_env_overview.md)
  Install libraries, clone and export environments, run custom build commands.
- [Apps](../projects/apps/index.md)
  Serve Streamlit, Gradio or any web app from the project.

</div>

<div class="hops-task-group" markdown>
:material-calendar-clock-outline:{ .hops-role-ico } Run and schedule
{ .hops-role-cap }

- [Jobs](../projects/jobs/python_job.md)
  Run Python, notebook, PySpark, Spark or Ray code as a job, on demand or on a schedule.
- [Airflow](../projects/airflow/airflow.md)
  Orchestrate jobs as DAGs with the Hopsworks operators.
- [Kubernetes scheduling](../projects/scheduling/kube_scheduler.md)
  Node selectors, tolerations and Kueue queues for where work lands.
- [Python deployments](../projects/python-deployment/python-deployment.md)
  Expose a Python function behind a REST endpoint.

</div>

</div>
