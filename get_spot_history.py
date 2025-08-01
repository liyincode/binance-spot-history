# Import required libraries
import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

# --- 1. Load environment variables from .env file ---
load_dotenv()

# --- 2. Read configuration from environment variables with fallback defaults ---
# Read API keys
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Read default trading pair, defaults to 'BTCUSDT' if not set
default_symbol_env = os.getenv('DEFAULT_SYMBOL', 'BTCUSDT')

# Read default lookback days, defaults to 3 if not set or invalid format
try:
    default_days_env = int(os.getenv('DEFAULT_DAYS_AGO', '3'))
except (ValueError, TypeError):
    default_days_env = 3
# ----------------------------------------------------

def get_binance_history(symbol, interval, start_date, end_date):
    """
    Get historical K-line data for specified trading pair, time range and interval.
    """
    if not api_key or not api_secret:
        print("Error: API Key or Secret Key not configured in .env file.")
        return

    client = Client(api_key, api_secret)
    print(f"\nFetching {symbol} K-line data with {interval} interval from {start_date} to {end_date}...")

    try:
        # Convert date strings to timestamps (milliseconds)
        # Start time set to 00:00:00 of the day
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        start_timestamp = int(start_dt.timestamp() * 1000)

        # End time set to 23:59:59 of the day to ensure full day data is included
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
        end_timestamp = int(end_dt.timestamp() * 1000)

        # Use timestamps to call API, avoiding date parsing warnings
        klines = client.get_historical_klines(symbol, interval, start_timestamp, end_timestamp)

        if not klines:
            print("No data found in the specified date range.")
            return

        formatted_data = []
        for kline in klines:
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            change = close_price - open_price
            percentage_change = (change / open_price) * 100 if open_price != 0 else 0
            kline_datetime = datetime.fromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')

            day_data = {
                "datetime": kline_datetime, "open": open_price, "high": high_price,
                "low": low_price, "close": close_price, "change": f"{change:.4f}",
                "percentage_change": f"{percentage_change:.2f}%"
            }
            formatted_data.append(day_data)

        print("\n--- Data fetched successfully ---")
        print(json.dumps(formatted_data, indent=4, ensure_ascii=False))

    except BinanceAPIException as e:
        print(f"Binance API Error: {e}")
    except BinanceRequestException as e:
        print(f"Binance Request Error: {e}")
    except Exception as e:
        print(f"Unknown error occurred: {e}")

if __name__ == "__main__":
    # --- 3. Use configuration from .env as default values for command line arguments ---
    parser = argparse.ArgumentParser(description='Get historical K-line data for specified trading pairs from Binance.')

    parser.add_argument('--symbol', type=str, default=default_symbol_env,
                        help=f'Trading pair, defaults to value configured in .env ({default_symbol_env}).')
    parser.add_argument('--start', type=str, default=None, help='Start date (YYYY-MM-DD).')
    parser.add_argument('--end', type=str, default=None, help='End date (YYYY-MM-DD).')
    parser.add_argument('--interval', type=str, default='1d',
                        help='K-line interval, defaults to 1d.')
    # --------------------------------------------------------

    args = parser.parse_args()

    if args.start is None or args.end is None:
        # --- 4. Use days from .env to calculate default date range ---
        print(f"No dates specified, using default: querying past {default_days_env} days of data.")

        # Get UTC time to avoid timezone issues
        now_utc = datetime.now(timezone.utc)

        # Simple and direct logic: get recent N days of complete data
        # End date: yesterday (to ensure data completeness)
        end_date_obj = (now_utc - timedelta(days=1)).date()

        # Start date: N-1 days before end date
        start_date_obj = end_date_obj - timedelta(days=default_days_env - 1)

        args.start = start_date_obj.strftime('%Y-%m-%d')
        args.end = end_date_obj.strftime('%Y-%m-%d')

        print(f"Actual query time range: {args.start} to {args.end} (getting {default_days_env} days of complete data)")
        # ----------------------------------------------------

    interval_map = {
        '1m': Client.KLINE_INTERVAL_1MINUTE, '3m': Client.KLINE_INTERVAL_3MINUTE,
        '5m': Client.KLINE_INTERVAL_5MINUTE, '15m': Client.KLINE_INTERVAL_15MINUTE,
        '30m': Client.KLINE_INTERVAL_30MINUTE, '1h': Client.KLINE_INTERVAL_1HOUR,
        '2h': Client.KLINE_INTERVAL_2HOUR, '4h': Client.KLINE_INTERVAL_4HOUR,
        '6h': Client.KLINE_INTERVAL_6HOUR, '8h': Client.KLINE_INTERVAL_8HOUR,
        '12h': Client.KLINE_INTERVAL_12HOUR, '1d': Client.KLINE_INTERVAL_1DAY,
        '3d': Client.KLINE_INTERVAL_3DAY, '1w': Client.KLINE_INTERVAL_1WEEK,
        '1M': Client.KLINE_INTERVAL_1MONTH
    }

    if args.interval not in interval_map:
        print(f"Error: Invalid interval '{args.interval}'.")
    else:
        get_binance_history(args.symbol, interval_map[args.interval], args.start, args.end)
