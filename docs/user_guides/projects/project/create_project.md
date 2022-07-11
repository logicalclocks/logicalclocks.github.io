# How To Create A Project

## Introduction

In this guide, you will learn how to create a new project.

!!! notice "Project name validation rules"
    A valid project name can only contain characters a-z, A-Z, 0-9 and special characters ‘_’ and ‘.’ but not ‘__’ (double underscore). There is also a number of [reserved project names](#reserved-project-names) that can not be used.

## GUI

### Step 1: Create a project

If you log in to the platform and do not have any projects, you are presented with the following view. To run the Feature Store tour click `Run a demo project`, to create a new project click `Create new project`.

For this guide click `Create new project` to continue.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/no_project_list.png" alt="API Keys">
    <figcaption>Landing page</figcaption>
  </figure>
</p>

### Step 2: Project creation form

In the creation form in which you enter the project name, an optional description and set of members to invite to the project.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/create_project_form.png" alt="API Keys">
    <figcaption>Project creation form</figcaption>
  </figure>
</p>

### Step 3: Project creation

Then wait for the project creation process to finish.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/project_creation.gif" alt="API Keys">
    <figcaption>List of created API Keys</figcaption>
  </figure>
</p>

### Step 4: Project overview

Once the project is created the overview page for it will appear.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/project_overview.png" alt="API Keys">
    <figcaption>List of created API Keys</figcaption>
  </figure>
</p>

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks

connection = hopsworks.connection()
```

### Step 2: Create project

```python
project = connection.create_project("my_project")
```

### API Reference

[Projects](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/projects/)

## Reserved project names

```bash
PROJECTS, HOPS-SYSTEM, HOPSWORKS, INFORMATION_SCHEMA, AIRFLOW, GLASSFISH_TIMERS, GRAFANA, HOPS, METASTORE,
MYSQL, NDBINFO, PERFORMANCE_SCHEMA, SQOOP, SYS, GLASSFISH_TIMERS, GRAFANA, HOPS, METASTORE, MYSQL, NDBINFO,
PERFORMANCE_SCHEMA, SQOOP, SYS, BIGINT, BINARY, BOOLEAN, BOTH, BY, CASE, CAST, CHAR, COLUMN, CONF, CREATE, CROSS, CUBE, CURRENT, CURRENT_DATE,
CURRENT_TIMESTAMP, CURSOR, DATABASE, DATE, DECIMAL, DELETE, DESCRIBE, DISTINCT, DOUBLE, DROP, ELSE, END,
EXCHANGE, EXISTS, EXTENDED, EXTERNAL, FALSE, FETCH, FLOAT, FOLLOWING, FOR, FROM, FULL, FUNCTION, GRANT, GROUP,
GROUPING, HAVING, IF, IMPORT, IN, INNER, INSERT, INT, INTERSECT, INTERVAL, INTO, IS, JOIN, LATERAL, LEFT, LESS,
LIKE, LOCAL, MACRO, MAP, MORE, NONE, NOT, NULL, OF, ON, OR, ORDER, OUT, OUTER, OVER, PARTIALSCAN, PARTITION,
PERCENT, PRECEDING, PRESERVE, PROCEDURE, RANGE, READS, REDUCE, REVOKE, RIGHT, ROLLUP, ROW, ROWS, SELECT, SET,
SMALLINT, TABLE, TABLESAMPLE, THEN, TIMESTAMP, TO, TRANSFORM, TRIGGER, TRUE, TRUNCATE, UNBOUNDED, UNION,
UNIQUEJOIN, UPDATE, USER, USING, UTC_TMESTAMP, VALUES, VARCHAR, WHEN, WHERE, WINDOW, WITH, COMMIT, ONLY,
REGEXP, RLIKE, ROLLBACK, START, CACHE, CONSTRAINT, FOREIGN, PRIMARY, REFERENCES, DAYOFWEEK, EXTRACT, FLOOR,
INTEGER, PRECISION, VIEWS, TIME, NUMERIC, SYNC, BASE, PYTHON37, FILEBEAT.

And any word containing _FEATURESTORE.
```

## Conclusion

In this guide you learned how to create a project.