# Python Integration Guide

## Install

No package needed. Just use `requests`:

```bash
pip install requests
```

## Quick Start

```python
import requests

API = "https://boogeyman-unknowing-amenity.ngrok-free.dev"

def json_to_csv(data):
    r = requests.post(f"{API}/convert", json={"data": data})
    r.raise_for_status()
    return r.text

# Example
rows = [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]
csv_output = json_to_csv(rows)
print(csv_output)
# name,score
# Alice,95
# Bob,87
```

## Pricing

$0.01 per request. No auth required.

## Save to File

```python
with open("output.csv", "w") as f:
    f.write(json_to_csv(rows))
```

## API URL

https://boogeyman-unknowing-amenity.ngrok-free.dev
