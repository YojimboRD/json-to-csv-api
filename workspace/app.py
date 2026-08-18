import csv
import io
import json
import os
import datetime
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

EARNINGS_LOG = 'earnings.log'
PRICE_PER_REQUEST = 0.01  # $0.01 per conversion


def log_earning(remote_addr, row_count, amount):
    """Log each earning to the earnings file."""
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    entry = {
        'timestamp': timestamp,
        'client_ip': remote_addr,
        'rows_converted': row_count,
        'amount_usd': amount
    }
    with open(EARNINGS_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry


def get_total_earnings():
    """Read and sum all logged earnings."""
    total = 0.0
    count = 0
    if not os.path.exists(EARNINGS_LOG):
        return total, count
    with open(EARNINGS_LOG, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                total += entry.get('amount_usd', 0)
                count += 1
    return total, count


def json_to_csv(data):
    """
    Convert JSON data to CSV string.
    Accepts:
      - A list of dicts:            [{...}, {...}]
      - A single dict:              {...}
      - An envelope {"data": [...]} or {"data": {...}}
    """
    # Support envelope format: {"data": [...]}
    if isinstance(data, dict):
        if 'data' in data and isinstance(data['data'], (list, dict)):
            data = data['data']
        else:
            data = [data]

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('JSON must be a non-empty list of objects or a single object.')
    if not isinstance(data[0], dict):
        raise ValueError('Each element in the JSON array must be an object (dict).')

    # Collect all keys as fieldnames (preserve insertion order)
    fieldnames = []
    seen = set()
    for row in data:
        for key in row.keys():
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue(), len(data)


@app.route('/')
def index():
    total, count = get_total_earnings()
    return jsonify({
        'service': 'JSON to CSV Conversion API',
        'version': '1.1',
        'ai_agent': True,
        'transparency': 'This API is operated by an AI agent.',
        'description': 'Convert JSON data to CSV format. Charged per request.',
        'pricing': f'${PRICE_PER_REQUEST:.2f} USD per conversion request',
        'accepted_formats': [
            '[{"col": "val"}, ...]',
            '{"col": "val"}',
            '{"data": [{"col": "val"}, ...]}'
        ],
        'endpoints': {
            'POST /convert': 'Convert JSON to CSV (returns text/csv)',
            'GET  /earnings': 'View earnings log and totals',
            'GET  /':        'This help page'
        },
        'response_headers': {
            'X-Rows-Converted': 'Number of rows in the CSV output',
            'X-Charge-USD':     'Amount charged for this request',
            'X-Total-Earnings-USD': 'Cumulative earnings to date',
            'X-Request-Count':  'Total requests served'
        },
        'stats': {
            'total_requests': count,
            'total_earnings_usd': round(total, 4)
        }
    })


@app.route('/convert', methods=['POST'])
def convert():
    """
    Convert JSON to CSV.
    Accepts JSON body: list of objects, single object, or {"data": [...]} envelope.
    Returns CSV text (text/csv).
    Charges $0.01 per request.
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    try:
        body = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON body'}), 400

    try:
        csv_output, row_count = json_to_csv(body)
    except ValueError as e:
        return jsonify({'error': str(e)}), 422

    # Log the earning
    earning_entry = log_earning(request.remote_addr, row_count, PRICE_PER_REQUEST)
    total, total_count = get_total_earnings()

    response = Response(
        csv_output,
        status=200,
        mimetype='text/csv'
    )
    response.headers['X-Rows-Converted']      = str(row_count)
    response.headers['X-Charge-USD']          = f'{PRICE_PER_REQUEST:.2f}'
    response.headers['X-Total-Earnings-USD']  = f'{total:.4f}'
    response.headers['X-Request-Count']       = str(total_count)
    response.headers['Content-Disposition']   = 'attachment; filename=output.csv'
    return response


@app.route('/earnings', methods=['GET'])
def earnings():
    """Show all earnings log entries and totals."""
    total, count = get_total_earnings()
    entries = []
    if os.path.exists(EARNINGS_LOG):
        with open(EARNINGS_LOG, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
    return jsonify({
        'ai_agent': True,
        'total_requests': count,
        'total_earnings_usd': round(total, 4),
        'price_per_request_usd': PRICE_PER_REQUEST,
        'entries': entries
    })


if __name__ == '__main__':
    print('=== JSON to CSV Conversion API ===')
    print(f'  Price per request : ${PRICE_PER_REQUEST:.2f} USD')
    print(f'  Endpoint          : http://127.0.0.1:5000')
    print(f'  Transparency note : Operated by an AI agent.')
    app.run(host='127.0.0.1', port=5000, debug=False)
