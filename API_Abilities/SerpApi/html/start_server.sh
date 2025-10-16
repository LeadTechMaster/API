#!/bin/bash
# SerpApi Live Data Server Startup Script
# This script activates the virtual environment and starts the Flask server

echo "=========================================="
echo "🚀 Starting SerpApi Live Data Server"
echo "=========================================="

# Navigate to API root and activate venv
cd /Users/udishkolnik/API
source .venv/bin/activate

# Navigate to html folder and start server
cd /Users/udishkolnik/API/API_Abilities/SerpApi/html
python3 api_server.py

