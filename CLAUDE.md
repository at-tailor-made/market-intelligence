# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market intelligence automation system for Tailor Made travel advisory. Tracks flight prices on 6 key routes from Guadalajara (GDL) and exchange rates (MXN vs USD/EUR/GBP), generating daily data collection and weekly reports for business intelligence.

## Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Daily Operations
```bash
# Track flight prices (local only)
python scripts/market_intel.py track --type flights

# Track flight prices (save to Notion)
python scripts/market_intel.py track --type flights --notion

# Track exchange rates (save to Notion)
python scripts/market_intel.py track --type exchange --notion

# Generate weekly report (Telegram format)
python scripts/market_intel.py report --days 7 --format telegram

# Generate weekly report (JSON format, save to Notion)
python scripts/market_intel.py report --days 7 --format json --notion

# Analyze specific route
python scripts/market_intel.py analyze --route GDL-CUN
```

### Testing Commands
```bash
# Test flight tracking without API calls (uses mock data)
python scripts/market_intel.py track --type flights

# View recent data for a route
python scripts/market_intel.py analyze --route GDL-MIA
```

## Architecture

### Core Components

**scripts/market_intel.py** - Main engine with three operational modes:
- `track` mode: Collects current flight prices or exchange rates
- `report` mode: Analyzes historical data and generates weekly summaries
- `analyze` mode: Shows detailed history for a specific route

**Data Flow**:
1. Flight prices fetched from Amadeus API (or mock data if unavailable)
2. Exchange rates fetched from exchangerate-api.com (or fallback rates)
3. Data stored locally in `data/market-intel/` as timestamped JSON files
4. Optional: Data pushed to Notion database for visualization

### Data Storage Schema

Files in `data/market-intel/`:
- `flights_{ROUTE}.json`: Historical flight prices by date
  ```json
  {
    "2026-02-06": [{
      "timestamp": "2026-02-06T10:30:00",
      "prices": [100, 120, 150],
      "avg_price": 123.33,
      "min_price": 100,
      "max_price": 150
    }]
  }
  ```
- `exchange_{PAIR}.json`: Exchange rates by date
  ```json
  {
    "2026-02-06": {
      "timestamp": "2026-02-06T10:30:00",
      "rate": 17.22
    }
  }
  ```

### Monitored Routes

All routes originate from **Guadalajara (GDL)**, not Mexico City:
- `GDL-CUN`: Cancún (domestic leisure)
- `GDL-MIA`: Miami (US East Coast)
- `GDL-JFK`: New York (US East Coast)
- `GDL-LAX`: Los Angeles (US West Coast)
- `GDL-MAD`: Madrid (Europe)
- `GDL-CDG`: Paris (Europe)

Note: Legacy data exists for MEX (Mexico City) routes but is no longer actively tracked.

### External Dependencies

**Amadeus API** (optional):
- Requires `AmadeusClient` from `../clawd/skills/amadeus/lib/client.py`
- Falls back to mock data if unavailable
- Set `AMADEUS_API_KEY` environment variable to enable

**Exchange Rate API** (required for live rates):
- Service: exchangerate-api.com
- Set `EXCHANGERATE_API_KEY` environment variable
- Base URL in `EXCHANGERATE_URL` (defaults to v6 endpoint)
- Fetches MXN conversion rates, inverts to get foreign currency per MXN

**Notion Integration** (optional):
- Requires `notion-client` package
- Set `NOTION_API_KEY` environment variable
- Configure database ID in `data/notion-db-ids.json`
- Database must have properties: Name, Type, Route, Currency Pair, Avg Price, Min Price, Max Price, Trend, Exchange Rate, Insights, Report Data

### Automation

**Cron Jobs**:
- `cron-daily-flights.sh`: Runs daily at 14:00 UTC (8am CST) for flight tracking
- `cron-weekly-report.sh`: Runs Fridays at 12:00 UTC (6pm CST) for weekly reports

Both scripts:
1. Change to project directory (`/home/clawdbot/market-intelligence`)
2. Activate virtual environment
3. Execute market_intel.py with `--notion` flag

### Weekly Report Generation

Report logic in `generate_weekly_report()`:
- Compares latest vs oldest data over N days
- Calculates price trends and percentage changes
- Generates insights for significant changes:
  - Flight price drops >10%: "OFERTA" alert
  - Flight price increases >15%: "PRECIOS ALTOS" warning
  - Exchange rate changes >0.5: Currency opportunity alert

Output formats:
- `telegram`: Formatted with emojis for Telegram messaging
- `json`: Raw structured data

## Key Implementation Notes

- Exchange rate API returns "MXN per 1 foreign currency" but we need "foreign currency per 1 MXN", so rates are inverted (1/rate)
- Flight prices are for 30 days ahead from today (`departure_date = now + 30 days`)
- When Amadeus is unavailable, system uses hardcoded mock prices per route to maintain functionality
- All data files use ISO date format (YYYY-MM-DD) as keys for easy chronological sorting
- Notion integration is completely optional - system works standalone without it
