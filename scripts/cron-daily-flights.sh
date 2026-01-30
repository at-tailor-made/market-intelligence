#!/bin/bash
# Market Intelligence - Daily Flight Tracking
# Cron job for Tailor Made

cd /home/clawdbot/market-intelligence
source venv/bin/activate
python scripts/market_intel.py track --type flights >> data/flight-tracking.log 2>&1
