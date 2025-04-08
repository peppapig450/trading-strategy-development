# Trading Strategy Development

A modular Python program for predicting and backtesting trading strategies for S&P 500 stocks, with a focus on high-volatility market conditions.

## Overview

This project aims to develop and backtest trading strategies that perform well during periods of market stress. By analyzing historical data for all S&P 500 stocks during high-volatility days (when the VIX exceeds a specified threshold), the toolkit helps discover robust strategies that can navigate turbulent market conditions.

### Key Features

- **Data Acquisition**: Automated download of S&P 500 stock data and VIX index from Yahoo Finance
- **High-Volatility Filtering**: Focus on days when the VIX exceeds a user-defined threshold (default: 20)
- **Feature Engineering**: Calculation of technical indicators (SMAs, RSI, volatility, etc.)
- **Statistical Analysis**: Correlations, ARIMA modeling, market regime analysis
- **Predictive Modeling**: Machine learning models to predict next-day returns
- **Backtesting**: Validation of strategies using Backtrader
- **Visualization**: Performance charts, feature importance, equity curves

## Installation

### Prerequisites

- Python 3.12+
- Poetry 2.x.x

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/peppapig450/trading-strategy-development.git
   cd trading-strategy-development
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

## Project Structure

```
trading-strategy-development/
├── src/
│   └── trading_strategy_development/
│       ├── data/                 # Data acquisition and processing modules
│       │   ├── retrieval.py      # Download S&P 500 and VIX data
│       │   ├── filters.py        # Filter for high-volatility days
│       │   ├── features.py       # Technical indicator calculations
│       │   ├── io.py             # Data I/O operations
│       │   └── stats.py          # Statistical analysis
│       │
│       ├── models/               # Predictive models
│       │   ├── base.py           # Base model class
│       │   ├── xgboost_model.py  # XGBoost implementation
│       │   └── ...               # Other model implementations
│       │
│       ├── strategies/           # Trading strategies
│       │   ├── base_strategy.py  # Base strategy class
│       │   ├── prediction_based.py # Strategies using model predictions
│       │   └── ...               # Other strategies
│       │
│       ├── backtest/             # Backtesting framework
│       │   ├── engine.py         # Backtrader setup
│       │   ├── analyzers.py      # Performance metrics
│       │   └── ...               # Other backtest utilities
│       │
│       ├── visualize/            # Data visualization
│       │   ├── performance.py    # Performance charts
│       │   ├── feature_importance.py # Feature importance plots
│       │   └── ...               # Other visualization utilities
│       │
│       ├── utils/                # Utility functions
│       │   ├── logging.py        # Logging setup and configuration
│       │   └── ...               # Other utility modules
│       │
│       └── main.py               # Main entry point
│
├── tests/                        # Unit and integration tests
│   ├── test_data/
│   ├── test_models/
│   ├── test_utils/               # Tests for utility functions
│   └── ...
│
├── notebooks/                    # Jupyter notebooks for exploration and examples
├── pyproject.toml                # Poetry configuration
└── README.md                     # Project documentation
```

## Usage

### Basic Usage

```bash
# Run with default settings (VIX threshold = 20)
python -m trading_strategy_development.main

# Specify a different VIX threshold
python -m trading_strategy_development.main --vix 25

# Use a specific model
python -m trading_strategy_development.main --model xgboost

# Backtest a specific strategy
python -m trading_strategy_development.main --strategy prediction_based

# Specify date range
python -m trading_strategy_development.main --start-date 2020-01-01 --end-date 2023-12-31

# Save results to a specific directory
python -m trading_strategy_development.main --output-dir results/custom_run
```

### Example Workflow

1. **Data Acquisition and Processing**:

   ```python
   from trading_strategy_development.data import (
       get_stock_and_vix_data,
       filter_high_volatility_days,
       engineer_features,
       create_output_directory,
       save_stock_data
   )

   # Get S&P 500 and VIX data
   stock_data = get_stock_and_vix_data(period="5y")

   # Filter for high-volatility days
   high_vol_data = filter_high_volatility_days(stock_data, vix_threshold=20)

   # Engineer features
   features_data = engineer_features(high_vol_data)

   # Save processed data
   output_dir = create_output_directory()
   save_stock_data(features_data, output_dir=output_dir)
   ```

2. **Analysis and Modeling**:

   ```python
   from trading_strategy_development.data.stats import (
       calculate_summary_statistics,
       calculate_correlations
   )
   from trading_strategy_development.models.xgboost_model import XGBoostModel

   # Analyze correlations
   correlations = calculate_correlations(
       features_data, 
       target_col="next_day_return", 
       output_dir=output_dir,
       plot=True
   )

   # Calculate summary statistics
   stats = calculate_summary_statistics(
       features_data,
       output_dir=output_dir
   )

   # Train a model (will be implemented in future versions)
   # model = XGBoostModel()
   # model.train(train_data, valid_data)
   ```

3. **Backtesting** (planned for future implementation):

   ```python
   # This functionality will be available in future versions
   from trading_strategy_development.backtest.engine import BacktestEngine
   from trading_strategy_development.strategies.prediction_based import PredictionBasedStrategy

   engine = BacktestEngine(test_data)
   results = engine.run(PredictionBasedStrategy, params={"model": model})
   ```

4. **Visualization** (planned for future implementation):

   ```python
   # This functionality will be available in future versions
   from trading_strategy_development.visualize.performance import plot_equity_curve
   from trading_strategy_development.visualize.feature_importance import plot_feature_importance

   plot_equity_curve(results, output_dir=output_dir)
   plot_feature_importance(model, output_dir=output_dir)
   ```

## Data Sources

- Stock data is retrieved from Yahoo Finance via the `yfinance` package
- S&P 500 constituent list is retrieved from either `yfinance` or Wikipedia
- VIX data is retrieved from Yahoo Finance using the ticker `^VIX`

## Development

For development, it's recommended to install the package in editable mode:

```bash
# Install in development mode
poetry install

# Activate the virtual environment
poetry shell

# Run linting and formatting
ruff check .
ruff format .

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`poetry install`)
4. Make your changes
5. Run tests and formatting (`pytest` and `ruff format .`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
