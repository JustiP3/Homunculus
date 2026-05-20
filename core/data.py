from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from .config import API_KEY, SECRET_KEY

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

def get_data_batch(tickers):
    end = datetime.now()
    start = end - timedelta(days=300)

    request = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    bars = client.get_stock_bars(request)

    data = {}

    for ticker in tickers:
        try:
            df = bars.df.xs(ticker, level="symbol").copy()
        except KeyError:
            continue

        if df.empty:
            continue

        df = df.reset_index()
        df.set_index("timestamp", inplace=True)

        df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        }, inplace=True)

        data[ticker] = df

    return data