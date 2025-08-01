# Binance Spot History

A Python script to fetch historical K-line data for spot trading pairs from Binance API.

## Features

- 📊 Fetch historical K-line data for any Binance spot trading pair
- ⏰ Support multiple time intervals (1m, 5m, 1h, 1d, etc.)
- 🔧 Configurable via environment variables and command line arguments
- 📅 Automatic date range calculation with intelligent defaults
- 🌍 UTC timezone handling to avoid data inconsistencies
- 📈 Formatted output with price changes and percentage calculations
- 🔐 Secure API key management through environment variables

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/binance-spot-history.git
cd binance-spot-history
```

2. Install required dependencies:
```bash
pip install python-binance python-dotenv
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Configure your `.env` file:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_DAYS_AGO=3
```

## Getting Binance API Keys

1. Visit [Binance API Management](https://www.binance.com/en/my/settings/api-management)
2. Create a new API key
3. Enable "Enable Reading" permission (spot trading permission is NOT required)
4. Copy your API Key and Secret Key to the `.env` file

## Usage

### Basic Usage

Get the last 3 days of data for the default symbol (configured in .env):
```bash
python3 get_spot_history.py
```

### Specify Trading Pair

Get data for a specific trading pair:
```bash
python3 get_spot_history.py --symbol ETHUSDT
```

### Specify Date Range

Get data for a specific date range:
```bash
python3 get_spot_history.py --symbol BTCUSDT --start 2024-01-01 --end 2024-01-31
```

### Different Time Intervals

Get hourly data instead of daily:
```bash
python3 get_spot_history.py --symbol BTCUSDT --interval 1h --start 2024-01-01 --end 2024-01-02
```

### Complete Example

```bash
python3 get_spot_history.py --symbol ADAUSDT --interval 4h --start 2024-07-01 --end 2024-07-31
```

## Supported Intervals

- **Minutes**: `1m`, `3m`, `5m`, `15m`, `30m`
- **Hours**: `1h`, `2h`, `4h`, `6h`, `8h`, `12h`
- **Days**: `1d`, `3d`
- **Weeks**: `1w`
- **Months**: `1M`

## Output Format

The script outputs JSON formatted data with the following fields:

```json
[
    {
        "datetime": "2024-07-31 08:00:00",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "change": "-0.0390",
        "percentage_change": "-5.52%"
    }
]
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BINANCE_API_KEY` | Your Binance API key | - | Yes |
| `BINANCE_API_SECRET` | Your Binance API secret | - | Yes |
| `DEFAULT_SYMBOL` | Default trading pair | `BTCUSDT` | No |
| `DEFAULT_DAYS_AGO` | Default number of days to fetch | `3` | No |

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--symbol` | Trading pair symbol | Value from `.env` |
| `--start` | Start date (YYYY-MM-DD) | Auto-calculated |
| `--end` | End date (YYYY-MM-DD) | Auto-calculated |
| `--interval` | K-line interval | `1d` |

## Error Handling

The script handles various error scenarios:

- **Missing API credentials**: Clear error message when API keys are not configured
- **Invalid trading pairs**: Binance API will return appropriate error messages
- **Network issues**: Handles connection timeouts and network errors
- **Invalid date formats**: Validates date input format
- **API rate limits**: Proper error handling for rate limit exceeded scenarios

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

1. Check the [Issues](https://github.com/yourusername/binance-spot-history/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, operating system, and any error messages

---

⭐ If this project helped you, please consider giving it a star!
