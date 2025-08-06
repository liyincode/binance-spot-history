# Import required libraries
import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

try:
    import talib
    import numpy as np
    TALIB_AVAILABLE = True
    NUMPY_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    NUMPY_AVAILABLE = False
    try:
        import numpy as np
        NUMPY_AVAILABLE = True
    except ImportError:
        pass

    if not TALIB_AVAILABLE:
        print("Warning: TA-Lib not installed. MA calculations will use simple method.")
        print("Install TA-Lib for more accurate technical indicators: brew install ta-lib && pip install TA-Lib")

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

# Read MA periods from environment variables
try:
    ma_periods = [int(x.strip()) for x in os.getenv('MA_PERIODS', '7,25,99').split(',')]
except (ValueError, TypeError):
    ma_periods = [7, 25, 99]
# ----------------------------------------------------

def calculate_ma_simple(prices, period):
    """
    Calculate simple moving average using basic method (fallback when TA-Lib unavailable)
    """
    if len(prices) < period:
        return [None] * len(prices)

    ma_values = []
    for i in range(len(prices)):
        if i < period - 1:
            ma_values.append(None)
        else:
            ma_values.append(sum(prices[i-period+1:i+1]) / period)

    return ma_values

def calculate_technical_indicators(close_prices, ma_periods):
    """
    Calculate technical indicators including multiple moving averages
    """
    indicators = {}

    # Calculate moving averages
    for period in ma_periods:
        if TALIB_AVAILABLE and NUMPY_AVAILABLE:
            # Use TA-Lib for more accurate calculation
            close_array = np.array(close_prices, dtype=float)
            ma_values = talib.SMA(close_array, timeperiod=period)
            # Convert nan to None for JSON serialization
            ma_list = [None if np.isnan(x) else round(float(x), 6) for x in ma_values]
        else:
            # Use simple calculation as fallback
            ma_list = calculate_ma_simple(close_prices, period)
            ma_list = [None if x is None else round(float(x), 6) for x in ma_list]

        indicators[f'ma{period}'] = ma_list

    return indicators

def get_extended_date_range(start_date, end_date, max_ma_period):
    """
    Extend the date range backward to have enough data for MA calculation
    """
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    # Add extra days to ensure we have enough data for the longest MA
    extended_start_dt = start_dt - timedelta(days=max_ma_period + 10)
    return extended_start_dt.strftime('%Y-%m-%d')

def get_datetime_format(interval_str):
    """
    Determine appropriate datetime format based on interval
    """
    if interval_str in ['1d', '3d', '1w', '1M']:
        return '%Y-%m-%d'  # Date only for day/week/month intervals
    elif interval_str in ['1h', '2h', '4h', '6h', '8h', '12h']:
        return '%Y-%m-%d %H:%M'  # Date + hour for hourly intervals
    else:
        return '%Y-%m-%d %H:%M:%S'  # Full timestamp for minute intervals

