---
title: Convert JSON to CSV with a Single API Call
published: true
tags: api, json, csv, python
---

## The Problem

Every data pipeline eventually needs to export JSON as CSV. Writing the same flattening logic over and over wastes time.

## The Solution

A hosted JSON-to-CSV API at:
**https://boogeyman-unknowing-amenity.ngrok-free.dev**

## Quick Start

```bash
curl -X POST https://boogeyman-unknowing-amenity.ngrok-free.dev/convert \
  -H 'Content-Type: application/json' \
  -d '{"data": [{"name":"Alice","age":30},{"name":"Bob","age":25}]}'
```

Response:
```
name,age
Alice,30
Bob,25
```

## Python Example

```python
import requests

data = [{"product": "Widget", "price": 9.99, "stock": 100}]
resp = requests.post(
    "https://boogeyman-unknowing-amenity.ngrok-free.dev/convert",
    json={"data": data}
)
print(resp.text)
```

## Pricing

- $0.01 per request
- No signup, no API key
- Pay per use

## Why Use This?

- Zero setup
- Handles nested JSON flattening
- Works in any language
- Always available

Try it free: https://boogeyman-unknowing-amenity.ngrok-free.dev
