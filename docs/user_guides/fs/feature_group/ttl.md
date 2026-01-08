## Feature Group TTL Usage Guide

Time To Live (TTL) is a feature that automatically expires data in feature groups after a specified time period. This guide explains when and how to use TTL in your feature groups.

### Use Case: When to Use TTL

TTL is particularly useful for feature groups that contain time-sensitive data that becomes stale or irrelevant after a certain period. Common use cases include:

- **Regulatory compliance**: Data that must be automatically purged after a retention period for privacy or compliance reasons (e.g., GDPR, HIPAA)
- **Cost optimization**: Reducing storage costs by automatically removing outdated data that is no longer needed for model inference
- **Data freshness**: Ensuring that only recent, relevant data is available for online serving, preventing models from using stale features

For example, if you're building a recommendation system, you might want user interaction features (like "items viewed in the last hour") to automatically expire after 1 hour, ensuring your model only uses current, relevant data.

---

## Getting Started

### Creating a Feature Group with TTL

When creating a new feature group, you can enable TTL by specifying the `ttl` parameter. The TTL value determines how long data will remain in the feature group before being automatically expired.
The TTL is calculated based on the `event_time` column. Data rows where `event_time` is older than the TTL period will be automatically removed.

```python
from datetime import datetime, timezone
import pandas as pd

# Assume you already have a feature store handle
# fs = ...

now = datetime.now(timezone.utc)
df = pd.DataFrame(
    {
        "id": [0, 1, 2],
        "timestamp": [now, now, now],
        "feature1": [10, 20, 30],
        "feature2": ["a", "b", "c"],
    }
)

# Create a feature group with TTL enabled (60 seconds)
fg = fs.create_feature_group(
    name="fg_ttl_example",
    version=1,
    primary_key=["id"],
    event_time="timestamp",
    online_enabled=True,
    ttl=60,  # TTL in seconds - data will expire after 60 seconds
)

fg.insert(
    df,
    write_options={
        "start_offline_materialization": False,
        "wait_for_online_ingestion": True,
    },
)

# After 60 seconds, reading online will return empty data
fg.read(online=True)  # Returns empty DataFrame after TTL expires
```

For detailed API reference on all possible types of TTL values, see the [FeatureStore.create_feature_group API documentation][hsfs.feature_store.FeatureStore.create_feature_group].

---

## Managing TTL on Existing Feature Groups

### Updating the TTL Value

You can change the TTL value for an existing feature group at any time. This is useful when you need to adjust the retention period based on changing requirements.

```python
# Get your existing feature group
fg = fs.get_feature_group(
    name="fg_ttl_example",
    version=1,
)

# Update TTL to a new value (120 seconds = 2 minutes)
fg.enable_ttl(ttl=120)
```

After updating the TTL, the new retention period will apply to all future data insertions and will affect when existing data expires.

---

### Disabling and Re-enabling TTL

You can temporarily disable TTL on a feature group if you need to retain data indefinitely, and then re-enable it later.

#### Disabling TTL

```python
# Disable TTL - data will no longer expire automatically
fg.disable_ttl()
```

#### Re-enabling TTL

When re-enabling TTL, you have two options:

1. **Re-enable with the previous TTL value**: If you don't specify a TTL value, the feature group will use the last TTL value that was set.

```python
# Re-enable TTL using the previous TTL value
fg.enable_ttl()
```

**Important**: If TTL was never set on the feature group before, you must provide a TTL value when enabling it. Otherwise, TTL cannot be enabled.

2. **Re-enable with a new TTL value**: Specify a new TTL value when re-enabling.

```python
# Re-enable TTL with a new value (90 seconds)
fg.enable_ttl(ttl=90)
```

---

### Enabling TTL on an Existing Feature Group

If you created a feature group without TTL initially, you can enable it later:

```python
# Get an existing feature group that was created without TTL
fg = fs.get_feature_group(
    name="fg_existing_no_ttl",
    version=1,
)

# Enable TTL for the first time (60 seconds)
fg.enable_ttl(ttl=60)
```

Once enabled, TTL will apply to all data in the feature group based on the `event_time` column.
For detailed API reference on all possible types of TTL values and additional options, see the [FeatureGroup.enable_ttl API documentation][hsfs.feature_group.FeatureGroup.enable_ttl].
