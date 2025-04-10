"""Module for retrieving data for S&P 500 and VIX."""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import pandas as pd

from trading_strategy_development.utils.custom_logging import get_logger

logger = get_logger(__name__)

# Type variable for retry decorator
T = TypeVar("T")


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of retry attempts.
        delay: Delay between attempts in seconds.

    Returns:
        Decorated function.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: dict[str, Any], **kwargs: dict[str, Any]) -> T:
            attempts = 0
            last_exception = None

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s",
                        attempts,
                        max_attempts,
                        func.__qualname__,
                        str(e),
                    )

                    if attempts < max_attempts:
                        logger.info("Retrying in %d seconds...", delay)
                        time.sleep(delay)
                    else:
                        logger.error(
                            "All %d attempts failed for %s",
                            max_attempts,
                            func.__qualname__,
                        )

            if last_exception:
                raise last_exception

            raise RuntimeError("Unexpected error in retry decorator")

        return wrapper

    return decorator


@retry(max_attempts=3, delay=2.0)
def get_sp500_tickers() -> list[str]:
    """Get a list of S&P 500 tickers using Wikipedia.

    Returns:
        List of S&P 500 ticker symbols.
    """
    try:
        logger.info("Attempting to get S&P 500 tickers from Wikipedia...")
        ticker_table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
        tickers: list[str] = ticker_table["Symbol"].str.replace(".", "-", regex=False).tolist()
        return tickers
    except Exception as e:
        logger.exception("Failed to get S&P 500 tickers from Wikipedia: ")
        raise ValueError("Could not retreive S&P tickers.") from e
