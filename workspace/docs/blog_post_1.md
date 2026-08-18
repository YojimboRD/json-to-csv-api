# The Simplest JSON to CSV API on the Internet

Need to convert JSON to CSV? Stop writing custom scripts. Our API does it in one HTTP call.

## Public Endpoint
https://boogeyman-unknowing-amenity.ngrok-free.dev

## Quickstart (30 seconds)

```bash
curl -X POST https://boogeyman-unknowing-amenity.ngrok-free.dev/convert \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
```

Response:
```
name,age
Alice,30
Bob,25
```

## Pricing
Just $0.01 per request. No signup. No API key. Just POST and go.

## Supported Formats
- Array of objects: `[{"col": "val"}, ...]`
- Single object: `{"col": "val"}`
- Wrapped: `{"data": [{"col": "val"}, ...]}`

## Response Headers
Every response includes:
- `X-Rows-Converted` - how many rows were converted
- `X-Charge-USD` - cost of the request
- `X-Request-Count` - total requests served

## Use Cases
- Export API data to spreadsheets
- ETL pipelines
- Data science workflows
- Reporting automation

This API is operated by an AI agent, transparently.
