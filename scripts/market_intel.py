#!/usr/bin/env python3
"""
Tailor Made Market Intelligence Engine

Tracks flight prices and exchange rates for Tailor Made business intelligence.
Supports daily data collection and weekly reporting.

Usage:
    python3 market_intel.py track --type flights
    python3 market_intel.py track --type exchange
    python3 market_intel.py report --days 7
    python3 market_intel.py analyze --route MEX-CUN
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Data storage paths
DATA_DIR = Path(__file__).parent.parent / 'data' / 'market-intel'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Amadeus client (optional - set AMADEUS_API_KEY env var)
try:
    # Try to use Amadeus from clawdbot if available
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'clawd' / 'skills' / 'amadeus' / 'lib'))
    from client import AmadeusClient
    AMADEUS_AVAILABLE = True
except ImportError:
    AMADEUS_AVAILABLE = False
    AmadeusClient = None

# Key routes to monitor (Mexico-focused)
ROUTES = {
    'MEX-CUN': {'origin': 'MEX', 'destination': 'CUN', 'name': 'Ciudad de México → Cancún'},
    'MEX-MIA': {'origin': 'MEX', 'destination': 'MIA', 'name': 'Ciudad de México → Miami'},
    'MEX-JFK': {'origin': 'MEX', 'destination': 'JFK', 'name': 'Ciudad de México → Nueva York'},
    'MEX-LAX': {'origin': 'MEX', 'destination': 'LAX', 'name': 'Ciudad de México → Los Angeles'},
    'MEX-MAD': {'origin': 'MEX', 'destination': 'MAD', 'name': 'Ciudad de México → Madrid'},
    'MEX-CDG': {'origin': 'MEX', 'destination': 'CDG', 'name': 'Ciudad de México → París'},
}

# Currency pairs to track
CURRENCIES = ['USD', 'EUR', 'GBP']


def get_flight_prices(origin, destination, departure_date):
    """Get current flight prices from Amadeus."""
    if not AMADEUS_AVAILABLE:
        print(f"Warning: Amadeus not available, using mock data for {origin}-{destination}", file=sys.stderr)
        # Return mock data for demo when Amadeus not available
        mock_prices = {
            'MEX-CUN': [45.0, 48.0, 50.0, 52.0, 55.0],
            'MEX-MIA': [116.0, 180.0, 200.0, 220.0, 250.0],
            'MEX-JFK': [200.0, 220.0, 230.0, 240.0, 250.0],
            'MEX-LAX': [120.0, 150.0, 180.0, 200.0, 220.0],
            'MEX-MAD': [340.0, 350.0, 360.0, 370.0, 400.0],
            'MEX-CDG': [390.0, 400.0, 410.0, 420.0, 500.0],
        }
        route_key = f'{origin}-{destination}'
        return mock_prices.get(route_key, [100.0, 120.0, 150.0, 180.0, 200.0])

    try:
        client = AmadeusClient()
        response = client.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            adults=1,
            max_results=10
        )
        data = response.get('data', [])
        prices = []
        for offer in data:
            try:
                price = float(offer['price']['total'])
                prices.append(price)
            except (KeyError, TypeError, ValueError):
                continue
        return prices[:5]
    except Exception as e:
        print(f"Error fetching flights: {e}", file=sys.stderr)
        return []


def store_price_data(route_id, prices, data_type='flights'):
    """Store price data with timestamp."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().isoformat()

    file_path = DATA_DIR / f'{data_type}_{route_id}.json'
    existing_data = {}

    if file_path.exists():
        with open(file_path, 'r') as f:
            existing_data = json.load(f)

    if date_str not in existing_data:
        existing_data[date_str] = []

    existing_data[date_str].append({
        'timestamp': timestamp,
        'prices': prices,
        'avg_price': sum(prices) / len(prices) if prices else None,
        'min_price': min(prices) if prices else None,
        'max_price': max(prices) if prices else None,
    })

    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)

    return existing_data[date_str][-1]


def track_flights():
    """Track flight prices for all monitored routes."""
    print("Tracking flight prices...")

    results = []
    departure_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    for route_id, route_info in ROUTES.items():
        print(f"  {route_info['name']}...")

        prices = get_flight_prices(route_info['origin'], route_info['destination'], departure_date)

        if prices:
            result = store_price_data(route_id, prices, 'flights')
            results.append({
                'route': route_id,
                'name': route_info['name'],
                'data': result
            })
            print(f"    Avg: ${result['avg_price']:.2f} USD | Min: ${result['min_price']:.2f} USD")
        else:
            print(f"    No data available")

    return results


def track_exchange():
    """Track exchange rates (placeholder - needs real API)."""
    print("Tracking exchange rates...")

    # For MVP, using placeholder rates
    # In production: use汇率API or fetch from financial data source
    rates = {
        'MXN-USD': 17.22,
        'MXN-EUR': 18.75,
        'MXN-GBP': 21.50,
    }

    results = []
    for pair, rate in rates.items():
        result = {
            'timestamp': datetime.now().isoformat(),
            'rate': rate,
        }

        file_path = DATA_DIR / f'exchange_{pair}.json'
        existing_data = {}

        if file_path.exists():
            with open(file_path, 'r') as f:
                existing_data = json.load(f)

        date_str = datetime.now().strftime('%Y-%m-%d')
        existing_data[date_str] = result

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)

        results.append({
            'pair': pair,
            'data': result
        })
        print(f"  {pair}: {rate}")

    return results


