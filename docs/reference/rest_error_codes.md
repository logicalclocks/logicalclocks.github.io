# REST API Status Codes

Hopsworks REST API responses carry a numeric status code alongside the HTTP status.
The code is namespaced by resource category so that the same HTTP status (for example `400 BAD_REQUEST`) can be distinguished by the failure it actually represents.
Most codes are errors, but a few categories also carry success codes for informational responses, so both the code and the HTTP status are shown for every entry.

The numbering convention is a total of 6 digits: the first 2 digits indicate the category and the last 4 the code within that category.

- Service error codes start with `10`
- Dataset error codes start with `11`
- Generic error codes start with `12`
- Job error codes start with `13`
- Request error codes start with `14`
- Project error codes start with `15`
- User and Security error codes start with `20`
- Dela error codes start with `17`
- Metadata error codes start with `18`
- Kafka error codes start with `19`
- CA error codes start with `22`
- DelaCSR error codes start with `23`
- Serving error codes start with `24`
- Inference error codes start with `25`
- Activities error codes start with `26`
- Featurestore error codes start with `27`
- Python error codes start with `28`

The Schema Registry category is a documented exception to this convention: it mirrors the Confluent Schema Registry's own error codes, which are 5 digits starting with the HTTP status code (for example `50001` for `500 Internal Server Error`).
It is listed last on this page for that reason.

This page is generated from `RESTCodes.java` in the `hopsworks-ee` product source by `scripts/gen_error_codes.py`.
Do not hand-edit the tables below; regenerate them instead.

<!-- BEGIN GENERATED -->

## ServiceErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 100001 | `JUPYTER_ADD_FAILURE` | 400 BAD_REQUEST | Failed to create Jupyter notebook dir. Jupyter will not work properly. Try recreating the following dir manually. |
| 100002 | `OPENSEARCH_SERVER_NOT_AVAILABLE` | 400 BAD_REQUEST | The OpenSearch Server is either down or misconfigured. |
| 100003 | `OPENSEARCH_SERVER_NOT_FOUND` | 503 SERVICE_UNAVAILABLE | Problem when reaching the OpenSearch server |
| 100004 | `HIVE_ADD_FAILURE` | 400 BAD_REQUEST | Failed to create the Hive database |
| 100005 | `LLAP_STATUS_INVALID` | 400 BAD_REQUEST | Unrecognized new LLAP status |
| 100006 | `LLAP_CLUSTER_ALREADY_UP` | 400 BAD_REQUEST | LLAP cluster already up |
| 100007 | `LLAP_CLUSTER_ALREADY_DOWN` | 400 BAD_REQUEST | LLAP cluster already down |
| 100008 | `DATABASE_UNAVAILABLE` | 503 SERVICE_UNAVAILABLE | The database is temporarily unavailable. Please try again later |
| 100010 | `ZOOKEEPER_SERVICE_UNAVAILABLE` | 503 SERVICE_UNAVAILABLE | ZooKeeper service unavailable |
| 100011 | `ANACONDA_NODES_UNAVAILABLE` | 503 SERVICE_UNAVAILABLE | No conda machine is enabled. Contact the administrator. |
| 100012 | `OPENSEARCH_INDEX_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while creating index in opensearch |
| 100013 | `ANACONDA_LIST_LIB_FORMAT_ERROR` | 500 INTERNAL_SERVER_ERROR | Problem listing libraries. Did conda get upgraded and change its output format? |
| 100014 | `ANACONDA_LIST_LIB_ERROR` | 500 INTERNAL_SERVER_ERROR | Problem listing libraries. Please contact the Administrator |
| 100016 | `JUPYTER_HOME_ERROR` | 500 INTERNAL_SERVER_ERROR | Couldn't resolve JUPYTER_HOME using DB. |
| 100017 | `JUPYTER_STOP_ERROR` | 500 INTERNAL_SERVER_ERROR | Couldn't stop Jupyter Notebook Server. |
| 100018 | `INVALID_YML` | 400 BAD_REQUEST | Invalid .yml file |
| 100019 | `INVALID_YML_SIZE` | 500 INTERNAL_SERVER_ERROR | .yml file too large. Please set a higher value for variable max_env_yml_byte_size |
| 100020 | `ANACONDA_FROM_YML_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to create Anaconda environment from .yml file. |
| 100021 | `PYTHON_INVALID_VERSION` | 400 BAD_REQUEST | Invalid version of python (valid: '3.7' |
| 100022 | `ANACONDA_REPO_ERROR` | 500 INTERNAL_SERVER_ERROR | Problem adding the repo. |
| 100023 | `ANACONDA_OP_IN_PROGRESS` | 412 PRECONDITION_FAILED | A conda environment operation is currently executing (create/remove/list). Wait for it to finish or clear it first. |
| 100024 | `HOST_TYPE_NOT_FOUND` | 412 PRECONDITION_FAILED | No hosts with the desired capability. |
| 100025 | `HOST_NOT_FOUND` | 404 NOT_FOUND | Host was not found. |
| 100026 | `HOST_NOT_REGISTERED` | 404 NOT_FOUND | Host has not registered. |
| 100027 | `ANACONDA_DEP_REMOVE_FORBIDDEN` | 400 BAD_REQUEST | Could not uninstall library, it is a mandatory dependency |
| 100028 | `ANACONDA_DEP_INSTALL_FORBIDDEN` | 409 CONFLICT | Library is already installed |
| 100029 | `ANACONDA_EXPORT_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to export Anaconda environment. |
| 100030 | `ANACONDA_LIST_LIB_NOT_FOUND` | 204 NO_CONTENT | No results found |
| 100031 | `OPENSEARCH_INDEX_NOT_FOUND` | 404 NOT_FOUND | Index was not found in OpenSearch |
| 100032 | `OPENSEARCH_INDEX_TYPE_NOT_FOUND` | 404 NOT_FOUND | Index type was not found in OpenSearch |
| 100033 | `JUPYTER_SERVERS_NOT_FOUND` | 404 NOT_FOUND | Could not find any Jupyter notebook servers for this project. |
| 100034 | `JUPYTER_SERVERS_NOT_RUNNING` | 412 PRECONDITION_FAILED | Could not find any Jupyter notebook servers for this project. |
| 100035 | `JUPYTER_START_ERROR` | 500 INTERNAL_SERVER_ERROR | Jupyter server could not start. |
| 100036 | `JUPYTER_SAVE_SETTINGS_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not save Jupyter Settings. |
| 100037 | `IPYTHON_CONVERT_ERROR` | 500 INTERNAL_SERVER_ERROR | Problem converting ipython notebook to python program |
| 100039 | `EMAIL_SENDING_FAILURE` | 500 INTERNAL_SERVER_ERROR | Could not send email |
| 100040 | `HOST_EXISTS` | 409 CONFLICT | Host exists |
| 100041 | `TENSORFLOW_VERSION_NOT_SUPPORTED` | 400 BAD_REQUEST | We currently do not support this version of TensorFlow. Update to a newer version or contact an admin |
| 100042 | `SERVICE_GENERIC_ERROR` | 500 INTERNAL_SERVER_ERROR | Generic error while enabling the service |
| 100043 | `JUPYTER_SERVER_ALREADY_RUNNING` | 400 BAD_REQUEST | Jupyter Notebook Server is already running |
| 100044 | `ERROR_EXECUTING_REMOTE_COMMAND` | 500 INTERNAL_SERVER_ERROR | Error executing command over SSH |
| 100045 | `OPERATION_NOT_SUPPORTED` | 400 BAD_REQUEST | Supplied operation is not supported |
| 100046 | `GIT_COMMAND_FAILURE` | 400 BAD_REQUEST | Git command failed to execute |
| 100047 | `JUPYTER_NOTEBOOK_VERSIONING_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to version notebook |
| 100048 | `SERVICE_NOT_FOUND` | 404 NOT_FOUND | Service not found |
| 100049 | `ACTION_FORBIDDEN` | 400 BAD_REQUEST | Action forbidden |
| 100050 | `VARIABLE_NOT_FOUND` | 404 NOT_FOUND | Requested variable not found |
| 100051 | `DOCKER_IMAGE_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while creating the docker image |
| 100052 | `METASTORE_CONNECTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error opening connection with the Hive metastore |
| 100053 | `SERVICE_DISCOVERY_ERROR` | 500 INTERNAL_SERVER_ERROR | Service not found |
| 100054 | `WRONG_HDFS_USERNAME_PROVIDED_FOR_ATTACHING_JUPYTER_CONFIGURATION_TO_NOTEBOOK` | 400 BAD_REQUEST | Failed to attach jupyter configuration to notebook. Wrong hdfs username provided |
| 100055 | `ATTACHING_JUPYTER_CONFIG_TO_NOTEBOOK_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to attach jupyter configuration to notebook |
| 100056 | `RM_METRICS_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to fetch utilization metrics |
| 100057 | `PROMETHEUS_QUERY_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to execute prometheus query |
| 100058 | `GRAFANA_PROXY_ERROR` | 500 INTERNAL_SERVER_ERROR | Unauthorized access to dashboard |
| 100059 | `DOCKER_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to run docker command |
| 100060 | `LOCAL_FILESYSTEM_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to write to local filesystem |
| 100061 | `INVALID_DOCKER_COMMAND_FILE` | 400 BAD_REQUEST | Invalid commands file provided |
| 100062 | `INVALID_ARTIFACT_FOR_DOCKER_COMMANDS` | 400 BAD_REQUEST | Invalid artifact provided for docker commands |
| 100063 | `ENVIRONMENT_YAML_READ_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to read yaml file |
| 100064 | `ENVIRONMENT_BUILD_NOT_FOUND` | 404 NOT_FOUND | Build not found in environment history |
| 100065 | `ENVIRONMENT_HISTORY_READ_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to read environment history record from database |
| 100066 | `ENVIRONMENT_HISTORY_CUSTOM_COMMANDS_FILE_READ_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to read custom command file |
| 100067 | `KUBE_CLIENT_ERROR` | 500 INTERNAL_SERVER_ERROR | Kubernetes client error |
| 100068 | `WRONG_HDFS_USERNAME_PROVIDED_FOR_SAVING_SPARK_SESSION_FROM_NOTEBOOK` | 400 BAD_REQUEST | Failed to save spark session from jupyter server |
| 100069 | `WRONG_HDFS_USERNAME_PROVIDED_FOR_JUPYTER_RAY_SESSION_OPERATION` | 400 BAD_REQUEST | Hdfs username provided for jupyter ray session operation does not exist |
| 100070 | `KERNEL_NOT_FOUND` | 404 NOT_FOUND | Kernel id not found in the running jupyter notebook server |
| 100071 | `RAY_SESSION_NOT_FOUND` | 404 NOT_FOUND | Ray session not found |
| 100072 | `INVALID_CUSTOM_COMMAND_ENV_VARIABLES` | 400 BAD_REQUEST | Invalid custom command environment variables |
| 100073 | `TERMINAL_ERROR` | 500 INTERNAL_SERVER_ERROR | Terminal error |
| 100074 | `WEBSOCKET_POOL_FULL` | 503 SERVICE_UNAVAILABLE | The cluster has reached the limit for active sessions across Jupyter notebooks, terminals, and apps. Starting a new session will fail until existing sessions are closed. If this happens often, contact your administrator to raise the limit. |

## DatasetErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 110000 | `DATASET_OPERATION_FORBIDDEN` | 403 FORBIDDEN | Dataset/content operation forbidden |
| 110001 | `DATASET_OPERATION_INVALID` | 400 BAD_REQUEST | Operation cannot be performed. |
| 110002 | `DATASET_OPERATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Dataset operation failed. |
| 110003 | `DATASET_ALREADY_SHARED_WITH_PROJECT` | 400 BAD_REQUEST | Dataset already shared with project |
| 110004 | `DATASET_NOT_SHARED_WITH_PROJECT` | 400 BAD_REQUEST | Dataset is not shared with project. |
| 110005 | `DATASET_NAME_EMPTY` | 400 BAD_REQUEST | DataSet name cannot be empty. |
| 110006 | `FILE_CORRUPTED_REMOVED_FROM_HDFS` | 400 BAD_REQUEST | Corrupted file removed from hdfs. |
| 110007 | `INODE_DELETION_ERROR` | 500 INTERNAL_SERVER_ERROR | File/Dir could not be deleted. |
| 110008 | `INODE_NOT_FOUND` | 404 NOT_FOUND | File not found. |
| 110009 | `DATASET_REMOVED_FROM_HDFS` | 400 BAD_REQUEST | DataSet removed from hdfs. |
| 110010 | `SHARED_DATASET_REMOVED` | 400 BAD_REQUEST | The shared dataset has been removed from this project. |
| 110011 | `DATASET_NOT_FOUND` | 400 BAD_REQUEST | DataSet not found. |
| 110012 | `DESTINATION_EXISTS` | 400 BAD_REQUEST | Destination already exists. |
| 110013 | `DATASET_ALREADY_PUBLIC` | 409 CONFLICT | Dataset is already public. |
| 110014 | `DATASET_ALREADY_IN_PROJECT` | 400 BAD_REQUEST | Dataset is already in project. |
| 110015 | `DATASET_NOT_PUBLIC` | 400 BAD_REQUEST | DataSet is not public. |
| 110016 | `DATASET_NOT_EDITABLE` | 400 BAD_REQUEST | DataSet is not editable. |
| 110017 | `DATASET_PENDING` | 400 BAD_REQUEST | DataSet is not yet accessible. Accept the share request to access it. |
| 110018 | `PATH_NOT_FOUND` | 400 BAD_REQUEST | Path not found |
| 110019 | `PATH_NOT_DIRECTORY` | 400 BAD_REQUEST | Requested path is not a directory |
| 110020 | `PATH_IS_DIRECTORY` | 400 BAD_REQUEST | Requested path is a directory |
| 110021 | `DOWNLOAD_ERROR` | 400 BAD_REQUEST | Failed to download. |
| 110022 | `DOWNLOAD_PERMISSION_ERROR` | 400 BAD_REQUEST | Your role does not allow to download this file |
| 110023 | `DATASET_PERMISSION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not update dataset permissions |
| 110024 | `COMPRESSION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while performing a (un)compress operation |
| 110025 | `DATASET_OWNER_ERROR` | 400 BAD_REQUEST | You cannot perform this action on a dataset you are not the owner |
| 110026 | `DATASET_PUBLIC_IMMUTABLE` | 400 BAD_REQUEST | Public datasets are immutable. |
| 110028 | `DATASET_NAME_INVALID` | 400 BAD_REQUEST | Name of dir is invalid |
| 110029 | `IMAGE_SIZE_INVALID` | 400 BAD_REQUEST | Image is too big to display please download it by double-clicking it instead |
| 110030 | `FILE_PREVIEW_ERROR` | 400 BAD_REQUEST | README.md too large to be previewd |
| 110031 | `DATASET_PARAMETERS_INVALID` | 400 BAD_REQUEST | Invalid parameters for requested dataset operation |
| 110032 | `EMPTY_PATH` | 400 BAD_REQUEST | Empty path requested |
| 110033 | `ONGOING_PERMISSION_OPERATION` | 409 CONFLICT | There is an ongoing permission operation |
| 110035 | `UPLOAD_PATH_NOT_SPECIFIED` | 400 BAD_REQUEST | The path to upload the template was not specified |
| 110036 | `README_NOT_ACCESSIBLE` | 401 UNAUTHORIZED | Readme not accessible. |
| 110037 | `COMPRESSION_SIZE_ERROR` | 412 PRECONDITION_FAILED | Not enough free space on the local scratch directory to download and unzip this file. Talk to your admin to increase disk space at the path: hopsworks/staging_dir |
| 110038 | `INVALID_PATH_FILE` | 400 BAD_REQUEST | The requested path does not resolve to a valid file |
| 110039 | `INVALID_PATH_DIR` | 400 BAD_REQUEST | The requested path does not resolve to a valid directory |
| 110040 | `UPLOAD_DIR_CREATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Uploads directory could not be created in the file system |
| 110041 | `UPLOAD_CONCURRENT_ERROR` | 412 PRECONDITION_FAILED | A file with the same name is being uploaded |
| 110042 | `UPLOAD_RESUMABLEINFO_INVALID` | 400 BAD_REQUEST | ResumableInfo is invalid |
| 110043 | `UPLOAD_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred while uploading file |
| 110044 | `DATASET_REQUEST_EXISTS` | 409 CONFLICT | Request for this dataset from this project already exists. |
| 110045 | `COPY_FROM_PROJECT` | 403 FORBIDDEN | Cannot copy file/folder from another project |
| 110046 | `COPY_TO_PUBLIC_DS` | 403 FORBIDDEN | Can not copy to a public dataset. |
| 110047 | `DATASET_SUBDIR_ALREADY_EXISTS` | 400 BAD_REQUEST | A sub-directory with the same name already exists. |
| 110048 | `DOWNLOAD_NOT_ALLOWED` | 403 FORBIDDEN | Downloading files is not allowed. Please contact the system administrator for further information. |
| 110049 | `DATASET_REQUEST_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not send dataset request |
| 110050 | `DATASET_ACCESS_PERMISSION_DENIED` | 403 FORBIDDEN | Permission denied. |
| 110051 | `PATH_ENCODING_NOT_SUPPORTED` | 400 BAD_REQUEST | Unsupported encoding. |
| 110052 | `ATTACH_XATTR_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to attach Xattr. |
| 110053 | `TARGET_PROJECT_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Target project not found. |
| 110054 | `DATASET_PERMISSION_IMMUTABLE` | 400 BAD_REQUEST | Internal datasets permission can not be changed. |
| 110055 | `UPLOAD_DISK_SPACE_ERROR` | 500 INTERNAL_SERVER_ERROR | Upload failed: HopsFS storage is full. Please contact your administrator to free up disk space. |

## GenericErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 120000 | `UNKNOWN_ERROR` | 500 INTERNAL_SERVER_ERROR | A generic error occurred. |
| 120001 | `ILLEGAL_ARGUMENT` | 422 UNPROCESSABLE_ENTITY | An argument was not provided or it was malformed. |
| 120002 | `ILLEGAL_STATE` | 400 BAD_REQUEST | A runtime error occurred. |
| 120003 | `ROLLBACK` | 500 INTERNAL_SERVER_ERROR | The last transaction did not complete as expected |
| 120004 | `WEBAPPLICATION` | dynamic (from wrapped exception) | Web application exception occurred |
| 120005 | `PERSISTENCE_ERROR` | 500 INTERNAL_SERVER_ERROR | Persistence error occurred |
| 120006 | `UNKNOWN_ACTION` | 400 BAD_REQUEST | This action can not be applied on this resource. |
| 120007 | `INCOMPLETE_REQUEST` | 400 BAD_REQUEST | Some parameters were not provided or were not in the required format. |
| 120008 | `SECURITY_EXCEPTION` | 500 INTERNAL_SERVER_ERROR | A Java security error occurred. |
| 120009 | `ENDPOINT_ANNOTATION_MISSING` | 503 SERVICE_UNAVAILABLE | The requested endpoint did not have any project role annotation |
| 120010 | `ENTERPRISE_FEATURE` | 400 BAD_REQUEST | This feature is only available in the enterprise edition |
| 120011 | `NOT_AUTHORIZED_TO_ACCESS` | 400 BAD_REQUEST | Project not accessible to user |
| 120012 | `FEATURE_FLAG_NOT_ENABLED` | 400 BAD_REQUEST | Platform feature not enabled |

## JobErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 130000 | `JOB_START_FAILED` | 400 BAD_REQUEST | An error occurred while trying to start this job. Check the job logs for details |
| 130001 | `JOB_STOP_FAILED` | 400 BAD_REQUEST | An error occurred while trying to stop this job. |
| 130002 | `JOB_TYPE_UNSUPPORTED` | 400 BAD_REQUEST | Unsupported job type. |
| 130003 | `JOB_ACTION_UNSUPPORTED` | 400 BAD_REQUEST | Unsupported action type. |
| 130005 | `JOB_NAME_EMPTY` | 400 BAD_REQUEST | Job name is not set. |
| 130006 | `JOB_NAME_INVALID` | 400 BAD_REQUEST | Job name is invalid. Invalid charater(s) in job name |
| 130007 | `JOB_EXECUTION_NOT_FOUND` | 404 NOT_FOUND | Execution not found. |
| 130008 | `JOB_EXECUTION_TRACKING_URL_NOT_FOUND` | 400 BAD_REQUEST | Tracking url not found. |
| 130009 | `JOB_NOT_FOUND` | 404 NOT_FOUND | Job not found. |
| 130010 | `JOB_EXECUTION_INVALID_STATE` | 400 BAD_REQUEST | Execution state is invalid. |
| 130011 | `JOB_LOG` | 400 BAD_REQUEST | Job log error. |
| 130012 | `JOB_DELETION_ERROR` | 400 BAD_REQUEST | Error while deleting job. |
| 130013 | `JOB_CREATION_ERROR` | 400 BAD_REQUEST | Error while creating job. |
| 130014 | `OPENSEARCH_INDEX_NOT_FOUND` | 400 BAD_REQUEST | OpenSearch indices do not exist |
| 130015 | `OPENSEARCH_TYPE_NOT_FOUND` | 400 BAD_REQUEST | OpenSearch type does not exist |
| 130016 | `TENSORBOARD_ERROR` | 204 NO_CONTENT | Error getting the TensorBoard(s) for this application |
| 130017 | `APPLICATIONID_NOT_FOUND` | 400 BAD_REQUEST | Error while deleting job. |
| 130018 | `JOB_ACCESS_ERROR` | 403 FORBIDDEN | Cannot access job |
| 130019 | `LOG_AGGREGATION_NOT_ENABLED` | 503 SERVICE_UNAVAILABLE | YARN log aggregation is not enabled |
| 130020 | `LOG_RETRIEVAL_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while retrieving YARN logs |
| 130021 | `JOB_SCHEDULE_UPDATE` | 500 INTERNAL_SERVER_ERROR | Could not update schedule. |
| 130022 | `JAR_INSPECTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not inspect jar file. |
| 130023 | `PROXY_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not get proxy user. |
| 130024 | `JOB_CONFIGURATION_CONVERT_TO_JSON_ERROR` | 400 BAD_REQUEST | Could not convert JobConfiguration to json |
| 130025 | `JOB_DELETION_FORBIDDEN` | 403 FORBIDDEN | Your role does not allow to delete this job. |
| 130026 | `UNAUTHORIZED_EXECUTION_ACCESS` | 403 FORBIDDEN | This execution does not belong to a job of this project. |
| 130027 | `APPID_NOT_FOUND` | 404 NOT_FOUND | AppId not found. |
| 130028 | `JOB_PROGRAM_VERSIONING_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to version application program |
| 130029 | `INSUFFICIENT_EXECUTOR_MEMORY` | 400 BAD_REQUEST | Insufficient executor memory provided. |
| 130030 | `NODEMANAGERS_OFFLINE` | 503 SERVICE_UNAVAILABLE | Nodemanagers are offline |
| 130031 | `DOCKER_MOUNT_NOT_ALLOWED` | 400 BAD_REQUEST | It is not allowed to mount volumes. |
| 130032 | `DOCKER_MOUNT_DIR_NOT_ALLOWED` | 400 BAD_REQUEST | It is not allowed to mount this directory. |
| 130033 | `DOCKER_UID_GID_STRICT` | 400 BAD_REQUEST | Docker jobs run in uid/gid strict mode. It it now allowed to set uid/gid. If you remove the uid/gid, the job will run with a default user. Please ask an administrator to update the setting if necessary. |
| 130034 | `JOB_ALERT_NOT_FOUND` | 404 NOT_FOUND | Job alert not found |
| 130035 | `JOB_ALERT_ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Job alert missing argument. |
| 130036 | `JOB_ALERT_ALREADY_EXISTS` | 400 BAD_REQUEST | Job alert with the same status already exists. |
| 130037 | `DOCKER_INVALID_JOB_PROPERTIES` | 400 BAD_REQUEST | Received invalid job property values |
| 130038 | `FAILED_TO_CREATE_ROUTE` | 400 BAD_REQUEST | Failed to create route. |
| 130039 | `FAILED_TO_DELETE_ROUTE` | 400 BAD_REQUEST | Failed to delete route. |
| 130040 | `EXECUTIONS_LIMIT_REACHED` | 400 BAD_REQUEST | Job reached the maximum number of executions. |
| 130041 | `JOB_ALREADY_EXISTS` | 400 BAD_REQUEST | Job with this name already exists. |
| 130042 | `JOB_SCHEDULE_NOT_FOUND` | 404 NOT_FOUND | Cannot find the job schedule. |
| 130043 | `UNMATCHED_JOB_NAME` | 400 BAD_REQUEST | Provided job names do not match. |
| 130044 | `UNMATCHED_JOB_SCHEDULE_AND_JOB_NAME` | 400 BAD_REQUEST | Requested job schedule id does not match the job name. |
| 130045 | `INVALID_RAY_JOB_ENVIRONMENT_YAML_FILE` | 400 BAD_REQUEST | Invalid Ray job environment yaml file. |
| 130046 | `JOB_DEPENDENCY_INSPECTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not inspect job dependencies. |
| 130047 | `JOB_DEPENDENCY_NOT_FOUND` | 400 BAD_REQUEST | Job dependency not found. |
| 130048 | `DLT_JOB_FEATURE_GROUP_NOT_FOUND` | 400 BAD_REQUEST | Feature group not found. |
| 130049 | `DLT_JOB_FEATURE_GROUP_NO_DATASOURCE` | 400 BAD_REQUEST | The feature group does not have a datasource. |
| 130050 | `DLT_JOB_UNSUPPORTED_CONNECTOR` | 400 BAD_REQUEST | The feature group connector does not support DLT sink functionality. |
| 130051 | `DLT_JOB_CONFIGS_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to create config for job. |
| 130052 | `DLT_JOB_FEATURESTORE_CONNECTOR_NOT_FOUND` | 400 BAD_REQUEST | Featurestore connector not found. |
| 130053 | `DLT_JOB_STATE_DIR_CREATION_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to create state directory for DLT job. |
| 130054 | `DLT_JOB_FEATURE_GROUP_NO_STORAGE_CONNECTOR` | 400 BAD_REQUEST | The feature group does not have a storage connector. |
| 130055 | `DLT_JOB_FEATURE_STORE_NOT_FOUND` | 400 BAD_REQUEST | Feature store not found. |
| 130056 | `DLT_JOB_FEATURE_GROUP_NO_DATA_SOURCE` | 400 BAD_REQUEST | The feature group does not have a data source. |
| 130057 | `DLT_JOB_FEATURE_GROUP_ID_MISMATCH` | 400 BAD_REQUEST | Ingestion feature group cannot be changed |
| 130058 | `DLT_JOB_FEATURE_STORE_ID_MISMATCH` | 400 BAD_REQUEST | Ingestion feature group cannot be changed |
| 130059 | `DLT_JOB_FEATURE_STORE_PROJECT_MISMATCH` | 400 BAD_REQUEST | Ingestion job can only be created in the same project as the feature store. |
| 130060 | `DLT_JOB_ALREADY_RUNNING` | 400 BAD_REQUEST | A DLT job for this feature group is already running. |
| 130061 | `DLT_JOB_CLEAR_FEATUREGROUP_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to clear feature group data before DLT ingestion. |
| 130062 | `PYTHON_APP_ALREADY_RUNNING` | 400 BAD_REQUEST | A Python App is already running for this job. Stop it before starting a new one. |
| 130063 | `RESERVED_ENV_VAR_NAME` | 400 BAD_REQUEST | One or more environment variable names are reserved by the Hopsworks platform. |
| 130064 | `AGENT_INVALID_CONFIGURATION` | 400 BAD_REQUEST | Invalid agent job configuration. |
| 130065 | `MAX_QUEUED_EXECUTIONS_REACHED` | 429 TOO_MANY_REQUESTS | Max queued executions reached for this job. Wait for some to start before submitting more. |
| 130066 | `PYTHON_APP_READINESS_PROBE_INVALID` | 400 BAD_REQUEST | Readiness probe path must be a safe absolute path. |
| 130067 | `PYTHON_APP_BASE_PATH_INVALID` | 400 BAD_REQUEST | App base path must be a safe absolute path. |

## RequestErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 140000 | `MESSAGE_ACCESS_NOT_ALLOWED` | 403 FORBIDDEN | Message not allowed. |
| 140001 | `EMAIL_EMPTY` | 400 BAD_REQUEST | Email cannot be empty. |
| 140002 | `EMAIL_INVALID` | 400 BAD_REQUEST | Not a valid email address. |
| 140003 | `DATASET_REQUEST_ERROR` | 400 BAD_REQUEST | Error while submitting dataset request |
| 140004 | `REQUEST_UNKNOWN_ACTION` | 400 BAD_REQUEST | Unknown request action |
| 140005 | `MESSAGE_NOT_FOUND` | 404 NOT_FOUND | Message was not found |

## ProjectErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 150001 | `PROJECT_EXISTS` | 409 CONFLICT | Project with the same name already exists. |
| 150002 | `NUM_PROJECTS_LIMIT_REACHED` | 400 BAD_REQUEST | You have reached the maximum number of projects you could create. Contact an administrator to increase your limit or delete some of the existing projects. |
| 150003 | `INVALID_PROJECT_NAME` | 400 BAD_REQUEST | Invalid project name, valid characters: \[a-zA-Z0-9\]((?!__)\[_a-zA-Z0-9\]){0,62} |
| 150004 | `PROJECT_NOT_FOUND` | 400 BAD_REQUEST | Project wasn't found. |
| 150005 | `PROJECT_NOT_REMOVED` | 400 BAD_REQUEST | Project wasn't removed. |
| 150007 | `PROJECT_FOLDER_NOT_CREATED` | 500 INTERNAL_SERVER_ERROR | Project folder could not be created in HDFS. |
| 150008 | `STARTER_PROJECT_BAD_REQUEST` | 400 BAD_REQUEST | Type of starter project is not valid |
| 150009 | `PROJECT_FOLDER_NOT_REMOVED` | 400 BAD_REQUEST | Project folder could not be removed from HDFS. |
| 150010 | `PROJECT_REMOVAL_NOT_ALLOWED` | 403 FORBIDDEN | Project can only be deleted by its owner. |
| 150011 | `PROJECT_MEMBER_NOT_REMOVED` | 500 INTERNAL_SERVER_ERROR | Failed to remove team member. |
| 150012 | `MEMBER_REMOVAL_NOT_ALLOWED` | 403 FORBIDDEN | Your project role does not allow to remove other members from this project. |
| 150013 | `PROJECT_OWNER_NOT_ALLOWED` | 403 FORBIDDEN | Removing the project owner is not allowed. |
| 150014 | `PROJECT_OWNER_ROLE_NOT_ALLOWED` | 403 FORBIDDEN | Changing the role of the project owner is not allowed. |
| 150015 | `FOLDER_INODE_NOT_CREATED` | 400 BAD_REQUEST | Folder Inode could not be created in DB. |
| 150016 | `FOLDER_NAME_NOT_SET` | 400 BAD_REQUEST | Name cannot be empty. |
| 150017 | `FOLDER_NAME_TOO_LONG` | 400 BAD_REQUEST | Name cannot be longer than 88 characters. |
| 150018 | `FOLDER_NAME_CONTAIN_DISALLOWED_CHARS` | 400 BAD_REQUEST | Name cannot contain any of the characters |
| 150019 | `FILE_NAME_EXIST` | 400 BAD_REQUEST | File with the same name already exists. |
| 150020 | `FILE_NOT_FOUND` | 400 BAD_REQUEST | File not found. |
| 150021 | `NO_MEMBER_TO_ADD` | 400 BAD_REQUEST | No member to add. |
| 150022 | `NO_MEMBER_ADD` | 400 BAD_REQUEST | No member added. |
| 150023 | `TEAM_MEMBER_NOT_FOUND` | 404 NOT_FOUND | The selected user is not a team member in this project. |
| 150024 | `TEAM_MEMBER_ALREADY_EXISTS` | 400 BAD_REQUEST | The selected user is already a team member of this project. |
| 150025 | `ROLE_NOT_SET` | 400 BAD_REQUEST | Role cannot be empty. |
| 150026 | `PROJECT_NOT_SELECTED` | 400 BAD_REQUEST | No project selected |
| 150027 | `QUOTA_NOT_FOUND` | 400 BAD_REQUEST | Quota information not found. |
| 150028 | `QUOTA_ERROR` | 400 BAD_REQUEST | Quota create or update error. |
| 150029 | `PROJECT_QUOTA_ERROR` | 412 PRECONDITION_FAILED | This project is out of credits. |
| 150030 | `PROJECT_CREATED` | 201 CREATED | Project created successfully. |
| 150031 | `PROJECT_DESCRIPTION_CHANGED` | 200 OK | Project description changed. |
| 150033 | `PROJECT_SERVICE_ADDED` | 200 OK | Project service added |
| 150034 | `PROJECT_SERVICE_ADD_FAILURE` | 500 INTERNAL_SERVER_ERROR | Failure adding service |
| 150035 | `PROJECT_REMOVED` | 200 OK | The project and all related files were removed successfully. |
| 150036 | `PROJECT_REMOVED_NOT_FOLDER` | 500 INTERNAL_SERVER_ERROR | The project was removed successfully. But its datasets have not been deleted. |
| 150037 | `PROJECT_MEMBER_REMOVED` | 200 OK | Member removed successfully |
| 150038 | `PROJECT_MEMBERS_ADDED` | 200 OK | Members added successfully |
| 150039 | `PROJECT_MEMBER_ADDED` | 200 OK | One member added successfully |
| 150040 | `MEMBER_ROLE_UPDATED` | 200 OK | Role updated successfully. |
| 150041 | `MEMBER_REMOVED_FROM_TEAM` | 200 OK | Member removed from team. |
| 150042 | `PROJECT_INODE_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not create dummy Inode |
| 150043 | `PROJECT_FOLDER_EXISTS` | 409 CONFLICT | A folder with same name as the project already exists in the system. |
| 150044 | `PROJECT_USER_EXISTS` | 409 CONFLICT | Filesystem user(s) already exists in the system. |
| 150045 | `PROJECT_GROUP_EXISTS` | 409 CONFLICT | Filesystem group(s) already exists in the system. |
| 150046 | `PROJECT_CERTIFICATES_EXISTS` | 409 CONFLICT | Certificates for this project already exist in the system. |
| 150047 | `PROJECT_QUOTA_EXISTS` | 409 CONFLICT | Quotas corresponding to this project already exist in the system. |
| 150048 | `PROJECT_LOGS_EXIST` | 409 CONFLICT | Logs corresponding to this project already exist in the system. |
| 150049 | `PROJECT_VERIFICATIONS_FAILED` | 500 INTERNAL_SERVER_ERROR | Error occurred while running verifications |
| 150050 | `PROJECT_SET_PERMISSIONS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred while setting permissions for project folders. |
| 150051 | `PROJECT_HANDLER_PRECREATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project precreate handler. |
| 150052 | `PROJECT_HANDLER_POSTCREATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project postcreate handler. |
| 150053 | `PROJECT_HANDLER_PREDELETE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project predelete handler. |
| 150054 | `PROJECT_HANDLER_POSTDELETE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project postdelete handler. |
| 150055 | `PROJECT_TOUR_FILES_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while adding tour files to project. |
| 150056 | `PROJECT_KIBANA_CREATE_INDEX_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not create kibana index-pattern for project |
| 150057 | `PROJECT_KIBANA_CREATE_SEARCH_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not create kibana search for project |
| 150058 | `PROJECT_KIBANA_CREATE_DASHBOARD_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not create kibana dashboard for project |
| 150060 | `PROJECT_CONDA_LIBS_NOT_FOUND` | 404 NOT_FOUND | No preinstalled anaconda libs found. |
| 150061 | `KILL_MEMBER_JOBS` | 500 INTERNAL_SERVER_ERROR | Could not kill user's yarn applications |
| 150062 | `JUPYTER_SERVER_NOT_FOUND` | 404 NOT_FOUND | Could not find Jupyter entry for user in this project. |
| 150063 | `PYTHON_LIB_ALREADY_INSTALLED` | 304 NOT_MODIFIED | This python library is already installed on this project |
| 150064 | `PYTHON_LIB_NOT_INSTALLED` | 304 NOT_MODIFIED | This python library is not installed for this project. Cannot remove/upgrade op |
| 150066 | `ANACONDA_NOT_ENABLED` | 412 PRECONDITION_FAILED | First enable Anaconda. Click on 'Python' -> Activate Anaconda |
| 150067 | `TENSORBOARD_OPENSEARCH_INDEX_NOT_FOUND` | 404 NOT_FOUND | Could not find OpenSearch index for TensorBoard. |
| 150068 | `PROJECT_ROLE_FORBIDDEN` | 403 FORBIDDEN | Your project role does not allow to perform this action. |
| 150069 | `FOLDER_NAME_ENDS_WITH_DOT` | 400 BAD_REQUEST | Name cannot end in a period. |
| 150070 | `FOLDER_NAME_EXISTS` | 400 BAD_REQUEST | A directory with the same name already exists. If you want to replace it delete it first then try recreating. |
| 150071 | `PROJECT_SERVICE_NOT_FOUND` | 400 BAD_REQUEST | service was not found. |
| 150072 | `QUOTA_REQUEST_NOT_COMPLETE` | 400 BAD_REQUEST | Please specify both namespace and space quota. |
| 150073 | `RESERVED_PROJECT_NAME` | 400 BAD_REQUEST | Not allowed - reserved project name, pick another project name. |
| 150074 | `PROJECT_ANACONDA_ENABLE_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to enable conda. |
| 150075 | `PROJECT_NAME_TOO_LONG` | 400 BAD_REQUEST | Project name is too long - cannot be longer than 25 characters. |
| 150076 | `PROJECT_DOCKER_VERSION_EXTRACT_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to extract the hopsworks version of the docker image for this project. |
| 150077 | `PROJECT_DEFAULT_JOB_CONFIG_NOT_FOUND` | 404 NOT_FOUND | Default job config not found |
| 150078 | `ALERT_NOT_FOUND` | 404 NOT_FOUND | Alert not found |
| 150079 | `ALERT_ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Alert missing argument. |
| 150080 | `ALERT_ALREADY_EXISTS` | 400 BAD_REQUEST | Alert with the same status already exists. |
| 150081 | `FAILED_TO_ADD_MEMBER` | 400 BAD_REQUEST | Failed to add member. |
| 150082 | `FAILED_TO_CREATE_ROUTE` | 400 BAD_REQUEST | Failed to create route. |
| 150083 | `FAILED_TO_DELETE_ROUTE` | 400 BAD_REQUEST | Failed to delete route. |
| 150084 | `PROJECT_TEAM_ROLE_HANDLER_ADD_MEMBER_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project team role add handler. |
| 150085 | `PROJECT_TEAM_ROLE_HANDLER_UPDATE_MEMBERS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project team role update handler. |
| 150086 | `PROJECT_TEAM_ROLE_HANDLER_REMOVE_MEMBER_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during project team role remove handler. |
| 150087 | `PROJECT_TEAM_ROLE_NOT_SUPPORTED` | 400 BAD_REQUEST | Role not supported. |
| 150088 | `PROJECT_NAMESPACE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred when using kubernetes namespace in project |
| 150089 | `FAILED_TO_CREATE_WORKER_FOR_BREWER` | 500 INTERNAL_SERVER_ERROR | Failed to create worker for brewer. |
| 150090 | `PROJECT_SERVICE_NOT_ALLOWED` | 400 BAD_REQUEST | Project service not allowed. |
| 150091 | `PROJECT_MAPPING_ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Illegal argument. |
| 150092 | `PROJECT_MAPPING_NOT_ALLOWED` | 400 BAD_REQUEST | Operation not allowed. |
| 150093 | `PROJECT_MAPPING_NOT_FOUND` | 400 BAD_REQUEST | Mapping not found. |
| 150094 | `PROJECT_MAPPING_DUPLICATE_ENTRY` | 400 BAD_REQUEST | Duplicate entry. |
| 150095 | `MEMBER_MANAGEMENT_NOT_ALLOWED` | 400 BAD_REQUEST | Member management not allowed. |
| 150096 | `MCP_SERVER_NOT_FOUND` | 404 NOT_FOUND | MCP server not found. |
| 150097 | `MCP_SERVER_VALIDATION` | 400 BAD_REQUEST | MCP server validation error. |

## UserErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 160000 | `NO_ROLE_FOUND` | 401 UNAUTHORIZED | No valid role found for this user |
| 160001 | `USER_DOES_NOT_EXIST` | 400 BAD_REQUEST | User does not exist. |
| 160002 | `USER_WAS_NOT_FOUND` | 404 NOT_FOUND | User not found |
| 160003 | `USER_EXISTS` | 409 CONFLICT | There is an existing account associated with this email |
| 160004 | `ACCOUNT_REQUEST` | 401 UNAUTHORIZED | Your account has not yet been approved. |
| 160005 | `ACCOUNT_DEACTIVATED` | 401 UNAUTHORIZED | This account has been deactivated. |
| 160006 | `ACCOUNT_VERIFICATION` | 400 BAD_REQUEST | You need to verify your account. |
| 160007 | `ACCOUNT_BLOCKED` | 401 UNAUTHORIZED | Your account has been blocked. Contact the administrator. |
| 160008 | `AUTHENTICATION_FAILURE` | 401 UNAUTHORIZED | Authentication failed, invalid credentials |
| 160009 | `LOGOUT_FAILURE` | 400 BAD_REQUEST | Logout failed on backend. |
| 160014 | `PASSWORD_EMPTY` | 400 BAD_REQUEST | Password cannot be empty. |
| 160015 | `PASSWORD_TOO_SHORT` | 400 BAD_REQUEST | Password too short. |
| 160016 | `PASSWORD_TOO_LONG` | 400 BAD_REQUEST | Password too long. |
| 160017 | `PASSWORD_INCORRECT` | 400 BAD_REQUEST | Password incorrect |
| 160018 | `PASSWORD_PATTERN_NOT_CORRECT` | 400 BAD_REQUEST | Password should include one uppercase letter, one special character and/or alphanumeric characters. |
| 160019 | `INCORRECT_PASSWORD` | 401 UNAUTHORIZED | The password is incorrect. Please try again |
| 160020 | `PASSWORD_MISS_MATCH` | 400 BAD_REQUEST | Passwords do not match - typo? |
| 160021 | `TOS_NOT_AGREED` | 400 BAD_REQUEST | You must agree to our terms of use. |
| 160022 | `CERT_DOWNLOAD_DENIED` | 400 BAD_REQUEST | Admin is not allowed to download certificates |
| 160023 | `CREATED_ACCOUNT` | 400 BAD_REQUEST | You have successfully created an account but you might need to wait until your account has been approved before you can login. |
| 160024 | `PASSWORD_RESET_SUCCESSFUL` | 400 BAD_REQUEST | Your password was successfully reset your new password have been sent to your email. |
| 160025 | `PASSWORD_RESET_UNSUCCESSFUL` | 400 BAD_REQUEST | Your password could not be reset. Please try again later or contact support. |
| 160026 | `PASSWORD_CHANGED` | 400 BAD_REQUEST | Your password was successfully changed. |
| 160028 | `PROFILE_UPDATED` | 400 BAD_REQUEST | Your profile was updated successfully. |
| 160029 | `SSH_KEY_REMOVED` | 400 BAD_REQUEST | Your ssh key was deleted successfully. |
| 160030 | `NOTHING_TO_UPDATE` | 400 BAD_REQUEST | Nothing to update |
| 160031 | `CREATE_USER_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while creating user |
| 160032 | `CERT_AUTHORIZATION_ERROR` | 401 UNAUTHORIZED | Certificate CN does not match the username provided. |
| 160033 | `PROJECT_USER_CERT_NOT_FOUND` | 403 FORBIDDEN | Could not find exactly one certificate for user in project. |
| 160034 | `ACCOUNT_INACTIVE` | 401 UNAUTHORIZED | This account has not been activated |
| 160035 | `ACCOUNT_LOST_DEVICE` | 401 UNAUTHORIZED | This account has registered a lost device. |
| 160036 | `ACCOUNT_NOT_APPROVED` | 401 UNAUTHORIZED | This account has not yet been approved |
| 160037 | `INVALID_EMAIL` | 400 BAD_REQUEST | Invalid email format. |
| 160038 | `INCORRECT_DEACTIVATION_LENGTH` | 400 BAD_REQUEST | The message should have a length between 5 and 500 characters |
| 160039 | `TMP_CODE_INVALID` | 401 UNAUTHORIZED | The temporary code was wrong. |
| 160040 | `INCORRECT_CREDENTIALS` | 400 BAD_REQUEST | Incorrect email or password. |
| 160041 | `INCORRECT_VALIDATION_KEY` | 400 BAD_REQUEST | Incorrect validation key |
| 160042 | `ACCOUNT_ALREADY_VERIFIED` | 409 CONFLICT | User is already verified |
| 160043 | `TWO_FA_ENABLE_ERROR` | 500 INTERNAL_SERVER_ERROR | Cannot enable 2-factor authentication. |
| 160044 | `ACCOUNT_REGISTRATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Account registration error. |
| 160045 | `TWO_FA_DISABLED` | 412 PRECONDITION_FAILED | 2-factor authentication is disabled. |
| 160046 | `TRANSITION_STATUS_ERROR` | 400 BAD_REQUEST | The user can't transition from current status to requested status |
| 160047 | `ACCESS_CONTROL` | 403 FORBIDDEN | Client not authorized for this invocation. |
| 160048 | `SECRET_EMPTY` | 404 NOT_FOUND | Secret is empty |
| 160049 | `SECRET_EXISTS` | 409 CONFLICT | Same Secret already exists |
| 160050 | `SECRET_ENCRYPTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error encrypting/decrypting Secret |
| 160051 | `ACCOUNT_NOT_ACTIVE` | 400 BAD_REQUEST | This account is not active |
| 160052 | `ACCOUNT_ACTIVATION_FAILED` | 400 BAD_REQUEST | Account activation failed |
| 160053 | `ROLE_NOT_FOUND` | 400 BAD_REQUEST | Role not found |
| 160054 | `ACCOUNT_DELETION_ERROR` | 400 BAD_REQUEST | Failed to delete account. |
| 160055 | `USER_NAME_NOT_SET` | 400 BAD_REQUEST | User name not set. |
| 160056 | `SECRET_DELETION_FAILED` | 400 BAD_REQUEST | Failed to delete secret. |
| 160057 | `USER_SEARCH_NOT_ALLOWED` | 400 BAD_REQUEST | Search not allowed. |
| 160058 | `FAILED_TO_GENERATE_QR_CODE` | 417 EXPECTATION_FAILED | Failed to generate QR code. |
| 160059 | `INVALID_OTP` | 400 BAD_REQUEST | Invalid OTP. |
| 160060 | `USER_ACCOUNT_HANDLER_CREATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during user account create handler. |
| 160061 | `USER_ACCOUNT_HANDLER_UPDATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during user account update handler. |
| 160062 | `USER_ACCOUNT_HANDLER_REMOVE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during user account remove handler. |
| 160063 | `OPERATION_NOT_ALLOWED` | 400 BAD_REQUEST | Operation not allowed on user |
| 160064 | `ACCOUNT_REJECTION_FAILED` | 400 BAD_REQUEST | Account rejection failed |
| 160065 | `SECRET_CREATION_FAILED` | 500 INTERNAL_SERVER_ERROR | Secret creation failed |
| 160066 | `ENV_VAR_INVALID_NAME` | 400 BAD_REQUEST | Environment variable name is invalid. |
| 160067 | `ENV_VAR_RESERVED_NAME` | 400 BAD_REQUEST | Environment variable name is reserved. |
| 160068 | `ENV_VAR_VALUE_TOO_LARGE` | 400 BAD_REQUEST | Environment variable value is too large. |
| 160069 | `ENV_VAR_LIMIT_EXCEEDED` | 400 BAD_REQUEST | Environment variable limit exceeded. |
| 160070 | `ENV_VAR_NOT_FOUND` | 404 NOT_FOUND | Environment variable was not found. |
| 160071 | `ENV_VAR_ENCRYPTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error encrypting/decrypting environment variable. |
| 160072 | `SECRET_VALUE_TOO_LARGE` | 400 BAD_REQUEST | Secret value is too large. |
| 160073 | `ENV_VAR_INVALID_VALUE` | 400 BAD_REQUEST | Environment variable value is invalid. |

## MetadataErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 180000 | `TEMPLATE_ALREADY_AVAILABLE` | 400 BAD_REQUEST | The template is already available |
| 180001 | `TEMPLATE_INODEID_EMPTY` | 400 BAD_REQUEST | The template id is empty |
| 180002 | `TEMPLATE_NOT_ATTACHED` | 400 BAD_REQUEST | The template could not be attached to a file |
| 180003 | `DATASET_TEMPLATE_INFO_MISSING` | 400 BAD_REQUEST | Template info is missing. Please provide InodeDTO path and templateId. |
| 180004 | `NO_METADATA_EXISTS` | 400 BAD_REQUEST | No metadata found |
| 180005 | `METADATA_MAX_SIZE_EXCEEDED` | 400 BAD_REQUEST | Metadata is too large |
| 180006 | `METADATA_MISSING_FIELD` | 400 BAD_REQUEST | Metadata missing attributed name. |
| 180007 | `METADATA_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while processing the extended metadata. |
| 180008 | `METADATA_ILLEGAL_NAME` | 400 BAD_REQUEST | Metadata name is illegal. |

## KafkaErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 190000 | `TOPIC_NOT_FOUND` | 404 NOT_FOUND | No topics found |
| 190001 | `BROKER_METADATA_ERROR` | 500 INTERNAL_SERVER_ERROR | An error occurred while retrieving topic metadata from broker |
| 190002 | `TOPIC_ALREADY_EXISTS` | 409 CONFLICT | Kafka topic already exists in database. Pick a different topic name |
| 190003 | `TOPIC_ALREADY_EXISTS_IN_ZOOKEEPER` | 409 CONFLICT | Kafka topic already exists in ZooKeeper. Pick a different topic name |
| 190004 | `TOPIC_LIMIT_REACHED` | 412 PRECONDITION_FAILED | Topic limit reached. Contact your administrator to increase the number of topics that can be created for this project. |
| 190005 | `TOPIC_REPLICATION_ERROR` | 400 BAD_REQUEST | Maximum topic replication factor exceeded |
| 190006 | `SCHEMA_NOT_FOUND` | 404 NOT_FOUND | Topic has no schema attached to it. |
| 190007 | `KAFKA_GENERIC_ERROR` | 500 INTERNAL_SERVER_ERROR | An error occurred while retrieving information about Kafka |
| 190008 | `DESTINATION_PROJECT_IS_TOPIC_OWNER` | 400 BAD_REQUEST | Destination projet is topic owner |
| 190009 | `TOPIC_ALREADY_SHARED` | 400 BAD_REQUEST | Topic is already shared |
| 190010 | `TOPIC_NOT_SHARED` | 404 NOT_FOUND | Topic is not shared with project |
| 190011 | `ACL_ALREADY_EXISTS` | 409 CONFLICT | ACL already exists. |
| 190012 | `ACL_NOT_FOUND` | 404 NOT_FOUND | ACL not found. |
| 190013 | `ACL_NOT_FOR_TOPIC` | 400 BAD_REQUEST | ACL does not belong to the specified topic |
| 190014 | `SCHEMA_IN_USE` | 412 PRECONDITION_FAILED | Schema is currently used by topics. topic |
| 190015 | `BAD_NUM_PARTITION` | 400 BAD_REQUEST | Invalid number of partitions |
| 190016 | `CREATE_SUBJECT_RESERVED_NAME` | 405 METHOD_NOT_ALLOWED | The provided subject name is reserved for system calls |
| 190017 | `DELETE_RESERVED_SCHEMA` | 405 METHOD_NOT_ALLOWED | The schema is reserved and cannot be deleted |
| 190018 | `SCHEMA_VERSION_NOT_FOUND` | 404 NOT_FOUND | Specified version of the schema not found |
| 190019 | `PROJECT_IS_NOT_THE_OWNER_OF_THE_TOPIC` | 400 BAD_REQUEST | Specified project is not the owner of the topic |
| 190020 | `ACL_FOR_ANY_USER` | 400 BAD_REQUEST | Cannot create an ACL for user with email '*' |
| 190021 | `KAFKA_UNAVAILABLE` | 503 SERVICE_UNAVAILABLE | Kafka is temporarily unavailable. Please try again later |
| 190022 | `TOPIC_DELETION_FAILED` | 500 INTERNAL_SERVER_ERROR | Could not delete Kafka topics. |
| 190023 | `TOPIC_FETCH_FAILED` | 500 INTERNAL_SERVER_ERROR | Could not fetch topic details. |
| 190024 | `TOPIC_CREATION_FAILED` | 500 INTERNAL_SERVER_ERROR | Could not create topic. |
| 190025 | `BROKER_MISSING` | 404 NOT_FOUND | Could not find a broker endpoint. |

## SecurityErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 200001 | `MASTER_ENCRYPTION_PASSWORD_CHANGE` | 400 BAD_REQUEST | Master password change procedure started. Check your inbox for final status |
| 200002 | `HDFS_ACCESS_CONTROL` | 403 FORBIDDEN | Access error while trying to access hdfs resource |
| 200003 | `EJB_ACCESS_LOCAL` | 401 UNAUTHORIZED | Unauthorized invocation |
| 200004 | `CERT_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while generating certificates. |
| 200005 | `CERT_CN_EXTRACT_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while extracting CN from certificate. |
| 200006 | `CERT_ERROR` | 401 UNAUTHORIZED | Certificate could not be validated. |
| 200007 | `CERT_ACCESS_DENIED` | 403 FORBIDDEN | Certificate access denied. |
| 200008 | `CSR_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while signing CSR. |
| 200009 | `CERT_APP_REVOKE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while revoking application certificate, check the logs |
| 200010 | `CERT_MATERIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | CertificateMaterializer error, could not materialize certificates |
| 200011 | `MASTER_ENCRYPTION_PASSWORD_ACCESS_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not read master encryption password. |
| 200012 | `NOT_RENEWABLE_TOKEN` | 400 BAD_REQUEST | Token can not be renewed. |
| 200013 | `INVALIDATION_ERROR` | 417 EXPECTATION_FAILED | Error while invalidating token. |
| 200014 | `REST_ACCESS_CONTROL` | 403 FORBIDDEN | Client not authorized for this invocation. |
| 200015 | `DUPLICATE_KEY_ERROR` | 409 CONFLICT | A signing key with the same name already exists. |
| 200016 | `CERTIFICATE_REVOKATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error revoking the certificate |
| 200017 | `CERTIFICATE_NOT_FOUND` | 400 BAD_REQUEST | Could not find the certificate |
| 200018 | `CERTIFICATE_REVOKATION_USER_ERR` | 400 BAD_REQUEST | Error revoking the certificate |
| 200019 | `CERTIFICATE_SIGN_USER_ERR` | 400 BAD_REQUEST | Error signing the certificate |
| 200020 | `MASTER_ENCRYPTION_PASSWORD_RESET_ERROR` | 500 INTERNAL_SERVER_ERROR | Error resetting master encryption password. |

## CAErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 220000 | `BADSIGNREQUEST` | 400 BAD_REQUEST | No CSR provided or CSR is malformed |
| 220001 | `BADREVOKATIONREQUEST` | 400 BAD_REQUEST | No certificate identifier provided |
| 220002 | `CERTNOTFOUND` | 204 NO_CONTENT | Certificate not found |
| 220003 | `CERTEXISTS` | 400 BAD_REQUEST | Certificate with the same identifier already exists |
| 220004 | `BAD_SUBJECT_NAME` | 400 BAD_REQUEST | Invalid certificate subject name |
| 220005 | `CERTIFICATE_DECODING_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not decode certificate |
| 220006 | `CERTIFICATE_REVOCATION_FAILURE` | 500 INTERNAL_SERVER_ERROR | Failed to revoke certificate |
| 220007 | `CERTIFICATE_REVOCATION_LIST_READ` | 500 INTERNAL_SERVER_ERROR | Failed to read Certificate Revocation List |
| 220008 | `CSR_GENERIC_ERROR` | 500 INTERNAL_SERVER_ERROR | Error handling certificate signing request |
| 220009 | `CSR_SIGNING_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not sign Certificate Signing Request |
| 220010 | `CA_INITIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while initializing Certificate Authorities |
| 220011 | `PKI_GENERIC_ERROR` | 500 INTERNAL_SERVER_ERROR | Generic PKI error |

## DelaCSRErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 230000 | `BADREQUEST` | 400 BAD_REQUEST | User or CS not set |
| 230001 | `EMAIL` | 401 UNAUTHORIZED | CSR email not set or does not match user |
| 230003 | `CN` | 400 BAD_REQUEST | CSR common name not set |
| 230004 | `O` | 400 BAD_REQUEST | CSR organization name not set |
| 230005 | `OU` | 400 BAD_REQUEST | CSR organization unit name not set |
| 230006 | `NOTFOUND` | 400 BAD_REQUEST | No cluster registered with the given organization name and organizational unit |
| 230007 | `SERIALNUMBER` | 400 BAD_REQUEST | Cluster has already a signed certificate |
| 230008 | `CNNOTFOUND` | 400 BAD_REQUEST | No cluster registered with the CSR common name |
| 230009 | `AGENTIDNOTFOUND` | 401 UNAUTHORIZED | No cluster registered for the user |

## ServingErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 240000 | `INSTANCE_NOT_FOUND` | 404 NOT_FOUND | Serving instance not found |
| 240001 | `DELETION_ERROR` | 500 INTERNAL_SERVER_ERROR | Serving instance could not be deleted |
| 240002 | `UPDATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Serving instance could not be updated |
| 240003 | `LIFECYCLE_ERROR` | 400 BAD_REQUEST | Serving instance could not be started/stopped |
| 240004 | `LIFECYCLE_ERROR_INT` | 500 INTERNAL_SERVER_ERROR | Serving instance could not be started/stopped |
| 240005 | `STATUS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error getting model server instance status |
| 240006 | `MODEL_PATH_NOT_FOUND` | 400 BAD_REQUEST | Model path not found |
| 240007 | `COMMAND_NOT_RECOGNIZED` | 400 BAD_REQUEST | Command not recognized |
| 240008 | `COMMAND_NOT_PROVIDED` | 400 BAD_REQUEST | Command not provided |
| 240009 | `SPEC_NOT_PROVIDED` | 400 BAD_REQUEST | TFServing spec not provided |
| 240010 | `BAD_TOPIC` | 400 BAD_REQUEST | Topic provided cannot be used for Serving logging |
| 240011 | `DUPLICATED_ENTRY` | 400 BAD_REQUEST | An entry with the same name already exists in this project |
| 240012 | `PYTHON_ENVIRONMENT_NOT_ENABLED` | 400 BAD_REQUEST | Python environment has not been enabled in this project, which is required for serving SkLearn Models |
| 240013 | `UPDATE_MODEL_SERVER_ERROR` | 400 BAD_REQUEST | The model server of a deployment cannot be updated. |
| 240014 | `KUBERNETES_NOT_INSTALLED` | 400 BAD_REQUEST | Kubernetes is not installed |
| 240015 | `KSERVE_NOT_ENABLED` | 400 BAD_REQUEST | KServe is not installed or disabled |
| 240016 | `SCRIPT_NOT_FOUND` | 400 BAD_REQUEST | Script not found |
| 240017 | `MODEL_FILES_STRUCTURE_NOT_VALID` | 400 BAD_REQUEST | Model path does not have a valid file structure |
| 240018 | `MODEL_ARTIFACT_NOT_VALID` | 400 BAD_REQUEST | Model artifact not valid |
| 240019 | `MODEL_ARTIFACT_OPERATION_ERROR` | 400 BAD_REQUEST | Model artifact cannot be created or changed |
| 240020 | `PREDICTOR_NOT_SUPPORTED` | 400 BAD_REQUEST | Predictors not supported |
| 240021 | `TRANSFORMER_NOT_SUPPORTED` | 400 BAD_REQUEST | Transformers not supported |
| 240022 | `KAFKA_TOPIC_NOT_FOUND` | 400 BAD_REQUEST | Kafka topic not found |
| 240023 | `KAFKA_TOPIC_NOT_VALID` | 400 BAD_REQUEST | Kafka topic not valid |
| 240024 | `FINEGRAINED_INF_LOGGING_NOT_SUPPORTED` | 400 BAD_REQUEST | Fine-grained inference logging not supported |
| 240025 | `REQUEST_BATCHING_NOT_SUPPORTED` | 400 BAD_REQUEST | Request batching not supported |
| 240026 | `CREATE_ERROR` | 400 BAD_REQUEST | Serving instance could not be created |
| 240027 | `SERVER_LOGS_NOT_AVAILABLE` | 404 NOT_FOUND | Server logs not available |
| 240028 | `API_PROTOCOL_NOT_SUPPORTED` | 400 BAD_REQUEST | GRPC only supported in KServe deployments |
| 240029 | `SCHEDULING_CONFIG_ERROR` | 400 BAD_REQUEST | Scheduling configuration error |
| 240030 | `UNSUPPORTED_MODELLESS_SERVING_TYPE` | 400 BAD_REQUEST | Modelless serving type not supported |
| 240031 | `RESERVED_ENV_VAR_NAME` | 400 BAD_REQUEST | One or more environment variable names are reserved by the Hopsworks platform. |
| 240032 | `VLLM_VERSION_NOT_AVAILABLE` | 400 BAD_REQUEST | vLLM version not available |

## InferenceErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 250000 | `SERVING_NOT_FOUND` | 404 NOT_FOUND | Serving instance not found |
| 250001 | `SERVING_NOT_RUNNING` | 400 BAD_REQUEST | Serving instance not running |
| 250002 | `REQUEST_ERROR` | 500 INTERNAL_SERVER_ERROR | Error contacting the serving server |
| 250003 | `EMPTY_RESPONSE` | 500 INTERNAL_SERVER_ERROR | Empty response from the serving server |
| 250004 | `BAD_REQUEST` | 400 BAD_REQUEST | Request malformed |
| 250005 | `MISSING_VERB` | 400 BAD_REQUEST | Verb is missing |
| 250006 | `ERROR_READING_RESPONSE` | 500 INTERNAL_SERVER_ERROR | Error while reading the response |
| 250007 | `SERVING_INSTANCE_INTERNAL` | 500 INTERNAL_SERVER_ERROR | Serving instance internal error |
| 250008 | `SERVING_INSTANCE_BAD_REQUEST` | 400 BAD_REQUEST | Serving instance bad request error |
| 250009 | `REQUEST_AUTH_TYPE_NOT_SUPPORTED` | 400 BAD_REQUEST | Authentication type not supported |
| 250010 | `UNAUTHORIZED` | 401 UNAUTHORIZED | Unauthorized request |
| 250011 | `FORBIDDEN` | 403 FORBIDDEN | Forbidden request |
| 250012 | `ENDPOINT_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Inference endpoint not found |

## ActivitiesErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 260000 | `FORBIDDEN` | 403 FORBIDDEN | You are not allow to perform this action. |
| 260001 | `ACTIVITY_NOT_FOUND` | 404 NOT_FOUND | Activity instance not found |
| 260002 | `ACTIVITY_NOT_SUPPORTED` | 400 BAD_REQUEST | Activity type not supported |

## FeaturestoreErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 270001 | `COULD_NOT_CREATE_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not create feature group and corresponding online/offline store. |
| 270002 | `FEATURESTORE_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Featurestore Id was not provided |
| 270003 | `FEATUREGROUP_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Featuregroup Id was not provided |
| 270004 | `FEATUREGROUP_VERSION_NOT_PROVIDED` | 400 BAD_REQUEST | Featuregroup version was not provided |
| 270005 | `COULD_NOT_DELETE_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not delete feature group and corresponding Hive table |
| 270006 | `COULD_NOT_CREATE_FEATURESTORE` | 500 INTERNAL_SERVER_ERROR | Could not create feature store and corresponding Hive database |
| 270007 | `COULD_NOT_PREVIEW_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not preview the contents of the feature group |
| 270008 | `FEATURESTORE_NOT_FOUND` | 404 NOT_FOUND | Featurestore wasn't found. |
| 270009 | `FEATUREGROUP_NOT_FOUND` | 404 NOT_FOUND | Featuregroup wasn't found. |
| 270010 | `COULD_NOT_FETCH_FEATUREGROUP_SHOW_CREATE_SCHEMA` | 500 INTERNAL_SERVER_ERROR | The query SHOW CREATE SCHEMA for the featuregroup in Hive failed. |
| 270011 | `FEATURE_STORE_NOT_SHARED` | 400 BAD_REQUEST | Trying to un-share a featurestore that is not shared |
| 270012 | `TRAINING_DATASET_NOT_FOUND` | 404 NOT_FOUND | Training dataset wasn't found. |
| 270013 | `TRAINING_DATASET_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Training dataset Id was not provided |
| 270014 | `COULD_NOT_DELETE_TRAINING_DATASET` | 500 INTERNAL_SERVER_ERROR | Could not delete training dataset |
| 270015 | `CLONE_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Clone Id not provided despite requesting to clone feature group version |
| 270016 | `TRAINING_DATASET_ALREADY_EXISTS` | 400 BAD_REQUEST | The provided training dataset name already exists |
| 270017 | `NO_PRIMARY_KEY_SPECIFIED` | 400 BAD_REQUEST | A feature group or training dataset must have a primary key specified |
| 270018 | `CERTIFICATES_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Could not find user certificates for authenticating with Hive Feature Store |
| 270019 | `COULD_NOT_INITIATE_HIVE_CONNECTION` | 500 INTERNAL_SERVER_ERROR | Could not initiate connection to Hive Server |
| 270020 | `HIVE_UPDATE_STATEMENT_ERROR` | 500 INTERNAL_SERVER_ERROR | Hive Update Statement failed |
| 270021 | `HIVE_READ_QUERY_ERROR` | 500 INTERNAL_SERVER_ERROR | Hive Read Query failed |
| 270023 | `FEATURESTORE_NAME_NOT_PROVIDED` | 400 BAD_REQUEST | Featurestore name was not provided |
| 270024 | `FORBIDDEN_FEATURESTORE_OPERATION` | 403 FORBIDDEN | User is forbidden to enact these changes |
| 270025 | `STORAGE_CONNECTOR_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Storage backend id not provided |
| 270026 | `CANNOT_FETCH_HIVE_SCHEMA_FOR_ON_DEMAND_FEATUREGROUPS` | 400 BAD_REQUEST | Fetching Hive Schema of On-demand feature groups is not supported |
| 270027 | `ON_DEMAND_FEATUREGROUP_JDBC_CONNECTOR_NOT_FOUND` | 404 NOT_FOUND | The JDBC Connector for the on-demand feature group could not be found |
| 270028 | `PREVIEW_NOT_SUPPORTED_FOR_ON_DEMAND_FEATUREGROUPS` | 400 BAD_REQUEST | Fetching Hive Schema of On-demand feature groups is not supported |
| 270029 | `CLEAR_OPERATION_NOT_SUPPORTED_FOR_ON_DEMAND_FEATUREGROUPS` | 400 BAD_REQUEST | Clearing Feature Group contents is not supported for on-demand feature groups |
| 270030 | `ILLEGAL_STORAGE_CONNECTOR_NAME` | 400 BAD_REQUEST | Illegal storage connector name |
| 270031 | `ILLEGAL_STORAGE_CONNECTOR_DESCRIPTION` | 400 BAD_REQUEST | Illegal storage connector description |
| 270032 | `ILLEGAL_JDBC_CONNECTION_STRING` | 400 BAD_REQUEST | Illegal JDBC Connection String |
| 270033 | `ILLEGAL_JDBC_CONNECTION_ARGUMENTS` | 400 BAD_REQUEST | Illegal JDBC Connection Arguments |
| 270034 | `ILLEGAL_S3_CONNECTOR_BUCKET` | 400 BAD_REQUEST | Illegal S3 connector bucket |
| 270035 | `ILLEGAL_S3_CONNECTOR_ACCESS_KEY` | 400 BAD_REQUEST | Illegal S3 connector access key |
| 270036 | `ILLEGAL_S3_CONNECTOR_SECRET_KEY` | 400 BAD_REQUEST | Illegal S3 connector secret key |
| 270037 | `ILLEGAL_HOPSFS_CONNECTOR_DATASET` | 400 BAD_REQUEST | Illegal Hopsfs connector dataset |
| 270040 | `ILLEGAL_FEATURE_NAME` | 400 BAD_REQUEST | Illegal feature name |
| 270041 | `ILLEGAL_FEATURE_DESCRIPTION` | 400 BAD_REQUEST | Illegal feature description |
| 270042 | `CONNECTOR_NOT_FOUND` | 404 NOT_FOUND | Connector not found |
| 270043 | `CONNECTOR_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Connector Id was not provided |
| 270044 | `INVALID_SQL_QUERY` | 400 BAD_REQUEST | Invalid SQL query |
| 270046 | `HOPSFS_CONNECTOR_NOT_FOUND` | 404 NOT_FOUND | HopsFs Connector not found |
| 270047 | `STORAGE_CONNECTOR_TYPE_NOT_PROVIDED` | 400 BAD_REQUEST | Storage Connector Type was not provided |
| 270048 | `COULD_NOT_CLEAR_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not clear contents of feature group |
| 270049 | `ILLEGAL_FEATUREGROUP_TYPE` | 400 BAD_REQUEST | The provided feature group type was not recognized |
| 270050 | `ILLEGAL_TRAINING_DATASET_TYPE` | 400 BAD_REQUEST | The provided training dataset type was not recognized |
| 270051 | `CAN_ONLY_GET_INODE_FOR_HOPSFS_TRAINING_DATASETS` | 400 BAD_REQUEST | Getting the inode id of a non-hopsfs training dataset is not supported |
| 270052 | `TRAINING_DATASET_VERSION_NOT_PROVIDED` | 400 BAD_REQUEST | Training Dataset version was not provided |
| 270054 | `S3_CONNECTOR_ID_NOT_PROVIDED` | 400 BAD_REQUEST | S3 Connector Id was not provided |
| 270055 | `HOPSFS_CONNECTOR_ID_NOT_PROVIDED` | 400 BAD_REQUEST | HopsFS Connector Id was not provided |
| 270057 | `ILLEGAL_TRAINING_DATASET_DATA_FORMAT` | 400 BAD_REQUEST | Illegal training dataset data format |
| 270058 | `ILLEGAL_TRAINING_DATASET_VERSION` | 400 BAD_REQUEST | Illegal training dataset version |
| 270059 | `ILLEGAL_FEATUREGROUP_VERSION` | 400 BAD_REQUEST | Illegal feature group version |
| 270060 | `ILLEGAL_STORAGE_CONNECTOR_TYPE` | 400 BAD_REQUEST | The provided storage connector type is not valid |
| 270061 | `FEATURESTORE_INITIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Featurestore Initialization Error |
| 270062 | `FEATURESTORE_UTIL_ARGS_FAILURE` | 500 INTERNAL_SERVER_ERROR | Could not write featurestore util args to HDFS |
| 270063 | `FEATURESTORE_ONLINE_SECRETS_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not get JDBC connection for the online featurestore |
| 270064 | `FEATURESTORE_ONLINE_NOT_ENABLED` | 400 BAD_REQUEST | Online featurestore not enabled |
| 270065 | `SYNC_TABLE_NOT_FOUND` | 400 BAD_REQUEST | The Hive Table to Sync with the feature store was not found in the metastore |
| 270066 | `COULD_NOT_INITIATE_MYSQL_CONNECTION_TO_ONLINE_FEATURESTORE` | 500 INTERNAL_SERVER_ERROR | Could not initiate connection to MySQL Server |
| 270067 | `MYSQL_JDBC_UPDATE_STATEMENT_ERROR` | 500 INTERNAL_SERVER_ERROR | MySQL JDBC Update Statement failed |
| 270068 | `MYSQL_JDBC_READ_QUERY_ERROR` | 500 INTERNAL_SERVER_ERROR | MySQL JDBC Read Query failed |
| 270069 | `ONLINE_FEATURE_SERVING_NOT_SUPPORTED_FOR_ON_DEMAND_FEATUREGROUPS` | 400 BAD_REQUEST | Online Feature Serving is onlysupported for feature groups that are cached inside Hopsworks |
| 270070 | `ERROR_CREATING_ONLINE_FEATURESTORE_DB` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to create the MySQL database for an online feature store |
| 270071 | `ERROR_CREATING_ONLINE_FEATURESTORE_USER` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to create the MySQL database user for an online feature store |
| 270072 | `ERROR_DELETING_ONLINE_FEATURESTORE_DB` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to delete the MySQL database for an online feature store |
| 270073 | `ERROR_DELETING_ONLINE_FEATURESTORE_USER` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to delete the MySQL user for an online feature store |
| 270074 | `ERROR_GRANTING_ONLINE_FEATURESTORE_USER_PRIVILEGES` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to grant/revoke privileges to a MySQL user for an online feature store |
| 270075 | `ONLINE_FEATUREGROUP_CANNOT_BE_PARTITIONED` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to create the MySQL table for the online feature group. User-defined partitioning is not supported for MySQL tables |
| 270076 | `COULD_NOT_CREATE_DATA_VALIDATION_RULES` | 500 INTERNAL_SERVER_ERROR | Failed to create data validation rules |
| 270077 | `COULD_NOT_READ_DATA_VALIDATION_RESULT` | 500 INTERNAL_SERVER_ERROR | Failed to read data validation result |
| 270078 | `IMPORT_JOB_ALREADY_RUNNING` | 400 BAD_REQUEST | A job to import this featuregroup is already running |
| 270079 | `IMPORT_CONF_ERROR` | 500 INTERNAL_SERVER_ERROR | Error writing import job configuration |
| 270080 | `TRAININGDATASETJOB_FAILURE` | 500 INTERNAL_SERVER_ERROR | Could not write featurestore cloud args to HDFS |
| 270081 | `TRAININGDATASETJOB_DUPLICATE_FEATURE` | 400 BAD_REQUEST | Feature list contains duplicate |
| 270082 | `FEATURE_DOES_NOT_EXIST` | 400 BAD_REQUEST | Feature does not exist |
| 270083 | `TRAININGDATASETJOB_FEATUREGROUP_DUPLICATE` | 400 BAD_REQUEST | Multiple featuregroups contain feature |
| 270084 | `TRAININGDATASETJOB_TRAININGDATASET_VERSION_EXISTS` | 400 BAD_REQUEST | Illegal training dataset name - version combination |
| 270085 | `TRAININGDATASETJOB_CONF_ERROR` | 500 INTERNAL_SERVER_ERROR | Error writing training dataset job configuration to hdfs |
| 270086 | `S3_KEYS_FORBIDDEN` | 400 BAD_REQUEST | IAM role is configured for this instance. AWS access/secret keys are not allowed |
| 270087 | `MISSING_REDSHIFT_DRIVER` | 400 BAD_REQUEST | Could not find Redshift JDBC driver. Please upload it in Resources/RedshiftJDBC42-no-awssdk.jar |
| 270088 | `TRAININGDATASETJOB_MISSPECIFICATION` | 400 BAD_REQUEST | Training dataset job is misspecified and cannot be created |
| 270089 | `FEATUREGROUP_EXISTS` | 400 BAD_REQUEST | The feature group you are trying to create does already exist. |
| 270090 | `XATTRS_OPERATIONS_ONLY_SUPPORTED_FOR_CACHED_FEATUREGROUPS` | 400 BAD_REQUEST | Attaching extended attributes is only supported for cached featuregroups. |
| 270091 | `ILLEGAL_ENTITY_NAME` | 400 BAD_REQUEST | Illegal feature store entity name |
| 270092 | `ILLEGAL_ENTITY_DESCRIPTION` | 400 BAD_REQUEST | Illegal featurestore entity description |
| 270094 | `FEATUREGROUP_NAME_NOT_PROVIDED` | 400 BAD_REQUEST | Feature group name was not provided |
| 270095 | `TRAINING_DATASET_NAME_NOT_PROVIDED` | 400 BAD_REQUEST | Training dataset name was not provided |
| 270096 | `NO_PK_JOINING_KEYS` | 400 BAD_REQUEST | Could not find any matching feature to join |
| 270097 | `LEFT_RIGHT_ON_DIFF_SIZES` | 400 BAD_REQUEST | LeftOn and RightOn have different sizes |
| 270098 | `ILLEGAL_TRAINING_DATASET_SPLIT_NAME` | 400 BAD_REQUEST | Illegal training dataset split name |
| 270099 | `ILLEGAL_TRAINING_DATASET_SPLIT_PERCENTAGE` | 400 BAD_REQUEST | Illegal training dataset split percentage |
| 270100 | `TAG_NOT_ALLOWED` | 400 BAD_REQUEST | The provided tag is not allowed |
| 270101 | `TAG_NOT_FOUND` | 404 NOT_FOUND | The provided tag is not attached |
| 270102 | `FEATUREGROUP_NOT_ONLINE` | 400 BAD_REQUEST | The feature group is not available online |
| 270103 | `FEATUREGROUP_ONDEMAND_NO_PARTS` | 400 BAD_REQUEST | Partitions not available for on demand feature group |
| 270104 | `ILLEGAL_S3_CONNECTOR_SERVER_ENCRYPTION_ALGORITHM` | 400 BAD_REQUEST | Illegal server encryption algorithm provided |
| 270105 | `ILLEGAL_S3_CONNECTOR_SERVER_ENCRYPTION_KEY` | 400 BAD_REQUEST | Illegal server encryption key provided |
| 270106 | `TRAINING_DATASET_DUPLICATE_SPLIT_NAMES` | 400 BAD_REQUEST | Duplicate split names in training dataset provided. |
| 270107 | `STATISTICS_READ_ERROR` | 500 INTERNAL_SERVER_ERROR | Error reading the statistics |
| 270108 | `ILLEGAL_STATISTICS_CONFIG` | 400 BAD_REQUEST | Illegal statistics config |
| 270109 | `ERROR_DELETING_STATISTICS` | 500 INTERNAL_SERVER_ERROR | Error deleting the statistics of a feature store entity |
| 270110 | `ERROR_GETTING_S3_CONNECTOR_ACCESS_AND_SECRET_KEY_FROM_SECRET` | 500 INTERNAL_SERVER_ERROR | Could not get access and secret key from the user secret |
| 270111 | `TRAINING_DATASET_NO_QUERY` | 400 BAD_REQUEST | The training dataset wasn't generated from a query |
| 270112 | `TRAINING_DATASET_NO_SCHEMA` | 400 BAD_REQUEST | No query or feature schema provided |
| 270113 | `QUERY_FAILED_FG_DELETED` | 400 BAD_REQUEST | Cannot generate query, some feature groups were deleted |
| 270114 | `ILLEGAL_FEATUREGROUP_UPDATE` | 400 BAD_REQUEST | Illegal feature group update |
| 270115 | `COULD_NOT_ALTER_FEAUTURE_GROUP_METADATA` | 500 INTERNAL_SERVER_ERROR | Failed to alter feature group meta data |
| 270116 | `COULD_NOT_GET_FEATURE_GROUP_METADATA` | 500 INTERNAL_SERVER_ERROR | Failed to retrieve feature group meta data |
| 270117 | `ERROR_CREATING_HIVE_METASTORE_CLIENT` | 500 INTERNAL_SERVER_ERROR | Failed to open Hive Metastore client |
| 270118 | `NO_DATA_AVAILABLE_FEATUREGROUP_COMMITDATE` | 404 NOT_FOUND | No data is available for feature group with this commit date |
| 270119 | `PROVIDED_DATE_FORMAT_NOT_SUPPORTED` | 400 BAD_REQUEST | Invalid date format |
| 270120 | `ONLINE_FEATURESTORE_JDBC_CONNECTOR_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Online featurestore JDBC connector not found |
| 270121 | `PRIMARY_KEY_REQUIRED` | 400 BAD_REQUEST | Primary key is required when using Hudi time travel format |
| 270122 | `DATABRICKS_INSTANCE_ALREADY_EXISTS` | 409 CONFLICT | Databricks Instance already registered |
| 270123 | `DATABRICKS_INSTANCE_NOT_EXISTS` | 404 NOT_FOUND | Databricks Instance doesn't exists |
| 270124 | `DATABRICKS_CANNOT_START_CLUSTER` | 500 INTERNAL_SERVER_ERROR | Could not start Databricks cluster |
| 270125 | `DATABRICKS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error communicating with Databricks |
| 270126 | `STORAGE_CONNECTOR_GET_ERROR` | 500 INTERNAL_SERVER_ERROR | Error retrieving the storage connector |
| 270127 | `ERROR_ONLINE_FEATURES` | 500 INTERNAL_SERVER_ERROR | Error retrieving online features |
| 270128 | `ERROR_ONLINE_USERS` | 500 INTERNAL_SERVER_ERROR | Error getting database users |
| 270129 | `ERROR_ONLINE_GENERIC` | 500 INTERNAL_SERVER_ERROR | Error communicating with the online feature store |
| 270130 | `COULD_NOT_CREATE_ON_DEMAND_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not create on demand feature group |
| 270131 | `COULD_NOT_DELETE_ON_DEMAND_FEATUREGROUP` | 500 INTERNAL_SERVER_ERROR | Could not delete on demand feature group |
| 270132 | `ILLEGAL_FEATURE_GROUP_FEATURE_DEFAULT_VALUE` | 400 BAD_REQUEST | Illegal feature default value |
| 270133 | `KEYWORD_ERROR` | 500 INTERNAL_SERVER_ERROR | Keyword error for feature group/training dataset |
| 270134 | `KEYWORD_FORMAT_ERROR` | 400 BAD_REQUEST | Keyword format error |
| 270135 | `REDSHIFT_CONNECTOR_NOT_FOUND` | 404 NOT_FOUND | Redshift Connector not found |
| 270136 | `ILLEGAL_STORAGE_CONNECTOR_ARG` | 400 BAD_REQUEST | Illegal storage connector argument |
| 270137 | `ERROR_SAVING_STATISTICS` | 400 BAD_REQUEST | Error saving statistics |
| 270138 | `FILTER_CONSTRUCTION_ERROR` | 500 INTERNAL_SERVER_ERROR | Failed to construct filter condition |
| 270139 | `ILLEGAL_FILTER_ARGUMENTS` | 400 BAD_REQUEST | Malformed filter conditions for Query |
| 270140 | `ILLEGAL_ON_DEMAND_DATA_FORMAT` | 400 BAD_REQUEST | Illegal on-demand feature group data format |
| 270141 | `ERROR_JOB_SETUP` | 500 INTERNAL_SERVER_ERROR | Error setting up feature store job |
| 270142 | `LABEL_NOT_FOUND` | 404 NOT_FOUND | Could not find label in training dataset schema |
| 270143 | `DATA_VALIDATION_RESULTS_NOT_FOUND` | 404 NOT_FOUND | Could not find feature group validation results. Make sure the results file was not manually removed from the dataset |
| 270144 | `DATA_VALIDATION_NOT_FOUND` | 404 NOT_FOUND | Could not find feature group validation. |
| 270145 | `FEATURE_STORE_EXPECTATION_NOT_FOUND` | 404 NOT_FOUND | Could not find feature store expectation. |
| 270146 | `FEATURE_GROUP_EXPECTATION_NOT_FOUND` | 404 NOT_FOUND | Could not find feature group expectation. |
| 270147 | `FEATURE_GROUP_EXPECTATION_FEATURE_NOT_FOUND` | 404 NOT_FOUND | Could not find expectation feature(s) in feature group expectation. |
| 270148 | `FEATURE_STORE_RULE_NOT_FOUND` | 404 NOT_FOUND | Could not find feature store data validation rule. |
| 270149 | `FEATURE_GROUP_CHECKS_FAILED` | 417 EXPECTATION_FAILED | Feature group validation checks did not pass, will not persist the data. |
| 270150 | `RULE_NOT_FOUND` | 404 NOT_FOUND | Rule with provided name was not found. |
| 270151 | `AVRO_PRIMITIVE_TYPE_NOT_SUPPORTED` | 400 BAD_REQUEST | Error converting Hive Type to Avro primitive type |
| 270152 | `AVRO_MAP_STRING_KEY` | 400 BAD_REQUEST | Map types are only supported with STRING type keys |
| 270153 | `AVRO_MALFORMED_SCHEMA` | 500 INTERNAL_SERVER_ERROR | Error converting Hive schema to Avro |
| 270154 | `FEATURE_GROUP_EXPECTATION_FEATURE_TYPE_INVALID` | 400 BAD_REQUEST | Could not attach expectation because some feature types did not match rule types. |
| 270155 | `ALERT_NOT_FOUND` | 404 NOT_FOUND | Alert not found |
| 270156 | `ALERT_ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Alert missing argument. |
| 270157 | `ALERT_ALREADY_EXISTS` | 400 BAD_REQUEST | Alert with the same status already exists. |
| 270158 | `ERROR_DELETING_TRANSFORMERFUNCTION` | 500 INTERNAL_SERVER_ERROR | Error deleting the transformer function of a feature store entity |
| 270159 | `TRANSFORMATION_FUNCTION_ALREADY_EXISTS` | 400 BAD_REQUEST | The provided transformation function name and version already exists |
| 270160 | `TRANSFORMATION_FUNCTION_DOES_NOT_EXIST` | 400 BAD_REQUEST | Transformation function does not exist |
| 270161 | `TRANSFORMATION_FUNCTION_READ_ERROR` | 500 INTERNAL_SERVER_ERROR | Error reading the transformation function |
| 270162 | `TRANSFORMATION_FUNCTION_VERSION` | 400 BAD_REQUEST | Illegal transformation function version |
| 270163 | `ILLEGAL_TRANSFORMATION_FUNCTION_OUTPUT_TYPE` | 400 BAD_REQUEST | Illegal transformation function output type |
| 270164 | `FEATURE_WITH_TRANSFORMATION_NOT_FOUND` | 404 NOT_FOUND | Could not find feature in training dataset schema |
| 270165 | `ILLEGAL_PREFIX_NAME` | 400 BAD_REQUEST | Illegal feature name |
| 270169 | `FAILED_TO_CREATE_ROUTE` | 400 BAD_REQUEST | Failed to create route. |
| 270170 | `FAILED_TO_DELETE_ROUTE` | 400 BAD_REQUEST | Failed to delete route. |
| 270171 | `ILLEGAL_EVENT_TIME_FEATURE_TYPE` | 400 BAD_REQUEST | Illegal event time feature type |
| 270172 | `EVENT_TIME_FEATURE_NOT_FOUND` | 400 BAD_REQUEST | Event time feature not found |
| 270173 | `FEATURE_GROUP_MISSING_EVENT_TIME` | 400 BAD_REQUEST | Feature group is not event time enabled |
| 270174 | `JOIN_OPERATOR_MISMATCH` | 400 BAD_REQUEST | Join features and operator list have different sizes |
| 270175 | `VALIDATION_RULE_INCOMPLETE` | 400 BAD_REQUEST | Rule is missing a required field. |
| 270176 | `COULD_NOT_CREATE_ONLINE_FEATUREGROUP` | 400 BAD_REQUEST | Could not create online feature group |
| 270177 | `COULD_NOT_GET_QUERY_FILTER` | 500 INTERNAL_SERVER_ERROR | Error getting query filter |
| 270178 | `ERROR_REGISTER_BUILTIN_TRANSFORMATION_FUNCTION` | 500 INTERNAL_SERVER_ERROR | This branch should not be reached. Please fix automatic registering of the built-in transformation functions upon project creation |
| 270179 | `FEATURE_VIEW_ALREADY_EXISTS` | 400 BAD_REQUEST | The provided feature view name and version already exists |
| 270180 | `FEATURE_VIEW_CREATION_ERROR` | 400 BAD_REQUEST | Cannot create feature view. |
| 270181 | `FEATURE_VIEW_NOT_FOUND` | 404 NOT_FOUND | Feature view wasn't found. |
| 270182 | `KAFKA_STORAGE_CONNECTOR_STORE_NOT_EXISTING` | 400 BAD_REQUEST | Provided certificate store location does not exist |
| 270183 | `VALIDATION_NOT_SUPPORTED` | 400 BAD_REQUEST | Rule is not supported. |
| 270184 | `STREAM_FEATURE_GROUP_ONLINE_DISABLE_ENABLE` | 400 BAD_REQUEST | Stream feature group cannot be online enabled if it was created as offline only. |
| 270185 | `GCS_FIELD_MISSING` | 400 BAD_REQUEST | Field missing |
| 270186 | `TRAINING_DATASET_COULD_NOT_BE_CREATED` | 500 INTERNAL_SERVER_ERROR | Could not create training dataset |
| 270187 | `NESTED_JOIN_NOT_ALLOWED` | 400 BAD_REQUEST | Nested join is not supported. |
| 270188 | `FEATURE_NOT_FOUND` | 404 NOT_FOUND | Could not find feature. |
| 270189 | `EXPECTATION_TYPE_NOT_FOUND` | 404 NOT_FOUND | Expectation type not supported. |
| 270190 | `EXPECTATION_NOT_FOUND` | 404 NOT_FOUND | Expectation not found. |
| 270191 | `NO_EXPECTATION_SUITE_ATTACHED_TO_THIS_FEATUREGROUP` | 404 NOT_FOUND | No Expectation Suite attached to this feature group. Use fg.save_expectation_suite to attach a Great Expectations suite to your FeatureGroup. |
| 270192 | `VALIDATION_REPORT_NOT_FOUND` | 404 NOT_FOUND | Validation report not found. |
| 270193 | `FAILED_TO_PARSE_EXPECTATION_CONFIG_TO_JSON` | 400 BAD_REQUEST | Failed to parse expectation config field to json. Expectation config must be a valid json to fetch the expectationId from the meta field. |
| 270194 | `KEY_NOT_FOUND_OR_INVALID_VALUE_TYPE_IN_JSON_OBJECT` | 400 BAD_REQUEST | Requested key has not been found in Json object or associated value is not of required type. |
| 270195 | `FAILED_TO_PARSE_VALIDATION_RESULT_FOR_OBSERVED_VALUE` | 400 BAD_REQUEST | Failed to parse result json to get observed_value field |
| 270196 | `FAILED_TO_PARSE_EXPECTATION_META_FIELD` | 400 BAD_REQUEST | Failed to parse expectation meta field. |
| 270197 | `VALIDATION_REPORT_IS_NOT_VALID_JSON` | 400 BAD_REQUEST | Validation report is not a valid JSON. |
| 270198 | `ERROR_SAVING_ON_DISK_VALIDATION_REPORT` | 500 INTERNAL_SERVER_ERROR | Error saving full json report to disk. |
| 270199 | `ERROR_DELETING_ON_DISK_VALIDATION_REPORT` | 500 INTERNAL_SERVER_ERROR | Error deleting on-disk validation report. You can delete the report manually using the file browser in the project setting tab. Reports are stored by default in the DataValidation directory, under the corresponding feature group name and version subdirectories. |
| 270200 | `INPUT_FIELD_EXCEEDS_MAX_ALLOWED_CHARACTER` | 400 BAD_REQUEST | Input field length exceeds max allowed characters. |
| 270201 | `INPUT_FIELD_IS_NOT_VALID_JSON` | 400 BAD_REQUEST | Input field fail to be parsed to valid Json. |
| 270202 | `INPUT_FIELD_IS_NOT_NULLABLE` | 400 BAD_REQUEST | Input field is not nullable. |
| 270203 | `ERROR_INFERRING_INGESTION_RESULT` | 400 BAD_REQUEST | Could not infer ingestion result from validation ingestion policy and validation success. |
| 270204 | `FAILED_TO_DELETE_TD_DATA` | 400 BAD_REQUEST | Failed to delete training dataset. |
| 270205 | `ERROR_DELETING_FEATURE_VIEW` | 500 INTERNAL_SERVER_ERROR | Error deleting feature view. |
| 270206 | `ILLEGAL_TRAINING_DATASET_TIME_SERIES_SPLIT` | 400 BAD_REQUEST | Illegal training dataset time series split. |
| 270207 | `ILLEGAL_EXPECTATION_UPDATE` | 400 BAD_REQUEST | Illegal Expectation update. To preserve the validation history this update is not allowed. Create a new Expectation by removing expectationId from meta field instead. |
| 270208 | `EXPECTATION_SUITE_ALREADY_EXISTS` | 409 CONFLICT | An expectation suite is already attached to this feature group. Either update the existing suite via the update endpoint or delete it first. |
| 270209 | `FAILURE_HDFS_USER_OPERATION` | 500 INTERNAL_SERVER_ERROR | HDFS user operation failure |
| 270210 | `FEATURE_NAME_NOT_FOUND` | 400 BAD_REQUEST | The Feature Name was not found in this version of the Feature Group. |
| 270211 | `VALIDATION_RESULT_IS_NOT_VALID_JSON` | 400 BAD_REQUEST | The validation result is not a valid json. |
| 270212 | `FEATURE_OFFLINE_TYPE_NOT_PROVIDED` | 400 BAD_REQUEST | Feature offline type cannot be null or empty. |
| 270213 | `AMBIGUOUS_FEATURE_ERROR` | 400 BAD_REQUEST | Feature name is ambiguous. |
| 270214 | `STORAGE_CONNECTOR_TYPE_NOT_ENABLED` | 400 BAD_REQUEST | Storage connector type not enabled |
| 270215 | `COULD_NOT_SHARE_FEATURE_STORE` | 500 INTERNAL_SERVER_ERROR | Could not share feature store |
| 270216 | `FILE_DELETION_ERROR` | 400 BAD_REQUEST | Failed to delete file |
| 270217 | `FILE_READ_ERROR` | 400 BAD_REQUEST | Failed to read file |
| 270218 | `DOCKER_FULLNAME_ERROR` | 400 BAD_REQUEST | Failed to retrieve full docker image name |
| 270219 | `CONNECTION_CHECKER_LAUNCH_ERROR` | 400 BAD_REQUEST | Failed to launch process to start docker container for testing connection |
| 270220 | `CONNECTION_CHECKER_ERROR` | 400 BAD_REQUEST | Failure in testing connection for storage connector |
| 270221 | `ERROR_CREATING_ONLINE_FEATURESTORE_KAFKA_OFFSET_TABLE` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to create the kafka offset table for an online feature store |
| 270222 | `ERROR_CONSTRUCTING_VALIDATION_REPORT_DIRECTORY_PATH` | 500 INTERNAL_SERVER_ERROR | An error occurred while constructing validation report directory path |
| 270223 | `SPINE_GROUP_ON_RIGHT_SIDE_OF_JOIN_NOT_ALLOWED` | 400 BAD_REQUEST | Spine groups cannot be used on the right sideof a feature view join. |
| 270224 | `FEATURE_GROUP_DUPLICATE_FEATURE` | 400 BAD_REQUEST | Feature list contains duplicate |
| 270225 | `HELPER_COL_NOT_FOUND` | 404 NOT_FOUND | Could not find helper column in feature view schema |
| 270226 | `OPENSEARCH_DEFAULT_EMBEDDING_INDEX_SUFFIX_NOT_DEFINED` | 500 INTERNAL_SERVER_ERROR | Opensearch default embedding index not defined |
| 270227 | `FEATURE_GROUP_COMMIT_NOT_FOUND` | 400 BAD_REQUEST | Feature group commit not found |
| 270228 | `STATISTICS_NOT_FOUND` | 404 NOT_FOUND | Statistics wasn't found. |
| 270229 | `INVALID_STATISTICS_WINDOW_TIMES` | 400 BAD_REQUEST | Window times provided are invalid |
| 270230 | `COULD_NOT_DELETE_VECTOR_DB_INDEX` | 500 INTERNAL_SERVER_ERROR | Could not delete index from vector db. |
| 270231 | `COULD_NOT_INITIATE_ARROW_FLIGHT_CONNECTION` | 500 INTERNAL_SERVER_ERROR | Could not initiate connection to Arrow Flight server |
| 270232 | `ARROW_FLIGHT_READ_QUERY_ERROR` | 400 BAD_REQUEST | Arrow Flight server Read Query failed |
| 270233 | `FEATURE_MONITORING_ENTITY_NOT_FOUND` | 404 NOT_FOUND | Feature Monitoring entity not found. |
| 270234 | `FEATURE_MONITORING_NOT_ENABLED` | 400 BAD_REQUEST | Feature monitoring is not enabled. |
| 270235 | `FEATURE_NOT_FOUND_IN_VECTOR_DB` | 500 INTERNAL_SERVER_ERROR | Feature not found in vector db. |
| 270236 | `COULD_NOT_PREVIEW_DATA_IN_VECTOR_DB` | 500 INTERNAL_SERVER_ERROR | Could not preview data in vector database. |
| 270237 | `EMBEDDING_FEATURE_NOT_FOUND` | 400 BAD_REQUEST | Embedding feature cannot be found in feature group. |
| 270238 | `COULD_NOT_GET_VECTOR_DB_INDEX` | 500 INTERNAL_SERVER_ERROR | Could not get index from vector db. |
| 270239 | `EMBEDDING_INDEX_EXISTED` | 400 BAD_REQUEST | Embedding index already exists. |
| 270240 | `INVALID_EMBEDDING_INDEX_NAME` | 400 BAD_REQUEST | Embedding index name is not valid. |
| 270241 | `VECTOR_DATABASE_INDEX_MAPPING_LIMIT_EXCEEDED` | 400 BAD_REQUEST | Index mapping limit exceeded. |
| 270242 | `VECTOR_DATABASE_DATA_TYPE_NOT_SUPPORTED` | 400 BAD_REQUEST | Provided data type is not supported by vector database. |
| 270243 | `PREVIEW_NOT_SUPPORTED` | 400 BAD_REQUEST | Preview is not supported |
| 270244 | `FOREIGN_KEY_NOT_PRIMARY_KEY` | 400 BAD_REQUEST | foreign key from the left feature group is not a primary key in the right feature group |
| 270245 | `NESTED_JOINS_RECURSION_LIMIT_EXCEEDED` | 500 INTERNAL_SERVER_ERROR | Could not construct nested query, recursion limit exceeded |
| 270246 | `ERROR_DELETING_TRANSFORMATION_FUNCTION_ATTACHED` | 500 INTERNAL_SERVER_ERROR | Cannot delete transformation function attached to a feature view |
| 270247 | `HOSWORKS_ACTION_TASK_SERIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Hopsworks action task serialization error. |
| 270248 | `FEATURE_VIEW_LOGGING_DOES_NOT_EXIST` | 400 BAD_REQUEST | Feature view logging does not exist |
| 270249 | `JOIN_ON_PARTIAL_PRIMARY_KEY` | 400 BAD_REQUEST | the join lacks a key which is part of the primary key of the feature group |
| 270250 | `COULD_NOT_INITIATE_S3_CLIENT` | 500 INTERNAL_SERVER_ERROR | Could not initiate connection to s3 |
| 270251 | `CONNECTOR_FIELD_MISSING` | 400 BAD_REQUEST | Field missing in storage connector |
| 270252 | `COULD_NOT_INIT_VECTOR_DB` | 500 INTERNAL_SERVER_ERROR | Could not initiate vector database. |
| 270253 | `TIME_TRAVEL_FORMAT_NOT_SUPPORTED` | 400 BAD_REQUEST | Not supported time travel format |
| 270254 | `ERROR_CREATING_ONLINE_INGESTION_RESULT_TABLE` | 500 INTERNAL_SERVER_ERROR | An error occurred when trying to create the Online Ingestion Result table for an online feature store |
| 270255 | `INVALID_OUTPUT_NAME_TRANSFORMATION_FUNCTION` | 400 BAD_REQUEST | Invalid output feature name specified for transformation function |
| 270256 | `INVALID_ONLINE_DATA_TYPE` | 400 BAD_REQUEST | The provided online type is invalid |
| 270257 | `DATABASE_NOT_SPECIFIED` | 400 BAD_REQUEST | The database was not specified |
| 270258 | `DATABASE_CANNOT_BE_CHANGED` | 400 BAD_REQUEST | The database cannot be specified |
| 270259 | `ARROW_FLIGHT_ERROR` | 500 INTERNAL_SERVER_ERROR | Arrow Flight error |
| 270260 | `COULD_NOT_ENABLE_TTL` | 400 BAD_REQUEST | Could not enable ttl |
| 270261 | `CHART_NOT_FOUND` | 404 NOT_FOUND | Chart wasn't found. |
| 270262 | `DASHBOARD_NOT_FOUND` | 404 NOT_FOUND | Dashboard wasn't found. |
| 270263 | `COULD_NOT_DELETE_FEATURE_GROUP` | 400 BAD_REQUEST | Could not delete feature group |
| 270264 | `FEATURE_STORE_ALREADY_SHARED` | 400 BAD_REQUEST | Feature store already shared with project |
| 270265 | `COULD_NOT_SHARE_FEATURE_GROUP` | 500 INTERNAL_SERVER_ERROR | Could not share feature group |
| 270266 | `FEATURE_GROUP_NOT_SHARED` | 400 BAD_REQUEST | The feature group is not shared |
| 270267 | `FEATURE_GROUP_ALREADY_SHARED` | 400 BAD_REQUEST | The feature group is already shared with the project |
| 270268 | `FEATURE_NOT_SHARED` | 400 BAD_REQUEST | The feature is not shared |
| 270269 | `ERROR_SIGNING_QUERY` | 500 INTERNAL_SERVER_ERROR | Could not sign the query |
| 270270 | `RESTRICTED_ACCESS_ALREADY_GRANTED` | 400 BAD_REQUEST | Restricted access to this feature group is already granted to the user |
| 270271 | `RESTRICTED_ACCESS_NOT_GRANTED` | 404 NOT_FOUND | Restricted access to this feature group is not granted to the user |
| 270272 | `FEATUREGROUP_NO_ACCESSIBLE_FEATURES` | 400 BAD_REQUEST | No accessible features in this feature group for the current user |
| 270273 | `FEATURE_GROUP_DUPLICATE_PATH` | 400 BAD_REQUEST | A feature group with the same path already exists |
| 270274 | `FAILED_TO_DELETE_SINK_JOB_FOR_FEATURE_GROUP` | 500 INTERNAL_SERVER_ERROR | Failed to delete sink job for feature group |
| 270275 | `COULD_NOT_DELETE_FEATURE_VIEW` | 409 CONFLICT | Could not delete feature view |
| 270276 | `INVALID_ONLINE_CONFIG_PRIMARY_KEY_INDEX_TYPE` | 400 BAD_REQUEST | The provided online config primary key index type is invalid. |
| 270277 | `LOOKBACK_WINDOW_MISSING_START` | 400 BAD_REQUEST | Lookback window requires `start` to be set. |
| 270278 | `LOOKBACK_WINDOW_INVERTED_RANGE` | 400 BAD_REQUEST | Lookback window `start` must be strictly earlier than `end`. |
| 270279 | `LOOKBACK_WINDOW_NO_EVENT_TIME` | 400 BAD_REQUEST | Lookback window `key=EVENT_TIME` requires the joined feature group to declare an event_time column. |
| 270280 | `LOOKBACK_WINDOW_NO_PARTITION_KEY` | 400 BAD_REQUEST | Lookback window `key=PARTITION_KEY` requires the joined feature group to have a single DATE partition column. |
| 270281 | `LOOKBACK_WINDOW_INVALID_KEY` | 400 BAD_REQUEST | Lookback window `key` must be `EVENT_TIME` or `PARTITION_KEY`. |
| 270282 | `LOOKBACK_WINDOW_UNKNOWN_JOIN` | 400 BAD_REQUEST | Lookback override does not match any joined feature group. |
| 270283 | `LOOKBACK_WINDOW_DUPLICATE_JOIN` | 400 BAD_REQUEST | Multiple lookback entries for the same joined feature group. |
| 270284 | `DEFAULT_FEATURESTORE_NOT_CONFIGURED` | 404 NOT_FOUND | Default featurestore project is not configured. |
| 270285 | `INVALID_ONLINE_CONFIG_SECONDARY_INDEX` | 400 BAD_REQUEST | The provided online config secondary index is invalid. |
| 270286 | `TRANSFORMATION_FUNCTION_INPUT_TYPE_UNRESOLVABLE` | 400 BAD_REQUEST | Transformation function input feature type could not be resolved. |
| 270287 | `FEATURE_MONITORING_INPUT_VALIDATION` | 400 BAD_REQUEST | Invalid feature monitoring input. |
| 270288 | `PARTITIONED_BY_EMPTY` | 400 BAD_REQUEST | partitioned_by must be a non-empty list when set. |
| 270289 | `PARTITIONED_BY_INVALID_GRAIN` | 400 BAD_REQUEST | partitioned_by contains a grain that is not in the supported set. |
| 270290 | `PARTITIONED_BY_DUPLICATE` | 400 BAD_REQUEST | partitioned_by contains duplicate grains. |
| 270291 | `PARTITIONED_BY_CONFLICTS_WITH_PARTITION_KEY` | 400 BAD_REQUEST | partitioned_by cannot be set together with partition_key. |
| 270292 | `PARTITIONED_BY_REQUIRES_EVENT_TIME` | 400 BAD_REQUEST | partitioned_by requires event_time to be set on the feature group. |
| 270293 | `PARTITIONED_BY_COLLIDES_WITH_EVENT_TIME` | 400 BAD_REQUEST | event_time column name collides with a partitioned_by grain. |
| 270294 | `PARTITIONED_BY_COLLIDES_WITH_FEATURE` | 400 BAD_REQUEST | partitioned_by grain name collides with an existing feature name. |
| 270295 | `PARTITIONED_BY_ONLINE_NOT_SUPPORTED` | 400 BAD_REQUEST | partitioned_by is not supported on online-enabled feature groups yet. |
| 270296 | `PARTITIONED_BY_UNSUPPORTED_FORMAT` | 400 BAD_REQUEST | partitioned_by requires a time_travel_format that materializes partition columns (DELTA, ICEBERG, or HUDI). |
| 270297 | `PARTITIONED_BY_HOUR_REQUIRES_TIMESTAMP` | 400 BAD_REQUEST | the 'hour' grain requires a timestamp event_time; a date event_time has no sub-day resolution. |
| 270298 | `ONLINE_FEATUREGROUP_OFFLINE_ONLY_KEY_COLUMN` | 400 BAD_REQUEST | a primary key, event_time, or secondary-index column cannot be offline_only: the online table excludes offline_only columns, so it would reference a column that is absent from the online schema. |

## AirflowErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 290001 | `JWT_NOT_CREATED` | 500 INTERNAL_SERVER_ERROR | JWT for Airflow service could not be created |
| 290002 | `JWT_NOT_STORED` | 500 INTERNAL_SERVER_ERROR | JWT for Airflow service could not be stored |
| 290003 | `AIRFLOW_DIRS_NOT_CREATED` | 500 INTERNAL_SERVER_ERROR | Airflow internal directories could not be created |
| 290004 | `DAG_NOT_TEMPLATED` | 500 INTERNAL_SERVER_ERROR | Could not template DAG file |
| 290005 | `AIRFLOW_MANAGER_UNINITIALIZED` | 500 INTERNAL_SERVER_ERROR | AirflowManager is not initialized |
| 290006 | `DAG_NAME_INVALID` | 400 BAD_REQUEST | DAG definition failed validation |
| 290007 | `AIRFLOW_GENERIC_ERROR` | 500 INTERNAL_SERVER_ERROR | Airflow internal error |
| 290008 | `AIRFLOW_DISABLED` | 400 BAD_REQUEST | Airflow is disabled |

## PythonErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 300000 | `ANACONDA_ENVIRONMENT_NOT_FOUND` | 404 NOT_FOUND | Could not find the environment. |
| 300001 | `ANACONDA_ENVIRONMENT_ALREADY_INITIALIZED` | 409 CONFLICT | Anaconda environment already created for this project. |
| 300002 | `PYTHON_SEARCH_TYPE_NOT_SUPPORTED` | 400 BAD_REQUEST | The supplied search is not supported, only pip and conda are currently supported. |
| 300003 | `PYTHON_LIBRARY_NOT_FOUND` | 404 NOT_FOUND | Library could not be found. |
| 300004 | `YML_FILE_MISSING_PYTHON_VERSION` | 400 BAD_REQUEST | No python binary version was found in the environment yaml file. |
| 300005 | `NOT_MATCHING_PYTHON_VERSIONS` | 400 BAD_REQUEST | The supplied yaml files have mismatching python versions. |
| 300006 | `CONDA_INSTALL_REQUIRES_CHANNEL` | 400 BAD_REQUEST | Conda package manager requires that a conda channel is selected in which the library is located |
| 300007 | `INSTALL_TYPE_NOT_SUPPORTED` | 400 BAD_REQUEST | The provided install type is not supported |
| 300008 | `CONDA_COMMAND_NOT_FOUND` | 400 BAD_REQUEST | Command not found. |
| 300009 | `MACHINE_TYPE_NOT_SPECIFIED` | 400 BAD_REQUEST | Machine type not specified. |
| 300010 | `VERSION_NOT_SPECIFIED` | 400 BAD_REQUEST | Version not specified. |
| 300011 | `ANACONDA_ENVIRONMENT_INITIALIZING` | 400 BAD_REQUEST | The project's Python environment is currently being initialized. Please try again later. |
| 300012 | `ANACONDA_ENVIRONMENT_FILE_INVALID` | 400 BAD_REQUEST | Path is not a valid environment file, must be Anaconda .yml or requirements.txt |
| 300013 | `ANACONDA_PIP_CHECK_FAILED` | 500 INTERNAL_SERVER_ERROR | pip check command failed |
| 300014 | `ANACONDA_ENVIRONMENT_FAILED_INITIALIZATION` | 500 INTERNAL_SERVER_ERROR | The project's Python environment failed to initialize, please recreate the environment. |
| 300015 | `ANACONDA_ENVIRONMENT_REMOVAL_FAILED` | 500 INTERNAL_SERVER_ERROR | Deletion of the project's Python environment encountered an issue |
| 300016 | `CONDA_COMMAND_DELETE_ERROR` | 400 BAD_REQUEST | Failed to delete a command |
| 300017 | `CONDA_INSTALL_DISABLED` | 403 FORBIDDEN | Conda install option is disabled. Contact Admin user to enable it. |
| 300018 | `INVALID_ENVIRONMENT_NAME` | 400 BAD_REQUEST | The name is not correct and does not match a valid environment |
| 300019 | `PREINSTALLED_ENVIRONMENT_CAN_NOT_BE_DELETED` | 403 FORBIDDEN | It is not possible to delete a preinstalled environment |
| 300020 | `CAN_NOT_MODIFY_BASE_ENVIRONMENT` | 403 FORBIDDEN | It is not possible to modify the base environment, create your own environment instead |
| 300021 | `INCORRECT_ENVIRONMENT` | 400 BAD_REQUEST | The configured environment is not compatible. |
| 300022 | `ENVIRONMENT_IN_USE` | 400 BAD_REQUEST | This environment is currently in use. |
| 300023 | `INVALID_ENVIRONMENT_NAME_INPUT` | 400 BAD_REQUEST | This environment is currently in use. |
| 300024 | `ENVIRONMENT_NOT_FOUND` | 404 NOT_FOUND | The environment was not found. |
| 300025 | `PROJECT_ENVIRONMENT_QUOTA_REACHED` | 403 FORBIDDEN | This project has reached the maximum number of environments that can be cloned |

## ResourceErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 310000 | `INVALID_QUERY_PARAMETER` | 404 NOT_FOUND | Invalid query. |

## ApiKeyErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 320001 | `KEY_NOT_CREATED` | 400 BAD_REQUEST | Api key could not be created |
| 320002 | `KEY_NOT_FOUND` | 401 UNAUTHORIZED | Api key not found |
| 320003 | `KEY_ROLE_CONTROL_EXCEPTION` | 403 FORBIDDEN | No valid role found for this invocation |
| 320004 | `KEY_SCOPE_CONTROL_EXCEPTION` | 403 FORBIDDEN | No valid scope found for this invocation |
| 320005 | `KEY_SCOPE_NOT_SPECIFIED` | 400 BAD_REQUEST | Api key scope can not be empty |
| 320006 | `KEY_SCOPE_EMPTY` | 400 BAD_REQUEST | Api key scope can not be empty |
| 320007 | `KEY_NAME_EXIST` | 400 BAD_REQUEST | Api key name already exists |
| 320008 | `KEY_NAME_NOT_SPECIFIED` | 400 BAD_REQUEST | Api key name not specified |
| 320009 | `KEY_NAME_NOT_VALID` | 400 BAD_REQUEST | Api key name not valid |
| 320010 | `KEY_HANDLER_CREATE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during apikey create handler. |
| 320011 | `KEY_HANDLER_DELETE_ERROR` | 500 INTERNAL_SERVER_ERROR | Error occurred during apikey delete handler. |
| 320012 | `KEY_INVALID` | 401 UNAUTHORIZED | Invalid or incorrect API key. |
| 320013 | `KEY_NOT_FOUND_IN_DATABASE` | 401 UNAUTHORIZED | API key not found in the database |
| 320014 | `KEY_EXPIRED` | 401 UNAUTHORIZED | Api key has expired |
| 320015 | `KEY_EXPIRY_DATE_INVALID` | 400 BAD_REQUEST | Api key expiry date is invalid |

## OpenSearchErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 330000 | `SIGNING_KEY_ERROR` | 500 INTERNAL_SERVER_ERROR | Couldn't get or create the elk signing key |
| 330001 | `JWT_NOT_CREATED` | 500 INTERNAL_SERVER_ERROR | Jwt for elk couldn't be created |
| 330002 | `KIBANA_REQ_ERROR` | 400 BAD_REQUEST | Error while executing Kibana request |
| 330003 | `OPENSEARCH_CONNECTION_ERROR` | 503 SERVICE_UNAVAILABLE | Couldn't connect to OpenSearch |
| 330004 | `OPENSEARCH_INTERNAL_REQ_ERROR` | 500 INTERNAL_SERVER_ERROR | Error while executing OpenSearch request |
| 330005 | `OPENSEARCH_QUERY_ERROR` | 400 BAD_REQUEST | Error while executing a user query on OpenSearch |
| 330006 | `INVALID_OPENSEARCH_ROLE` | 500 INTERNAL_SERVER_ERROR | Invalid OpenSearch security role |
| 330007 | `INVALID_OPENSEARCH_ROLE_USER` | 401 UNAUTHORIZED | Invalid OpenSearch security role for a user |
| 330008 | `OPENSEARCH_QUERY_NO_MAPPING` | 400 BAD_REQUEST | OpenSearch query uses a field that is not in the mapping of the index |
| 330009 | `OPENSEARCH_INDEX_NOT_FOUND` | 404 NOT_FOUND | OpenSearch index not found |

## ProvenanceErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 340001 | `MALFORMED_ENTRY` | 500 INTERNAL_SERVER_ERROR | Provenance entry is malformed |
| 340002 | `BAD_REQUEST` | 500 INTERNAL_SERVER_ERROR | Provenance query request is malformed |
| 340003 | `UNSUPPORTED` | 400 BAD_REQUEST | Provenance query is not supported |
| 340004 | `INTERNAL_ERROR` | 500 INTERNAL_SERVER_ERROR | Provenance logical error |
| 340005 | `ARCHIVAL_STORE` | 500 INTERNAL_SERVER_ERROR | Provenance archival store error |
| 340006 | `FS_ERROR` | 500 INTERNAL_SERVER_ERROR | Provenance xattr - file system error |

## ModelRegistryErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 360000 | `MODEL_NOT_FOUND` | 404 NOT_FOUND | No model found for provided name and version. |
| 360001 | `KEY_NOT_STRING` | 404 NOT_FOUND | metrics key is not a string. |
| 360002 | `METRIC_NOT_NUMBER` | 400 BAD_REQUEST | Could not cast provided metric to double. |
| 360003 | `MODEL_LIST_FAILED` | 500 INTERNAL_SERVER_ERROR | Error occurred when fetching models. |
| 360004 | `MODEL_MARSHALLING_FAILED` | 500 INTERNAL_SERVER_ERROR | Error occurred during marshalling/unmarshalling of model json. |
| 360005 | `MODEL_REGISTRY_ID_NOT_PROVIDED` | 400 BAD_REQUEST | Model Registry Id was not provided. |
| 360006 | `MODEL_REGISTRY_ID_NOT_FOUND` | 400 BAD_REQUEST | Model Registry Id was not found. |
| 360007 | `MODEL_REGISTRY_ACCESS_DENIED` | 403 FORBIDDEN | Model Registry not accessible. |
| 360008 | `MODEL_REGISTRY_MODELS_DATASET_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Models dataset does not exist in project. |
| 360009 | `MODEL_CANNOT_BE_DELETED` | 400 BAD_REQUEST | Could not delete the model |
| 360010 | `HUGGINGFACE_AUTH_REQUIRED` | 401 UNAUTHORIZED | HuggingFace access token is required for this model. Please provide a valid token. |
| 360011 | `HUGGINGFACE_MODEL_NOT_FOUND` | 404 NOT_FOUND | HuggingFace model not found. Please verify the model ID. |
| 360012 | `HUGGINGFACE_DOWNLOAD_FAILED` | 500 INTERNAL_SERVER_ERROR | Failed to download model from HuggingFace. |
| 360013 | `HUGGINGFACE_INVALID_REQUEST` | 400 BAD_REQUEST | Invalid HuggingFace import request. |

## SchematizedTagErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 370000 | `TAG_SCHEMA_NOT_FOUND` | 404 NOT_FOUND | No schema found for provided name |
| 370001 | `INVALID_TAG_SCHEMA` | 400 BAD_REQUEST | Invalid tag schema. |
| 370002 | `TAG_NOT_FOUND` | 404 NOT_FOUND | No tag found for provided name. |
| 370003 | `TAG_ALREADY_EXISTS` | 409 CONFLICT | Tag with the same name already exists. |
| 370004 | `INVALID_TAG_NAME` | 400 BAD_REQUEST | Invalid tag name. |
| 370005 | `INVALID_TAG_VALUE` | 400 BAD_REQUEST | Invalid tag value. |
| 370006 | `TAG_NOT_ALLOWED` | 400 BAD_REQUEST | The provided tag is not allowed |
| 370007 | `INTERNAL_PROCESSING_ERROR` | 500 INTERNAL_SERVER_ERROR | Internal error while processing tag |
| 370008 | `INVALID_MANDATORY_TAG` | 400 BAD_REQUEST | Invalid mandatory tag |

## CloudErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 380000 | `CLOUD_FEATURE` | 405 METHOD_NOT_ALLOWED | This method is only available in cloud deployments. |
| 380001 | `FAILED_TO_ASSUME_ROLE` | 400 BAD_REQUEST | Failed to assume role. |
| 380002 | `ACCESS_CONTROL_EXCEPTION` | 403 FORBIDDEN | You are not allowed to assume this role. |
| 380003 | `MAPPING_NOT_FOUND` | 400 BAD_REQUEST | Mapping not found. |
| 380004 | `MAPPING_ALREADY_EXISTS` | 400 BAD_REQUEST | Mapping for the given project and role already exists. |
| 380005 | `FAILED_TO_GET_CLUSTER_CRED` | 400 BAD_REQUEST | Failed to get cluster credential. |

## AlertErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 390000 | `ALERT_CREATION_FAILED` | 400 BAD_REQUEST | Failed to create alert |
| 390001 | `RECEIVER_EXIST` | 400 BAD_REQUEST | A receiver already exists. |
| 390002 | `ROUTE_EXIST` | 400 BAD_REQUEST | A route already exists. |
| 390003 | `RECEIVER_NOT_FOUND` | 400 BAD_REQUEST | Receiver not found. |
| 390004 | `ROUTE_NOT_FOUND` | 400 BAD_REQUEST | Route not found. |
| 390005 | `SILENCE_NOT_FOUND` | 400 BAD_REQUEST | Silence not found. |
| 390006 | `ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Illegal argument. |
| 390007 | `FAILED_TO_CONNECT` | 412 PRECONDITION_FAILED | Failed to connect to alert manager. |
| 390008 | `FAILED_TO_UPDATE_AM_CONFIG` | 412 PRECONDITION_FAILED | Failed to update alert manager configuration. |
| 390009 | `RESPONSE_ERROR` | 400 BAD_REQUEST | Alert manager response error. |
| 390010 | `ACCESS_CONTROL_EXCEPTION` | 403 FORBIDDEN | You are not allowed to access this resource. |
| 390011 | `FAILED_TO_READ_CONFIGURATION` | 412 PRECONDITION_FAILED | Failed to read alert manager configuration. |
| 390012 | `FAILED_TO_CLEAN` | 412 PRECONDITION_FAILED | Failed to clean project from alert manager config. |
| 390013 | `AM_CONFIG_NOT_UPDATED` | 409 CONFLICT | Alert manager config not updated. |

## RemoteAuthErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 400000 | `NOT_FOUND` | 404 NOT_FOUND | Not found. |
| 400001 | `DUPLICATE_ENTRY` | 400 BAD_REQUEST | Duplicate entry. |
| 400002 | `ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Illegal argument. |
| 400003 | `WRONG_CONFIG` | 412 PRECONDITION_FAILED | Wrong configuration. |
| 400004 | `TOKEN_PARSE_EXCEPTION` | 417 EXPECTATION_FAILED | Token ParseException. |
| 400005 | `NOT_ALLOWED` | 400 BAD_REQUEST | Operation not allowed. |

## CommandErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 410000 | `INTERNAL_SERVER_ERROR` | 500 INTERNAL_SERVER_ERROR | Something went wrong executing command |
| 410001 | `INVALID_SQL_QUERY` | 400 BAD_REQUEST | Invalid sql query for command |
| 410002 | `ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Illegal argument in command |
| 410003 | `FILESYSTEM_ACCESS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error accessing files system for components |
| 410004 | `FEATURESTORE_ACCESS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error accessing the featurestore |
| 410005 | `OPENSEARCH_ACCESS_ERROR` | 500 INTERNAL_SERVER_ERROR | Error acccessing OpenSearch |
| 410006 | `SERIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Error serializing content |
| 410007 | `NOT_IMPLEMENTED` | 501 NOT_IMPLEMENTED | Internal error dealing with new artifact type |
| 410008 | `DB_QUERY_ERROR` | 500 INTERNAL_SERVER_ERROR | DB error on query |
| 410009 | `ARTIFACT_DELETED` | 500 INTERNAL_SERVER_ERROR | Artifact was deleted before command could be executed |

## GitOpErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 500000 | `SIGNING_KEY_ERROR` | 500 INTERNAL_SERVER_ERROR | Couldn't get or create the GIT signing key. |
| 500001 | `JWT_NOT_CREATED` | 500 INTERNAL_SERVER_ERROR | Jwt for GIT could not be created. |
| 500003 | `INVALID_GIT_ROLE_USER` | 401 UNAUTHORIZED | Invalid git security role for a user. |
| 500004 | `JWT_MATERIALIZATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not materialize jwt. |
| 500005 | `GIT_PATHS_CREATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not create git paths. |
| 500006 | `REPOSITORY_URL_NOT_PROVIDED` | 400 BAD_REQUEST | Repository url not provided. |
| 500007 | `DIRECTORY_PATH_NOT_PROVIDED` | 400 BAD_REQUEST | Path to directory not provided. |
| 500008 | `DIRECTORY_PATH_DOES_NOT_EXIST` | 400 BAD_REQUEST | The directory does not exist. |
| 500009 | `PATH_IS_NOT_DIRECTORY` | 400 BAD_REQUEST | Path is not a directory. |
| 500010 | `GIT_HOME_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not resolve GIT_HOME using DB. |
| 500012 | `GIT_CONTAINER_LAUNCH_ERROR` | 500 INTERNAL_SERVER_ERROR | Could not launch the git container. |
| 500013 | `EXECUTION_OBJECT_NOT_FOUND` | 404 NOT_FOUND | Execution object with the id not found. |
| 500014 | `INVALID_AUTHENTICATION_METHOD` | 400 BAD_REQUEST | Unknown authentication method. |
| 500015 | `INVALID_GITHUB_USERNAME` | 400 BAD_REQUEST | Invalid git username. |
| 500016 | `USER_DOES_NOT_HAVE_PERMISSIONS_TO_GIT_DIR` | 400 BAD_REQUEST | Git directory security error. |
| 500017 | `COMMIT_MESSAGE_IS_EMPTY` | 400 BAD_REQUEST | Commit command message should not be empty. |
| 500018 | `INVALID_BRANCH_NAME` | 400 BAD_REQUEST | Branch name should not be empty. |
| 500019 | `REPOSITORY_NOT_FOUND` | 404 NOT_FOUND | Repository not found. |
| 500020 | `GIT_PROVIDER_NOT_PROVIDED` | 400 BAD_REQUEST | Git provider not provided. |
| 500021 | `INVALID_REPOSITORY_URL` | 400 BAD_REQUEST | Invalid repository url provided |
| 500022 | `DIRECTORY_IS_ALREADY_GIT_REPO` | 400 BAD_REQUEST | Directory is already a git repository |
| 500023 | `INVALID_BRANCH_ACTION` | 400 BAD_REQUEST | Invalid branch action provided. |
| 500024 | `INVALID_REMOTES_ACTION` | 400 BAD_REQUEST | Invalid remotes action provided |
| 500025 | `INVALID_REMOTE_NAME` | 400 BAD_REQUEST | Invalid remote name provided. Remote name should not be empty. |
| 500026 | `INVALID_REMOTE_URL_PROVIDED` | 400 BAD_REQUEST | Invalid remote url provided. Remote url should not be empty. |
| 500027 | `GIT_OPERATION_ERROR` | 500 INTERNAL_SERVER_ERROR | Git operation error. |
| 500028 | `GIT_REPOSITORIES_NOT_FOUND` | 404 NOT_FOUND | No git repository found in project |
| 500029 | `GIT_USERNAME_AND_PASSWORD_NOT_SET` | 400 BAD_REQUEST | Git username and password not set |
| 500030 | `COMMIT_FILES_EMPTY` | 400 BAD_REQUEST | Files to add and commit is empty. |
| 500031 | `INVALID_REPOSITORY_ACTION` | 400 BAD_REQUEST | Invalid repository action. |
| 500032 | `REMOTE_NOT_FOUND` | 404 NOT_FOUND | Git remote not found. |
| 500033 | `INVALID_BRANCH_AND_COMMIT_CHECKOUT_COMBINATION` | 400 BAD_REQUEST | Branch and Hash are mutually exclusive. |
| 500034 | `INVALID_GIT_COMMAND_CONFIGURATION` | 500 INTERNAL_SERVER_ERROR | Invalid git command operation |
| 500035 | `USER_IS_NOT_REPOSITORY_OWNER` | 403 FORBIDDEN | User not allowed to perform operation in repository |
| 500036 | `READ_ONLY_REPOSITORY` | 400 BAD_REQUEST | Repository is read only |
| 500037 | `ERROR_VALIDATING_REPOSITORY_PATH` | 500 INTERNAL_SERVER_ERROR | Error validating git repository path |
| 500038 | `ERROR_CANCELLING_GIT_EXECUTION` | 400 BAD_REQUEST | Failed to cancel git execution |
| 500039 | `INVALID_HOSTNAME` | 400 BAD_REQUEST | Hostname provided is not valid |
| 500040 | `TOKEN_NOT_PROVIDED` | 400 BAD_REQUEST | Token not provided |
| 500041 | `DUPLICATE_HOSTS` | 400 BAD_REQUEST | Duplicate hosts provided |

## KubeErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 510000 | `INVALID_INPUT` | 400 BAD_REQUEST | The request contains parameters not valid |
| 510001 | `INTERNAL_ERROR_MISSING` | 500 INTERNAL_SERVER_ERROR | Internal error - missing |
| 510002 | `LOCAL_QUEUE_ALREADY_EXISTS` | 400 BAD_REQUEST | Local queue already exists |
| 510003 | `LOCAL_QUEUE_CREATION_FAILED` | 500 INTERNAL_SERVER_ERROR | Local queue creation failed |
| 510004 | `ERROR_FETCHING_QUEUE` | 500 INTERNAL_SERVER_ERROR | Error fetching configured queue |

## BrewerErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 520000 | `CHAT_NOT_FOUND` | 404 NOT_FOUND | Chat not found. |
| 520001 | `WORKING_DIRECTORY_NOT_FOUND` | 400 BAD_REQUEST | Working directory not found. |
| 520002 | `FAILED_TO_PROCESS_CHAT_MESSAGE` | 500 INTERNAL_SERVER_ERROR | Failed to process chat message. |
| 520003 | `INVALID_CHAT_MESSAGE` | 400 BAD_REQUEST | Invalid chat message. |
| 520004 | `BREWER_WORKER_NOT_FOUND` | 500 INTERNAL_SERVER_ERROR | Brewer worker not found. |
| 520005 | `BREWER_NOT_ENABLED` | 400 BAD_REQUEST | Brewer is not enabled. |
| 520006 | `SELECTED_AGENT_NOT_FOUND` | 404 NOT_FOUND | Selected agent wasn't found. |
| 520007 | `INVALID_SELECTED_AGENT` | 400 BAD_REQUEST | Invalid selected agent. |
| 520008 | `FAILED_TO_SAVE_SELECTED_AGENT` | 500 INTERNAL_SERVER_ERROR | Could not save the selected agent. |
| 520009 | `AGENT_NOT_FOUND` | 404 NOT_FOUND | Agent not found. |
| 520010 | `FAILED_TO_SAVE_AGENT` | 500 INTERNAL_SERVER_ERROR | Could not save the agent. |
| 520011 | `INVALID_AGENT` | 400 BAD_REQUEST | Invalid agent. |
| 520012 | `LLM_NOT_CONFIGURED` | 400 BAD_REQUEST | LLM is not configured. |
| 520013 | `METADATA_INFERENCE_FAILED` | 500 INTERNAL_SERVER_ERROR | Metadata inference failed. |
| 520014 | `VLLM_CONFIG_GENERATION_FAILED` | 500 INTERNAL_SERVER_ERROR | vLLM config generation failed. |
| 520015 | `DEPLOYMENT_GENERATION_FAILED` | 500 INTERNAL_SERVER_ERROR | Deployment generation failed. |

## FeatureStoreMetricsErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 530000 | `METRIC_DOES_NOT_EXIST` | 404 NOT_FOUND | Metric does not exist. |
| 530001 | `FEATURE_STORE_REQUIRED_FOR_METRIC` | 400 BAD_REQUEST | Feature store is required for metric. |
| 530002 | `EVENT_NOT_FOUND` | 404 NOT_FOUND | Event not found. |

## TrinoErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 540000 | `AUTHENTICATION_ERROR` | 417 EXPECTATION_FAILED | Trino authentication error |
| 540001 | `CONNECTION_ERROR` | 503 SERVICE_UNAVAILABLE | Could not connect to Trino server |
| 540002 | `QUERY_EXECUTION_ERROR` | 400 BAD_REQUEST | Error executing Trino query |
| 540003 | `TRINO_NOT_ENABLED` | 400 BAD_REQUEST | Trino is disabled |
| 540004 | `ILLEGAL_ARGUMENT` | 400 BAD_REQUEST | Illegal argument provided |

## AiProviderErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 550000 | `NOT_FOUND` | 404 NOT_FOUND | AI provider not found |
| 550001 | `VALIDATION` | 400 BAD_REQUEST | AI provider validation error |
| 550002 | `SECRET_ERROR` | 500 INTERNAL_SERVER_ERROR | AI provider secret operation failed |

## SupersetErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 560000 | `AUTHENTICATION_ERROR` | 417 EXPECTATION_FAILED | Superset authentication error |
| 560001 | `CONNECTION_ERROR` | 503 SERVICE_UNAVAILABLE | Could not connect to Superset server |
| 560002 | `API_REQUEST_ERROR` | 400 BAD_REQUEST | Error executing Superset API request |
| 560003 | `SUPERSET_DISABLED` | 400 BAD_REQUEST | Superset is disabled |
| 560004 | `FORBIDDEN` | 403 FORBIDDEN | Forbidden from accessing Superset resource |
| 560005 | `INVALID_PARAMETER` | 400 BAD_REQUEST | Invalid parameter provided for Superset API request |

## ProxyErrorCode

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 570000 | `PROXY_UNAUTHORIZED` | 401 UNAUTHORIZED | Proxy authentication failed |
| 570001 | `PROXY_FORBIDDEN` | 403 FORBIDDEN | Not authorized to access this proxied resource |
| 570002 | `PROXY_UPSTREAM_NOT_FOUND` | 404 NOT_FOUND | Upstream proxied service not found |
| 570003 | `PROXY_UPSTREAM_ERROR` | 502 BAD_GATEWAY | Error forwarding request to upstream proxied service |

## SchemaRegistryErrorCode

This category does not follow the 6-digit convention described at the top of this page; it mirrors the Confluent Schema Registry's own error codes instead.

| Code | Name | HTTP status | Message |
| --- | --- | --- | --- |
| 40401 | `SUBJECT_NOT_FOUND` | 404 NOT_FOUND | Subject not found |
| 40402 | `VERSION_NOT_FOUND` | 404 NOT_FOUND | Version not found |
| 40403 | `SCHEMA_NOT_FOUND` | 404 NOT_FOUND | Schema not found |
| 40901 | `INCOMPATIBLE_AVRO_SCHEMA` | 409 CONFLICT | Incompatible Avro schema |
| 42201 | `INVALID_AVRO_SCHEMA` | 422 UNPROCESSABLE_ENTITY | Invalid Avro schema |
| 42202 | `INVALID_VERSION` | 422 UNPROCESSABLE_ENTITY | Invalid version |
| 42203 | `INVALID_COMPATIBILITY` | 422 UNPROCESSABLE_ENTITY | Invalid compatibility level |
| 50001 | `INTERNAL_SERVER_ERROR` | 500 INTERNAL_SERVER_ERROR | Error in the backend datastore |
| 50002 | `OPERATION_TIMED_OUT` | 500 INTERNAL_SERVER_ERROR | Operation timed out |
| 50003 | `ERROR_FORWARDING_REQUEST` | 500 INTERNAL_SERVER_ERROR | Error while forwarding the request to the primary |

<!-- END GENERATED -->
