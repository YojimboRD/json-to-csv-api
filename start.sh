#!/bin/bash
cd /mnt/f/automaton
source venv/bin/activate

echo "Starting Automaton ecosystem..."

if ! curl -s http://127.0.0.1:5000/ > /dev/null 2>&1; then
    echo "Starting Flask API..."
    cd workspace
    nohup python3 app.py > ../logs/api.log 2>&1 &
    echo "Flask API started (PID: $!)"
    cd ..
    sleep 2
else
    echo "Flask API already running ✓"
fi

echo "Starting Cloudflare tunnel..."
nohup cloudflared tunnel --url http://localhost:5000 > logs/tunnel.log 2>&1 &
sleep 6
TUNNEL_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' logs/tunnel.log | head -1)

echo "Starting heartbeat..."
nohup python3 heartbeat.py > logs/heartbeat.log 2>&1 &
echo "Heartbeat started"

echo ""
echo "======================================================"
echo " AUTOMATON IS LIVE"
echo "======================================================"
echo " Public URL: $TUNNEL_URL"
echo ""
echo " ⚠️  URL CHANGED? Update these Dev.to posts:"
echo "   https://dev.to/yojimbo/convert-json-to-csv-in-one-api-call-165c"
echo "   https://dev.to/yojimbo/json-to-csv-api-etl-made-effortless-404f"
echo "   https://dev.to/yojimbo/stop-writing-json-to-csv-code-use-this-api-instead-2jhd"
echo "======================================================"
echo ""

python3 main.py
