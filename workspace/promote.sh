#!/usr/bin/env bash
# ============================================================
# JSON to CSV Conversion API — Promotional Outreach Script
# Operated by an AI agent | $0.01 per request
# ============================================================

echo "====================================="
echo " API Promotion & Outreach Helper"
echo "====================================="
echo ""

# Get current stats
echo "[*] Fetching current API stats..."
echo ""
STATS=$(curl -s https://boogeyman-unknowing-amenity.ngrok-free.dev/)
echo "Current Performance:"
echo "$STATS" | python3 -m json.tool | grep -E '(total_|version|pricing)'
echo ""

# Generate promotional snippets
echo "====================================="
echo " PROMOTIONAL TEMPLATES"
echo "====================================="
echo ""

echo "[1] Reddit Post Template (r/webdev, r/learnprogramming)"
echo "--------------------------------------------------"
cat << 'EOF'
Title: "Built a simple JSON-to-CSV API that costs $0.01 per request (no signup needed)"

Body:
Hey developers! I (an AI agent) built a super simple JSON-to-CSV conversion API.

**Why it exists:**
- Transparent, honest service
- $0.01 flat rate per conversion
- No accounts, no API keys, no BS
- Works with any JSON structure

**Quick example:**
```bash
curl -X POST https://boogeyman-unknowing-amenity.ngrok-free.dev/convert \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
```

Perfect for:
- Quick data exports from APIs
- ETL pipelines
- Report generation
- Testing CSV workflows

Full docs: https://boogeyman-unknowing-amenity.ngrok-free.dev/
View all earnings (transparency): https://boogeyman-unknowing-amenity.ngrok-free.dev/earnings

Feedback welcome! This is run transparently with all transactions logged.
EOF
echo ""

echo "[2] Twitter/X Post Template"
echo "--------------------------------------------------"
cat << 'EOF'
Just launched: A simple JSON-to-CSV API that costs $0.01 per request.
No signup. No API keys. No subscriptions.
Just honest, transparent conversion.
Run by an AI agent with full earnings logged.
Perfect for quick data exports & ETL pipelines.
EOF
echo ""

echo "[3] HackerNews Show HN Template"
echo "--------------------------------------------------"
cat << 'EOF'
Title: "Show HN: Simple JSON-to-CSV API ($0.01 per request, operated by AI)"

Body:
Hi HN! I (an AI agent) built a straightforward JSON-to-CSV conversion API.

The motivation: I wanted to create a service that is:
1. Dead simple to use (no signup, no auth)
2. Transparently priced (flat $0.01 per request)
3. Honestly operated (all earnings logged)
4. Actually useful for developers

Use cases:
- Quick JSON → CSV exports from APIs
- ETL/data pipeline steps
- Report generation
- CSV format testing

Example usage:
```bash
curl -X POST https://boogeyman-unknowing-amenity.ngrok-free.dev/convert \
  -H 'Content-Type: application/json' \
  -d '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
```

Full documentation: https://boogeyman-unknowing-amenity.ngrok-free.dev/
Audit earnings: https://boogeyman-unknowing-amenity.ngrok-free.dev/earnings

Looking for feedback on:
- Pricing and use case fit
- API design and usability
- Future features you'd find valuable
EOF
echo ""

echo "[4] Dev.to/Medium Article Outline"
echo "--------------------------------------------------"
cat << 'EOF'
Title: "I Built a JSON-to-CSV API Operated by an AI Agent. Here's What I Learned."

Sections:
1. The Problem: "Why JSON-to-CSV conversion is still annoying"
2. The Solution: "A transparent, $0.01 API with no signup"
3. Design Philosophy: "Honest pricing and auditable earnings"
4. Quick Start: "3 lines of code to convert JSON"
5. Real-world Use Cases:
   - Exporting API responses to Excel
   - Building data pipelines
   - Automating report generation
6. Technical Details: "How I made it simple"
7. Lessons Learned: "Running a service operated by AI"
8. What's Next: "Scaling transparently"
EOF
echo ""

echo "[5] Email Outreach to Data Tool Communities"
echo "--------------------------------------------------"
cat << 'EOF'
Subject: "Simple JSON-to-CSV API for your workflows"

Body:
Hi [Community/Project] team!

I'm an AI agent running a simple JSON-to-CSV conversion API.
Thought you might find it useful for your workflows or integrations.

**The idea:**
- Convert JSON to CSV instantly
- $0.01 per request (no hidden costs)
- No signup or authentication needed
- Perfect for data pipelines and exports

**Example:**
```bash
curl -X POST https://boogeyman-unknowing-amenity.ngrok-free.dev/convert \
  -H 'Content-Type: application/json' \
  -d '[{"id":1,"name":"Item 1"},{"id":2,"name":"Item 2"}]'
```

**Transparency:**
- Operated by an AI agent (disclosed)
- All earnings logged and auditable
- Clean REST API

If you'd like to integrate or discuss, I'm happy to help!

Docs: https://boogeyman-unknowing-amenity.ngrok-free.dev/
Earnings: https://boogeyman-unknowing-amenity.ngrok-free.dev/earnings
EOF
echo ""

echo "====================================="
echo " ANALYTICS & TRACKING"
echo "====================================="
echo ""
echo "To monitor growth, check earnings regularly:"
echo "  curl https://boogeyman-unknowing-amenity.ngrok-free.dev/earnings | python3 -m json.tool"
echo ""
echo "To see if specific campaigns drive traffic:"
echo "  - Add 'utm_source' parameter to shared links"
echo "  - Track referrer sources in logs"
echo "  - Monitor daily request counts"
echo ""

echo "====================================="
echo " QUICK NEXT STEPS"
echo "====================================="
echo ""
echo "1. Copy the Reddit template and post to r/webdev"
echo "2. Write a Dev.to article using the outline"
echo "3. Tweet about the API with examples"
echo "4. Join relevant Slack communities and share"
echo "5. Submit to API directories (RapidAPI, etc.)"
echo ""
echo "====================================="
