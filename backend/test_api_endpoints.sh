#!/bin/bash
# Test all API endpoints

echo "==================================================================="
echo "Testing F1 Strategy Room API Endpoints"
echo "==================================================================="

API_BASE="http://localhost:8002"

echo ""
echo "1. GET /api/races/2023"
echo "-------------------------------------------------------------------"
curl -s "$API_BASE/api/races/2023" | python -m json.tool | head -30

echo ""
echo ""
echo "2. POST /api/degradation (Monza 2023)"
echo "-------------------------------------------------------------------"
curl -s -X POST "$API_BASE/api/degradation" \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "race": "Monza", "session": "R"}' \
  | python -m json.tool | head -50

echo ""
echo ""
echo "3. POST /api/strategy (Monza 2023)"
echo "-------------------------------------------------------------------"
curl -s -X POST "$API_BASE/api/strategy" \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "race": "Monza", "session": "R"}' \
  | python -m json.tool | head -60

echo ""
echo ""
echo "4. POST /api/overtakes (Monza 2023)"
echo "-------------------------------------------------------------------"
curl -s -X POST "$API_BASE/api/overtakes" \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "race": "Monza", "session": "R"}' \
  | python -m json.tool

echo ""
echo "==================================================================="
echo "All endpoints tested!"
echo "==================================================================="
