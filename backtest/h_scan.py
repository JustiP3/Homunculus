# Retrieve historical bars for a given ticker for a hard-coded date range
# Store the bars in a local database for later retrieval and analysis

import os
from dotenv import load_dotenv

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from h_db import insert_historical_bar


# =====================================================
# CONFIG
# =====================================================

TICKER = "SPY"

START_DATE = "2025-01-01"
END_DATE = "2026-01-01"

TIMEFRAME = TimeFrame.Day


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise ValueError(
        "Missing ALPACA_API_KEY or ALPACA_SECRET_KEY in environment."
    )


# =====================================================
# CREATE CLIENT
# =====================================================

client = StockHistoricalDataClient(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)


# =====================================================
# DOWNLOAD HISTORICAL DATA
# =====================================================

request = StockBarsRequest(
    symbol_or_symbols=TICKER,
    timeframe=TIMEFRAME,
    start=START_DATE,
    end=END_DATE
)

bars = client.get_stock_bars(request)

spy_bars = bars.data[TICKER]

print(f"Retrieved {len(spy_bars)} bars")


# =====================================================
# SAVE TO DATABASE
# =====================================================

inserted = 0

for bar in spy_bars:

    insert_historical_bar(
        symbol=TICKER,
        timestamp=bar.timestamp.isoformat(),

        open_price=float(bar.open),
        high=float(bar.high),
        low=float(bar.low),
        close=float(bar.close),

        volume=int(bar.volume),

        vwap=float(bar.vwap)
        if bar.vwap is not None
        else None,

        trade_count=int(bar.trade_count)
        if bar.trade_count is not None
        else None,

        timeframe="1Day"
    )

    inserted += 1

print(f"Inserted {inserted} bars into historical_bars")
