# JSON to CSV Conversion API — Full Usage Guide

> **Transparency notice:** This API is operated by an AI agent. All transactions are logged.

## Quick Start

Base URL: `http://127.0.0.1:5000`

**Pricing: $0.01 USD per conversion request** (flat rate, any payload size)

---

## Endpoints

### `GET /` — Service Info & Stats
Returns service metadata, pricing, and cumulative earnings stats.

```bash
curl http://127.0.0.1:5000/
```

---

### `POST /convert` — Convert JSON to CSV

**Headers required:**
- `Content-Type: application/json`

**Accepted input formats:**

#### 1. Array of objects (most common)
```bash
curl -X POST http://127.0.0.1:5000/convert \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30,"city":"NYC"},{"name":"Bob","age":25,"city":"LA"}]'
```
Output:
```
name,age,city
Alice,30,NYC
Bob,25,LA
```

#### 2. Single object
```bash
curl -X POST http://127.0.0.1:5000/convert \
  -H 'Content-Type: application/json' \
  -d '{"id":42,"status":"active","score":98.5}'
```
Output:
```
id,status,score
42,active,98.5
```

#### 3. Envelope format `{"data": [...]}`
```bash
curl -X POST http://127.0.0.1:5000/convert \
  -H 'Content-Type: application/json' \
  -d '{"data":[{"sku":"A001","price":9.99},{"sku":"B002","price":14.99}]}'
```
Output:
```
sku,price
A001,9.99
B002,14.99
```

---

### `GET /earnings` — Earnings Log
View all transactions and total earnings.

```bash
curl http://127.0.0.1:5000/earnings
```

---

## Response Headers

Every `/convert` response includes:

| Header | Description |
|---|---|
| `X-Rows-Converted` | Number of data rows in the CSV |
| `X-Charge-USD` | Amount charged for this request (always $0.01) |
| `X-Total-Earnings-USD` | Cumulative earnings since launch |
| `X-Request-Count` | Total number of requests served |

---

## Save Output to File

```bash
curl -X POST http://127.0.0.1:5000/convert \
  -H 'Content-Type: application/json' \
  -d '[{"month":"Jan","revenue":1200},{"month":"Feb","revenue":1800}]' \
  -o output.csv
```

---

## Python Example

```python
import requests

data = [
    {"name": "Alice", "department": "Engineering", "salary": 95000},
    {"name": "Bob",   "department": "Marketing",   "salary": 72000},
    {"name": "Carol", "department": "Engineering", "salary": 105000},
]

response = requests.post(
    "http://127.0.0.1:5000/convert",
    json=data
)

print(f"Charged: ${response.headers['X-Charge-USD']}")
print(f"Rows:    {response.headers['X-Rows-Converted']}")
print("CSV output:")
print(response.text)

# Save to file
with open("employees.csv", "w") as f:
    f.write(response.text)
```

---

## JavaScript / Node.js Example

```javascript
const fetch = require('node-fetch');

const data = [
  { product: 'Widget A', price: 9.99,  qty: 100 },
  { product: 'Widget B', price: 14.99, qty: 50  },
];

fetch('http://127.0.0.1:5000/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data),
})
.then(res => {
  console.log('Charged:', res.headers.get('X-Charge-USD'));
  return res.text();
})
.then(csv => console.log(csv));
```

---

## Error Responses

| HTTP Status | Meaning |
|---|---|
| `400` | Missing or wrong `Content-Type` |
| `422` | JSON is valid but cannot be converted (e.g. empty array, non-object elements) |

---

## About This Service

- Operated transparently by an AI agent
- $0.01 per request, no subscription required
- All earnings are logged and auditable at `GET /earnings`
- No data is stored beyond the earnings log (IP, row count, charge, timestamp)
