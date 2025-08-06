# Binance Spot History

Python scripts to fetch historical K-line data for spot trading pairs from Binance API with optional technical analysis indicators.

## Features

- 📊 Fetch historical K-line data for any Binance spot trading pair
- 📈 **Technical Analysis**: Calculate moving averages (MA) and other indicators  
- ⏰ Support multiple time intervals (1m, 5m, 1h, 1d, etc.)
- 🔧 Configurable via environment variables and command line arguments
- 📅 Automatic date range calculation with intelligent defaults
- 🌍 UTC timezone handling to avoid data inconsistencies
- 💡 Smart datetime formatting based on time interval granularity
- 📊 Formatted output with price changes and percentage calculations
- 🔐 Secure API key management through environment variables

## Available Scripts

- **`get_spot_history.py`** - Basic K-line data fetching
- **`get_spot_history_with_ma.py`** - Enhanced version with technical indicators (moving averages)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/binance-spot-history.git
cd binance-spot-history
```

2. Install required dependencies:
```bash
# Basic dependencies (required for both scripts)
pip install python-binance python-dotenv
```

3. Install optional dependencies for technical analysis (only needed for `get_spot_history_with_ma.py`):
```bash
# Option A: TA-Lib (recommended for accurate technical indicators)
# First install the TA-Lib C library:
brew install ta-lib           # On macOS
# sudo apt-get install libta-lib-dev  # On Ubuntu/Debian
# Then install the Python wrapper:
pip install TA-Lib numpy
```

**Note**: If you only plan to use the basic `get_spot_history.py` script, you can skip the technical analysis dependencies.

4. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

5. Configure your `.env` file:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_DAYS_AGO=3
# Technical analysis settings (for get_spot_history_with_ma.py)
MA_PERIODS=7,25,99
```

## Getting Binance API Keys

1. Visit [Binance API Management](https://www.binance.com/en/my/settings/api-management)
2. Create a new API key
3. Enable "Enable Reading" permission (spot trading permission is NOT required)
4. Copy your API Key and Secret Key to the `.env` file

## Usage

### Basic K-line Data

Get the last 3 days of basic data for the default symbol (configured in .env):
```bash
python3 get_spot_history.py
```

Specify trading pair and date range:
```bash
python3 get_spot_history.py --symbol ETHUSDT --start 2024-01-01 --end 2024-01-31
```

### Technical Analysis with Moving Averages

Get data with technical indicators (uses default MA periods: 7, 25, 99):
```bash
python3 get_spot_history_with_ma.py
```

Specify custom MA periods:
```bash
python3 get_spot_history_with_ma.py --symbol BTCUSDT --ma-periods "5,20,50"
```

Disable MA calculations (same as basic script):
```bash
python3 get_spot_history_with_ma.py --no-ma
```

### Different Time Intervals

Get hourly data with technical indicators:
```bash
python3 get_spot_history_with_ma.py --symbol BTCUSDT --interval 1h --start 2024-01-01 --end 2024-01-02
```

Get minute-level data:
```bash
python3 get_spot_history.py --symbol ETHUSDT --interval 5m --start 2024-01-01 --end 2024-01-01
```

### Complete Examples

```bash
# Basic K-line data for 4-hour intervals
python3 get_spot_history.py --symbol ADAUSDT --interval 4h --start 2024-07-01 --end 2024-07-31

# Technical analysis with custom MA periods
python3 get_spot_history_with_ma.py --symbol BTCUSDT --interval 1d --ma-periods "10,30,100" --start 2024-07-01 --end 2024-07-31
```

## Supported Intervals

- **Minutes**: `1m`, `3m`, `5m`, `15m`, `30m`
- **Hours**: `1h`, `2h`, `4h`, `6h`, `8h`, `12h`
- **Days**: `1d`, `3d`
- **Weeks**: `1w`
- **Months**: `1M`

## Output Format

### Basic Output (get_spot_history.py)

```json
[
    {
        "datetime": "2024-07-31",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "change": "-0.0390",
        "percentage_change": "-5.52%"
    }
]
```

### Enhanced Output with Technical Indicators (get_spot_history_with_ma.py)

```json
[
    {
        "datetime": "2024-07-31",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "volume": 1234567.89,
        "change": "-0.0390",
        "percentage_change": "-5.52%",
        "ma7": 0.684857,
        "ma25": 0.70692,
        "ma99": 0.669121
    }
]
```

**Note**: DateTime format adjusts automatically based on interval:
- Daily intervals (`1d`, `3d`, `1w`, `1M`): `"2024-07-31"`
- Hourly intervals (`1h`, `2h`, etc.): `"2024-07-31 14:00"`  
- Minute intervals (`1m`, `5m`, etc.): `"2024-07-31 14:30:00"`

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BINANCE_API_KEY` | Your Binance API key | - | Yes |
| `BINANCE_API_SECRET` | Your Binance API secret | - | Yes |
| `DEFAULT_SYMBOL` | Default trading pair | `BTCUSDT` | No |
| `DEFAULT_DAYS_AGO` | Default number of days to fetch | `3` | No |
| `MA_PERIODS` | Moving average periods (comma-separated) | `7,25,99` | No |

### Command Line Arguments

#### Basic Script (get_spot_history.py)

| Argument | Description | Default |
|----------|-------------|---------|
| `--symbol` | Trading pair symbol | Value from `.env` |
| `--start` | Start date (YYYY-MM-DD) | Auto-calculated |
| `--end` | End date (YYYY-MM-DD) | Auto-calculated |
| `--interval` | K-line interval | `1d` |

#### Enhanced Script (get_spot_history_with_ma.py)

| Argument | Description | Default |
|----------|-------------|---------|
| `--symbol` | Trading pair symbol | Value from `.env` |
| `--start` | Start date (YYYY-MM-DD) | Auto-calculated |
| `--end` | End date (YYYY-MM-DD) | Auto-calculated |
| `--interval` | K-line interval | `1d` |
| `--no-ma` | Disable moving average calculations | False |
| `--ma-periods` | Custom MA periods (e.g., "5,20,50") | Value from `.env` |

## Error Handling

The scripts handle various error scenarios:

- **Missing API credentials**: Clear error message when API keys are not configured
- **Invalid trading pairs**: Binance API will return appropriate error messages
- **Network issues**: Handles connection timeouts and network errors
- **Invalid date formats**: Validates date input format
- **API rate limits**: Proper error handling for rate limit exceeded scenarios
- **Technical Analysis Dependencies**: 
  - Graceful fallback when TA-Lib is not installed (uses simple MA calculation)
  - Warning messages when optional dependencies are missing
  - Validation of MA periods format

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is for educational and research purposes only. Always ensure compliance with Binance's terms of service and applicable regulations in your jurisdiction.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/liyincode/binance-spot-history/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, operating system, and any error messages

---

⭐ If this project helped you, please consider giving it a star!
