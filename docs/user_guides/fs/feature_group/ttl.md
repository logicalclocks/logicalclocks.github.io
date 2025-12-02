## Feature Group TTL Usage Guide

Below are examples showing how to work with TTL (Time To Live) on feature groups.

---

### 1. Create a Feature Group with TTL Enabled

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

fg = fs.create_feature_group(
    name="fg_ttl_example",
    version=1,
    primary_key=["id"],
    event_time="timestamp",
    online_enabled=True,
    ttl=60,  # TTL in seconds
)

fg.insert(
    df,
    write_options={
        "start_offline_materialization": False,
        "wait_for_online_ingestion": True,
    },
)

fg.read(online=True)  # return empty df after ttl 
```

---

### 2. Update the TTL Value

```python
# Example: change TTL to a new value (in seconds)
new_ttl_seconds = 120
# Later, update TTL
fg.enable_ttl(new_ttl_seconds)

---

### 3. Disable TTL and Enable It Again

```python
# Disable TTL
fg.disable_ttl()

# ... time passes, you decide to enforce TTL again ...

# Re‑enable TTL with a new value (in seconds)
fg.enable_ttl()  # If ttl is not set, the feature group will be enabled with the last TTL value being set.

# Or Re‑enable TTL with a new value (in seconds)
fg.enable_ttl(ttl=90)
```

---

### 4. Enable TTL on an Existing Feature Group (Created Without TTL)

```python
# Assume this FG was created earlier without TTL
fg = fs.get_feature_group(
    name="fg_existing_no_ttl",
    version=1,
)

# Enable TTL for the first time
fg.enable_ttl(ttl=60)  # seconds

```


### Reference

API reference on all possible types of ttl value can be found [here.](https://docs.hopsworks.ai/hopsworks-api/latest/generated/api/feature_group_api/#enable_ttl)