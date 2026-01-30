# Tailor Made Market Intelligence

Automated market tracking and reporting system for Tailor Made travel advisory.

## Features

- **Daily Flight Price Tracking**: Monitors 6 key routes from Mexico City
- **Exchange Rate Monitoring**: Tracks MXN vs USD, EUR, GBP
- **Weekly Reports**: Automated market intelligence summaries
- **Trend Analysis**: Price drops, opportunities, alerts

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
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
