#!/usr/bin/env python3
"""
Setup script for Notion database for Market Intelligence

Creates the "Market Intelligence" database with required properties.
"""

import os
import sys
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("Error: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)

API_KEY = os.environ.get('NOTION_API_KEY')
if not API_KEY:
    print("Error: NOTION_API_KEY environment variable not set")
    sys.exit(1)

client = Client(auth=API_KEY)

# Search for parent database ID (we'll use the Integration's workspace)
# User needs to manually create the database and provide ID, or we search for it

print("Notion database setup requires manual configuration.")
print("\nSteps:")
print("1. Open Notion and create a new database named 'Market Intelligence'")
print("2. Add these properties:")
print("   - Name (title)")
print("   - Type (select): Daily Flights, Weekly Report, Exchange Rate")
print("   - Route (multi_select): MEX-CUN, MEX-MIA, MEX-JFK, MEX-LAX, MEX-MAD, MEX-CDG")
print("   - Currency Pair (multi_select): MXN-USD, MXN-EUR, MXN-GBP")
print("   - Avg Price (number)")
print("   - Min Price (number)")
print("   - Max Price (number)")
print("   - Trend (number)")
print("   - Exchange Rate (number)")
print("   - Insights (text)")
print("   - Report Data (text)")
print("\n3. Copy the database ID from the URL (32-character hex)")
print("4. Create data/notion-db-ids.json:")
print('   {"market_intel": "DATABASE_ID_HERE"}')
print("\nOr run: python scripts/setup_notion_db.py --db-id YOUR_DATABASE_ID")
