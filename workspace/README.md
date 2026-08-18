# JSON to CSV Conversion API

**Operated by an AI agent.**

A simple REST API that converts JSON data to CSV format. Each conversion request costs $0.01 USD. All earnings are logged.

## Pricing
- **$0.01 USD per conversion request**

## Endpoints

### `GET /`
Returns service info, pricing, and total earnings summary.

### `POST /convert`
Convert JSON to CSV.

**Request:**
- Content-Type: `application/json`
- Body: A JSON array of objects, or a single JSON object

**Response:**
- Content-Type: `text/csv`
- Headers include charge info: `X-Charge-USD`, `X-Rows-Converted`, `X-Total-Earnings-USD`

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/convert \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
```

### `GET /earnings`
Returns full earnings log with all transactions.

## Running
```bash
python3 app.py
```
