#!/usr/bin/env bash
# ============================================================
# JSON to CSV Conversion API — Demo Script
# Operated by an AI agent | $0.01 per request
# ============================================================

BASE="http://127.0.0.1:5000"

echo "====================================="
echo " JSON → CSV Conversion API Demo"
echo " AI-operated | \$0.01 per request"
echo "====================================="
echo ""

# --- 1. Service info ---
echo "[1] Service Info & Current Stats"
echo "----------------------------------"
curl -s "$BASE/" | python3 -m json.tool
echo ""

# --- 2. Array of objects ---
echo "[2] Convert Array of Objects"
echo "----------------------------------"
curl -s -X POST "$BASE/convert" \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30,"city":"New York"},{"name":"Bob","age":25,"city":"Los Angeles"},{"name":"Carol","age":35,"city":"Chicago"}]' \
  -D - 2>&1
echo ""

# --- 3. Single object ---
echo "[3] Convert Single Object"
echo "----------------------------------"
curl -s -X POST "$BASE/convert" \
  -H 'Content-Type: application/json' \
  -d '{"id":1001,"status":"shipped","total":49.95}' \
  -D - 2>&1
echo ""

# --- 4. Envelope format ---
echo "[4] Convert Envelope Format {\"data\": [...]}"
echo "----------------------------------"
curl -s -X POST "$BASE/convert" \
  -H 'Content-Type: application/json' \
  -d '{"data":[{"month":"Jan","revenue":12000,"expenses":8000},{"month":"Feb","revenue":15000,"expenses":9500}]}' \
  -D - 2>&1
echo ""

# --- 5. Save to file ---
echo "[5] Save CSV Output to File"
echo "----------------------------------"
curl -s -X POST "$BASE/convert" \
  -H 'Content-Type: application/json' \
  -d '[{"sku":"A001","price":9.99,"stock":100},{"sku":"B002","price":24.99,"stock":45}]' \
  -o /tmp/products.csv
echo "Saved to /tmp/products.csv:"
cat /tmp/products.csv
echo ""

# --- 6. Earnings summary ---
echo "[6] Earnings Log"
echo "----------------------------------"
curl -s "$BASE/earnings" | python3 -m json.tool
echo ""

echo "====================================="
echo " Demo complete!"
echo "====================================="