def generate_weekly_report(days=7):
    """Generate weekly market intelligence report."""
    print("Generating weekly report...")

    report = {
        'generated_at': datetime.now().isoformat(),
        'period_days': days,
        'flights': {},
        'exchange': {},
        'insights': []
    }

    # Analyze flight trends
    for route_id in ROUTES.keys():
        file_path = DATA_DIR / f'flights_{route_id}.json'
        if not file_path.exists():
            continue

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Get recent days
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_data = {
            date: entries for date, entries in data.items()
            if date >= cutoff_date
        }

        if recent_data:
            all_avg_prices = []
            for entries in recent_data.values():
                for entry in entries:
                    if entry['avg_price']:
                        all_avg_prices.append(entry['avg_price'])

            if all_avg_prices:
                latest = list(recent_data.values())[-1][-1]
                oldest = list(recent_data.values())[0][0]

                trend = latest['avg_price'] - oldest['avg_price']
                trend_pct = (trend / oldest['avg_price'] * 100) if oldest['avg_price'] else 0

                report['flights'][route_id] = {
                    'name': ROUTES[route_id]['name'],
                    'latest_avg': latest['avg_price'],
                    'oldest_avg': oldest['avg_price'],
                    'trend': trend,
                    'trend_pct': round(trend_pct, 2),
                    'latest_min': latest['min_price'],
                }

                # Generate insight
                if trend_pct < -10:
                    report['insights'].append(
                        f"🔥 OFERTA: {ROUTES[route_id]['name']} bajó {abs(trend_pct):.1f}% "
                        f"(${latest['avg_price']:.0f} USD)"
                    )
                elif trend_pct > 15:
                    report['insights'].append(
                        f"⚠️ PRECIOS ALTOS: {ROUTES[route_id]['name']} subió {trend_pct:.1f}% "
                        f"(${latest['avg_price']:.0f} USD)"
                    )

    # Analyze exchange rates
    for currency in CURRENCIES:
        pair = f'MXN-{currency}'
        file_path = DATA_DIR / f'exchange_{pair}.json'
        if not file_path.exists():
            continue

        with open(file_path, 'r') as f:
            data = json.load(f)

        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_data = {
            date: entry for date, entry in data.items()
            if date >= cutoff_date
        }

        if recent_data:
            latest = recent_data[list(recent_data.keys())[-1]]
            oldest = recent_data[list(recent_data.keys())[0]]

            report['exchange'][pair] = {
                'latest': latest['rate'],
                'oldest': oldest['rate'],
                'change': latest['rate'] - oldest['rate'],
            }

            # MXN getting stronger vs foreign currency = good for Mexico→abroad travel
            change = latest['rate'] - oldest['rate']
            if change < -0.5:
                report['insights'].append(
                    f"💰 DÓLAR BARATO: MXN/{currency} subió {abs(change):.2f} "
                    f"(mejor para viajes a {currency})"
                )

    return report


def format_telegram_report(report):
    """Format report for Telegram."""
    lines = [
        "📊 *INFORME SEMANAL TAILOR MADE*",
        f"Periodo: {report['period_days']} días",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "✈️ *Vuelos*",
        ""
    ]

    for route_id, data in report['flights'].items():
        emoji = "📉" if data['trend'] < 0 else "📈" if data['trend'] > 0 else "➡️"
        lines.append(
            f"{emoji} {data['name']}\n"
            f"   Actual: ${data['latest_avg']:.0f} USD | "
            f"Min: ${data['latest_min']:.0f} USD\n"
            f"   Tendencia: {data['trend_pct']:+.1f}%"
        )

    if report['exchange']:
        lines.extend(["", "💱 *Tipo de Cambio*", ""])
        for pair, data in report['exchange'].items():
            change_emoji = "📉" if data['change'] < 0 else "📈"
            lines.append(
                f"{change_emoji} {pair}: {data['latest']:.2f} "
                f"({data['change']:+.2f})"
            )

    if report['insights']:
        lines.extend(["", "💡 *Oportunidades*", ""])
        for insight in report['insights']:
            lines.append(f"• {insight}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Tailor Made Market Intelligence')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Track command
    track_parser = subparsers.add_parser('track', help='Track data')
    track_parser.add_argument('--type', choices=['flights', 'exchange'], required=True,
                              help='Type of data to track')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate weekly report')
    report_parser.add_argument('--days', type=int, default=7,
                              help='Number of days to analyze (default: 7)')
    report_parser.add_argument('--format', choices=['json', 'telegram'], default='telegram',
                              help='Output format (default: telegram)')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze specific route')
    analyze_parser.add_argument('--route', choices=list(ROUTES.keys()), required=True,
                               help='Route to analyze')

    args = parser.parse_args()

    if args.command == 'track':
        if args.type == 'flights':
            results = track_flights()
            print(json.dumps(results, indent=2))
        else:
            results = track_exchange()
            print(json.dumps(results, indent=2))

    elif args.command == 'report':
        report = generate_weekly_report(days=args.days)
        if args.format == 'telegram':
            print(format_telegram_report(report))
        else:
            print(json.dumps(report, indent=2))

    elif args.command == 'analyze':
        file_path = DATA_DIR / f'flights_{args.route}.json'
        if not file_path.exists():
            print(f"No data found for route {args.route}", file=sys.stderr)
            sys.exit(1)

        with open(file_path, 'r') as f:
            data = json.load(f)

        print(f"\n{ROUTES[args.route]['name']}\n")
        print(f"{'Date':<12} {'Avg':<10} {'Min':<10} {'Max':<10}")
        print("-" * 42)

        for date in sorted(data.keys(), reverse=True)[:7]:
            entries = data[date]
            for entry in entries:
                if entry['avg_price']:
                    print(f"{date:<12} ${entry['avg_price']:<9.2f} "
                          f"${entry['min_price']:<9.2f} ${entry['max_price']:<9.2f}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
