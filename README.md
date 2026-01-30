# Tailor Made Market Intelligence

Automated market tracking and reporting system for Tailor Made travel advisory.

## Features

- **Daily Flight Price Tracking**: Monitors 6 key routes from Mexico City
- **Exchange Rate Monitoring**: Tracks MXN vs USD, EUR, GBP
- **Weekly Reports**: Automated market intelligence summaries
- **Trend Analysis**: Price drops, opportunities, alerts
- **Notion Integration**: Save all data to Notion database for easy access

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Notion Setup

1. **Create Notion Database**:
   - Open Notion and create a new database named "Market Intelligence"
   - Add these properties:
     - **Name** (title)
     - **Type** (select): Daily Flights, Weekly Report, Exchange Rate
     - **Route** (multi_select): MEX-CUN, MEX-MIA, MEX-JFK, MEX-LAX, MEX-MAD, MEX-CDG
     - **Currency Pair** (multi_select): MXN-USD, MXN-EUR, MXN-GBP
     - **Avg Price** (number)
     - **Min Price** (number)
     - **Max Price** (number)
     - **Trend** (number) - % change for weekly reports
     - **Exchange Rate** (number)
     - **Insights** (text)
     - **Report Data** (text)

2. **Configure Database ID**:
   - Copy the 32-character database ID from the Notion URL
   - Update `data/notion-db-ids.json`:
     ```json
     {
       "market_intel": "YOUR_DATABASE_ID_HERE"
     }
     ```

3. **Set Environment Variable**:
   ```bash
   export NOTION_API_KEY="your_integration_token"
   ```

## Usage

```bash
# Track flight prices (without Notion)
python scripts/market_intel.py track --type flights

# Track flight prices (with Notion save)
python scripts/market_intel.py track --type flights --notion

# Track exchange rates (with Notion save)
python scripts/market_intel.py track --type exchange --notion

# Generate weekly report
python scripts/market_intel.py report --days 7 --format telegram

# Generate weekly report (with Notion save)
python scripts/market_intel.py report --days 7 --notion

# Analyze specific route
python scripts/market_intel.py analyze --route MEX-CUN
```

## Usage

```bash
# Track flight prices
python scripts/market_intel.py track --type flights

# Track exchange rates
python scripts/market_intel.py track --type exchange

# Generate weekly report
python scripts/market_intel.py report --days 7 --format telegram

# Analyze specific route
python scripts/market_intel.py analyze --route MEX-CUN
```

## Monitored Routes

- MEX → CUN (Cancún) — Domestic leisure
- MEX → MIA (Miami) — US East Coast
- MEX → JFK (New York) — US East Coast
- MEX → LAX (Los Angeles) — US West Coast
- MEX → MAD (Madrid) — Europe
- MEX → CDG (Paris) — Europe

## Cron Jobs

```bash
# Daily flight tracking at 14:00 UTC (~8am Mexico City)
0 14 * * * /path/to/market-intelligence/cron-daily-flights.sh

# Weekly report on Mondays at 15:00 UTC
0 15 * * 1 /path/to/market-intelligence/cron-weekly-report.sh
```

## Data Storage

All data stored in `data/market-intel/` as JSON with timestamps.

## License

Proprietary - Tailor Made