def get_binance_history(symbol, interval, start_date, end_date, interval_str, include_ma=True):
    """
    Get historical K-line data for specified trading pair, time range and interval.
    Optionally include moving average calculations.
    """
    if not api_key or not api_secret:
        print("Error: API Key or Secret Key not configured in .env file.")
        return

    client = Client(api_key, api_secret)

    # Extend date range if MA calculation is needed
    original_start_date = start_date
    if include_ma and ma_periods:
        max_ma_period = max(ma_periods)
        extended_start_date = get_extended_date_range(start_date, end_date, max_ma_period)
        print(f"\nFetching extended data from {extended_start_date} to {end_date} for MA calculation...")
        fetch_start_date = extended_start_date
    else:
        fetch_start_date = start_date

    print(f"\nFetching {symbol} K-line data with {interval} interval from {fetch_start_date} to {end_date}...")

    try:
        # Convert date strings to timestamps (milliseconds)
        start_dt = datetime.strptime(fetch_start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        start_timestamp = int(start_dt.timestamp() * 1000)

        end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
        end_timestamp = int(end_dt.timestamp() * 1000)

        # Use timestamps to call API, avoiding date parsing warnings
        klines = client.get_historical_klines(symbol, interval, start_timestamp, end_timestamp)

        if not klines:
            print("No data found in the specified date range.")
            return

        # Process raw K-line data
        all_data = []
        close_prices = []

        for kline in klines:
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])
            change = close_price - open_price
            percentage_change = (change / open_price) * 100 if open_price != 0 else 0
            # Format datetime based on interval granularity
            datetime_format = get_datetime_format(interval_str)
            kline_datetime = datetime.fromtimestamp(kline[0] / 1000).strftime(datetime_format)

            day_data = {
                "datetime": kline_datetime,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
                "change": f"{change:.4f}",
                "percentage_change": f"{percentage_change:.2f}%"
            }
            all_data.append(day_data)
            close_prices.append(close_price)

        # Calculate technical indicators if requested
        if include_ma and ma_periods and len(close_prices) > 0:
            print("Calculating moving averages...")
            indicators = calculate_technical_indicators(close_prices, ma_periods)

            # Add MA values to each data point
            for i, data_point in enumerate(all_data):
                for ma_key, ma_values in indicators.items():
                    data_point[ma_key] = ma_values[i]

        # Filter data to original date range if we extended it
        if include_ma and ma_periods:
            original_start_dt = datetime.strptime(original_start_date, '%Y-%m-%d')
            datetime_format = get_datetime_format(interval_str)
            filtered_data = []
            for data_point in all_data:
                data_dt = datetime.strptime(data_point['datetime'], datetime_format)
                if data_dt.date() >= original_start_dt.date():
                    filtered_data.append(data_point)
            final_data = filtered_data
        else:
            final_data = all_data

        print("\n--- Data fetched successfully ---")
        if include_ma and ma_periods:
            ma_info = ", ".join([f"MA{p}" for p in ma_periods])
            print(f"Including technical indicators: {ma_info}")

        print(json.dumps(final_data, indent=4, ensure_ascii=False))

    except BinanceAPIException as e:
        print(f"Binance API Error: {e}")
    except BinanceRequestException as e:
        print(f"Binance Request Error: {e}")
    except Exception as e:
        print(f"Unknown error occurred: {e}")

if __name__ == "__main__":
    # --- 3. Use configuration from .env as default values for command line arguments ---
    parser = argparse.ArgumentParser(description='Get historical K-line data with technical indicators from Binance.')

    parser.add_argument('--symbol', type=str, default=default_symbol_env,
                        help=f'Trading pair, defaults to value configured in .env ({default_symbol_env}).')
    parser.add_argument('--start', type=str, default=None, help='Start date (YYYY-MM-DD).')
    parser.add_argument('--end', type=str, default=None, help='End date (YYYY-MM-DD).')
    parser.add_argument('--interval', type=str, default='1d',
                        help='K-line interval, defaults to 1d.')
    parser.add_argument('--no-ma', action='store_true',
                        help='Disable moving average calculations.')
    parser.add_argument('--ma-periods', type=str, default=None,
                        help='Comma-separated MA periods (e.g., "7,25,99"). Overrides .env settings.')
    # --------------------------------------------------------

    args = parser.parse_args()

    # Override MA periods if specified in command line
    if args.ma_periods:
        try:
            ma_periods = [int(x.strip()) for x in args.ma_periods.split(',')]
        except ValueError:
            print("Error: Invalid MA periods format. Use comma-separated numbers like '7,25,99'")
            exit(1)

    if args.start is None or args.end is None:
        # --- 4. Use days from .env to calculate default date range ---
        print(f"No dates specified, using default: querying past {default_days_env} days of data.")

        # Get UTC time to avoid timezone issues
        now_utc = datetime.now(timezone.utc)

        # Get recent N days of COMPLETE trading data
        # End date: yesterday (last complete trading day, avoiding incomplete current day data)
        end_date_obj = (now_utc - timedelta(days=1)).date()
        # Start date: N-1 days before end date to get exactly N complete days
        start_date_obj = end_date_obj - timedelta(days=default_days_env - 1)

        args.start = start_date_obj.strftime('%Y-%m-%d')
        args.end = end_date_obj.strftime('%Y-%m-%d')

        include_ma_info = " (with MA calculation)" if not args.no_ma else ""
        print(f"Actual query time range: {args.start} to {args.end}{include_ma_info}")
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
        include_ma = not args.no_ma
        get_binance_history(args.symbol, interval_map[args.interval], args.start, args.end, args.interval, include_ma)
