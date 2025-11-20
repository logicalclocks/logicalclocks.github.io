---
description: Using Feature Store REST API Server for retrieving feature vectors
---

# Feature Store REST API Server

This API server allows users to retrieve single/batch feature vectors from a feature view.

## How to use

From Hopsworks 3.3, you can connect to the Feature Vector Server via any REST client which supports POST requests.
Set the X-API-HEADER to your Hopsworks API Key and send the request with a JSON body, [single](#single-feature-vector-request) or [batch](#batch-feature-vectors-request).
By default, the server listens on the `0.0.0.0:4406` and the api version is set to `0.1.0`.
Please refer to `/srv/hops/mysql-cluster/rdrs_config.json` config file located on machines running the REST Server for additional configuration parameters.

In Hopsworks 3.7, we introduced a python client for the Online Store REST API Server.
The python client is available in the `hsfs` module and can be installed using `pip install hsfs`.
This client can be used instead of the Online Store SQL client in the `FeatureView.get_feature_vector(s)` methods.
Check the corresponding [documentation](./feature-vectors.md) for these methods.

## Single Feature Vector

### Single Feature Vector Request

`POST /{api-version}/feature_store`

#### Single Feature Vector Request Body

```json
{
        "featureStoreName": "fsdb002",
        "featureViewName": "sample_2",
        "featureViewVersion": 1,
        "passedFeatures": {},
        "entries": {
                "id1": 36
        },
        "metadataOptions": {
                "featureName": true,
                "featureType": true
        },
        "options": {
                "validatePassedFeatures": true,
                "includeDetailedStatus": true
        }
}
```

#### Single Feature Vector Request Parameters

| **parameter** | **type** | **note** |
| --- | --- | --- |
| featureStoreName | string | |
| featureViewName | string | |
| featureViewVersion | number(int) | |
| entries | objects | Map of serving key of feature view as key and value of serving key as value. Serving key are a set of the primary key of feature groups which are included in the feature view query. If feature groups are joint with prefix, the primary key needs to be attached with prefix. |
| passedFeatures | objects | Optional. Map of feature name as key and feature value as value. This overwrites feature values in the response. |
| metadataOptions | objects | Optional. Map of metadataoption as key and boolean as value. Default metadata option is false. Metadata is returned on request. Metadata options available: 1\. featureName 2\. featureType |
| options | objects | Optional. Map of option as key and boolean as value. Default option is false. Options available: 1\. validatePassedFeatures 2\. includeDetailedStatus |

### Single Feature Vector Response

```json
{
        "features": [
                36,
                "2022-01-24",
                "int24",
                "str14"
        ],
        "metadata": [
                {
                        "featureName": "id1",
                        "featureType": "bigint"
                },
                {
                        "featureName": "ts",
                        "featureType": "date"
                },
                {
                        "featureName": "data1",
                        "featureType": "string"
                },
                {
                        "featureName": "data2",
                        "featureType": "string"
                }
        ],
        "status": "COMPLETE",
        "detailedStatus": [
                {
                        "featureGroupId": 1,
                        "httpStatus": 200,
                },
                {
                        "featureGroupId": 2,
                        "httpStatus": 200,
                },
        ]
}
```

### Single Feature Vector Errors

| **Code** | **reason**                            | **response**                         |
| -------- | ------------------------------------- | ------------------------------------ |
| 200      |                                       |                                      |
| 400      | Requested metadata does not exist     |                                      |
| 400      | Error in pk or passed feature value   |                                      |
| 401      | Access denied                         | Access unshared feature store failed |
| 500      | Failed to read feature store metadata |                                      |

#### Response with PK/pass feature error

```json
{
        "code": 12,
        "message": "Wrong primay-key column. Column: ts",
        "reason": "Incorrect primary key."
}
```

#### Response with metadata error

```json
{
        "code": 2,
        "message": "",
        "reason": "Feature store does not exist."
}
```

#### PK value no match

```json
{
        "features": [
                9876543,
                null,
                null,
                null
        ],
        "metadata": null,
        "status": "MISSING"
}
```

#### Detailed Status

If `includeDetailedStatus` option is set to true, detailed status is returned in the response.
Detailed status is a list of feature group id and http status code, corresponding to each read operations perform internally by RonDB.
Meaning is as follows:

- `featureGroupId`: Id of the feature group, used to identify which table the operation correspond from.
- `httpStatus`: Http status code of the operation.
  - 200 means success
  - 400 means bad request, likely pk name is wrong or pk is incomplete.
    In particular, if pk for this table/feature group is not provided in the request, this http status is returned.
  - 404 means no row corresponding to PK
  - 500 means internal error.

Both `404` and `400` set the status to `MISSING` in the response.
Examples below corresponds respectively to missing row and bad request.

Missing Row: The PK name-value pair was correctly passed, but the corresponding row was not found in the feature group.

```json
{
        "features": [
                36,
                "2022-01-24",
                null,
                null
        ],
        "status": "MISSING",
        "detailedStatus": [
                {
                        "featureGroupId": 1,
                        "httpStatus": 200,
                },
                {
                        "featureGroupId": 2,
                        "httpStatus": 404,
                },
        ]
}
```

Bad Request, e.g., when PK name-value pair for FG2 not provided or the corresponding column names was incorrect:

```json
{
        "features": [
                36,
                "2022-01-24",
                null,
                null
        ],
        "status": "MISSING",
        "detailedStatus": [
                {
                        "featureGroupId": 1,
                        "httpStatus": 200,
                },
                {
                        "featureGroupId": 2,
                        "httpStatus": 400,
                },
        ]
}
```

## Batch Feature Vectors

### Batch Feature Vectors Request

`POST /{api-version}/batch_feature_store`

#### Batch Feature Vectors Request Body

```json
{
        "featureStoreName": "fsdb002",
        "featureViewName": "sample_2",
        "featureViewVersion": 1,
        "passedFeatures": [],
        "entries": [
                {
                        "id1": 16
                },
                {
                        "id1": 36
                },
                {
                        "id1": 71
                },
                {
                        "id1": 48
                },
                {
                        "id1": 29
                }
        ],
        "requestId": null,
        "metadataOptions": {
                "featureName": true,
                "featureType": true
        },
        "options": {
                "validatePassedFeatures": true,
                "includeDetailedStatus": true
        }
}
```

#### Batch Feature Vectors Request Parameters

| **parameter** | **type** | **note** |
| --- | --- | --- |
| featureStoreName | string | |
| featureViewName | string | |
| featureViewVersion | number(int) | |
| entries | `array<objects>` | Each items is a map of serving key as key and value of serving key as value. Serving key of feature view. |
| passedFeatures | `array<objects>` | Optional. Each items is a map of feature name as key and feature value as value. This overwrites feature values in the response. If provided, its size and order has to be equal to the size of entries. Item can be null. |
| metadataOptions | objects | Optional. Map of metadataoption as key and boolean as value. Default metadata option is false. Metadata is returned on request. Metadata options available: 1\. featureName 2\. featureType |
| options | objects | Optional. Map of option as key and boolean as value. Default option is false. Options available: 1\. validatePassedFeatures 2\. includeDetailedStatus |

### Batch Feature Vectors Response

```json
{
        "features": [
                [
                        16,
                        "2022-01-27",
                        "int31",
                        "str24"
                ],
                [
                        36,
                        "2022-01-24",
                        "int24",
                        "str14"
                ],
                [
                        71,
                        null,
                        null,
                        null
                ],
                [
                        48,
                        "2022-01-26",
                        "int92",
                        "str31"
                ],
                [
                        29,
                        "2022-01-03",
                        "int53",
                        "str91"
                ]
        ],
        "metadata": [
                {
                        "featureName": "id1",
                        "featureType": "bigint"
                },
                {
                        "featureName": "ts",
                        "featureType": "date"
                },
                {
                        "featureName": "data1",
                        "featureType": "string"
                },
                {
                        "featureName": "data2",
                        "featureType": "string"
                }
        ],
        "status": [
                "COMPLETE",
                "COMPLETE",
                "MISSING",
                "COMPLETE",
                "COMPLETE"
        ],
        "detailedStatus": [
                [{
                        "featureGroupId": 1,
                        "httpStatus": 200,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 200,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 404,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 200,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 200,
                }]
        ]
}
```

note: Order of the returned features are the same as the order of entries in the request.

### Batch Feature Vectors Errors

| **Code** | **reason**                            | **response**                         |
| -------- | ------------------------------------- | ------------------------------------ |
| 200      |                                       |                                      |
| 400      | Requested metadata does not exist     |                                      |
| 404      | Missing row corresponding to pk value |                                      |
| 401      | Access denied                         | Access unshared feature store failed |
| 500      | Failed to read feature store metadata |                                      |

#### Response with partial failure

```json
{
        "features": [
                [
                        81,
                        "id81",
                        "2022-01-29 00:00:00",
                        6
                ],
                null,
                [
                        51,
                        null,
                        null,
                        null,
                ]
        ],
        "metadata": null,
        "status": [
                "COMPLETE",
                "ERROR",
                "MISSING"
        ],
        "detailedStatus": [
                [{
                        "featureGroupId": 1,
                        "httpStatus": 200,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 400,
                }],
                [{
                        "featureGroupId": 1,
                        "httpStatus": 404,
                }]
        ]
}
```

## Access control to feature store

Currently, the REST API server only supports Hopsworks API Keys for authentication and authorization.
Add the API key to the HTTP requests using the `X-API-KEY` header.
