#!/bin/bash
# Market Intelligence - Weekly Report
# Cron job for Tailor Made (runs on Mondays)

cd /home/clawdbot/market-intelligence
source venv/bin/activate
python scripts/market_intel.py report --days 7 --format telegram --notion > /tmp/market-intel-weekly.txt
