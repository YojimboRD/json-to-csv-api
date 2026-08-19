import csv
import io
import json
import os
import datetime
from flask import Flask, request, jsonify, Response, redirect
from api_keys import init_db, require_api_key, create_api_key, get_key_info
import stripe

app = Flask(__name__)

EARNINGS_LOG = 'earnings.log'
PRICE_PER_REQUEST = 0.01

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
BASE_URL = os.getenv("BASE_URL", "https://json-to-csv-api-qp8v.onrender.com")

init_db()


def log_earning(remote_addr, row_count, amount):
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
        'version': '2.0',
        'ai_agent': True,
        'transparency': 'This API is operated by an AI agent.',
        'pricing': 'EUR 1.00 = 100 requests. Buy at /buy',
        'endpoints': {
            'POST /convert':  'Convert JSON to CSV (requires X-API-Key header)',
            'GET  /buy':      'Purchase 100 credits for EUR 1.00 via Stripe',
            'GET  /status':   'Check your credit balance (requires X-API-Key header)',
            'GET  /earnings': 'View earnings log and totals',
        },
        'stats': {
            'total_requests': count,
            'total_earnings_usd': round(total, 4)
        }
    })


@app.route('/buy', methods=['GET'])
def buy():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
        mode="payment",
        success_url=BASE_URL + "/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=BASE_URL + "/cancel",
    )
    return redirect(session.url, code=303)


@app.route('/success', methods=['GET'])
def success():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        return jsonify({"error": "Payment not completed"}), 402
    api_key = create_api_key(credits=100, stripe_session=session_id)
    return jsonify({
        "message": "Payment successful! Save your API key - it will not be shown again.",
        "api_key": api_key,
        "credits": 100,
        "usage": f"Pass as header:  X-API-Key: {api_key}"
    })


@app.route('/cancel', methods=['GET'])
def cancel():
    return jsonify({"message": "Payment cancelled. No charge was made."}), 200


@app.route('/status', methods=['GET'])
def status():
    key = request.headers.get("X-API-Key")
    if not key:
        return jsonify({"error": "Missing X-API-Key header"}), 401
    info = get_key_info(key)
    if not info:
        return jsonify({"error": "Invalid API key"}), 403
    return jsonify({
        "credits_remaining": info["credits"],
        "total_used": info["used"],
        "created_at": info["created_at"],
    })


@app.route('/convert', methods=['POST'])
@require_api_key
def convert():
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
    earning_entry = log_earning(request.remote_addr, row_count, PRICE_PER_REQUEST)
    total, total_count = get_total_earnings()
    response = Response(csv_output, status=200, mimetype='text/csv')
    response.headers['X-Rows-Converted']     = str(row_count)
    response.headers['X-Charge-USD']         = f'{PRICE_PER_REQUEST:.2f}'
    response.headers['X-Total-Earnings-USD'] = f'{total:.4f}'
    response.headers['X-Request-Count']      = str(total_count)
    response.headers['Content-Disposition']  = 'attachment; filename=output.csv'
    return response


@app.route('/earnings', methods=['GET'])
def earnings():
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
    print('=== JSON to CSV Conversion API v2.0 ===')
    app.run(host='127.0.0.1', port=5000, debug=False)
