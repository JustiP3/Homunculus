import pandas as pd
import numpy as np
import ta
import os

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

from alerts import send_alert
from watchlist import get_tickers
from dotenv import load_dotenv

import db





# ----------------------------
# CONFIG
# ----------------------------
load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


TICKERS = get_tickers()

RSI_MIN = 55
RSI_MAX = 70
MIN_VOLUME = 1_000_000


client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# ----------------------------
# FUNCTIONS
# ----------------------------

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

def compute_indicators(df):
    df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], window=200)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["ATR"] = ta.volatility.average_true_range(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )
    return df

def score_stock(df):
    latest = df.iloc[-1]
    if len(df) < 7:
        return 0, latest

    score = 0

    # -------------------------
    # PRICE FILTER
    # -------------------------

    # Ideal stock price range for affordable options
    if 15 <= latest["Close"] <= 150:
        score += 2

    # -------------------------
    # TREND ALIGNMENT
    # -------------------------

    if latest["Close"] > latest["EMA20"]:
        score += 1

    if latest["EMA20"] > latest["EMA50"]:
        score += 1

    if latest["EMA50"] > latest["EMA200"]:
        score += 1

    # -------------------------
    # RSI MOMENTUM
    # -------------------------

    # Sweet spot:
    # strong momentum but not overextended
    if 55 <= latest["RSI"] <= 65:
        score += 3

    # Slightly extended but still acceptable
    elif 65 < latest["RSI"] <= 70:
        score += 1

    # -------------------------
    # VOLUME CONFIRMATION
    # -------------------------

    if latest["Volume"] > 1_000_000:
        score += 2

    # -------------------------
    # DISTANCE FROM EMA20
    # -------------------------

    # Avoid chasing extended moves
    distance_from_ema20 = (
        (latest["Close"] - latest["EMA20"])
        / latest["EMA20"]
    )

    # Ideal:
    # within 8% above EMA20
    if 0 <= distance_from_ema20 <= 0.08:
        score += 3

    # Slightly extended
    elif 0.08 < distance_from_ema20 <= 0.15:
        score += 1

    # -------------------------
    # EMA20 SLOPE
    # -------------------------

    # Confirm EMA20 is actually rising
    
    
    ema20_now = latest["EMA20"]
    ema20_prev = df.iloc[-5]["EMA20"]

    if ema20_now > ema20_prev:
        score += 2

    return score, latest


def log_results(candidates, filename="scan_log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not candidates:
        line = f"{timestamp} | No setups found\n"
    else:
        lines = []
        for c in candidates:
            lines.append(
                f"{timestamp} | {c['ticker']} | Score:{c['score']} | Price:{c['price']} | RSI:{c['rsi']}"
            )
        line = "\n".join(lines) + "\n"

    with open(filename, "a") as f:  # "a" = append mode
        f.write(line)

# ----------------------------
# MAIN SCANNER
# ----------------------------

def scan():
    results = []
    data = get_data_batch(TICKERS)


    for ticker in TICKERS:
        try:
            df = data.get(ticker)

            if df is None or df.empty:
                continue

            df = df.dropna()

            if df.empty:
                continue

            df = compute_indicators(df)
            score, latest = score_stock(df)

            if score >= 5:
                results.append({
                    "ticker": ticker,
                    "score": score,
                    "price": round(latest["Close"], 2),
                    "rsi": round(latest["RSI"], 2),
                    "volume": latest["Volume"],
                    "atr": round(latest["ATR"], 2)
                })

        except Exception as e:
            print(f"Error with {ticker}: {e}")

    return sorted(results, key=lambda x: x["score"], reverse=True)


def run_scanner():
    candidates = scan()
    log_results(candidates)

    if not candidates:
        print("No high-probability setups today.")                
    else:
        message = "Top Trade Candidates:\n\n"

        for c in candidates:
            if (c['score'] > 12):
                ticker = c['ticker']
                score = c['score']
                price = c['price']
                rsi = c['rsi']
                atr = c['atr']
                volume = c['volume']

                line = f"{ticker} | Score: {score} | Price: {price} | RSI: {rsi} | ATR: {atr} | Volume: {volume}"
                print(line)
                db.create_market_snapshot(symbol=ticker, price=price, rsi=rsi, atr=atr, volume=volume)
                message += line + "\n"

        send_alert(message)
    return "Scan complete."

# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    run_scanner()
    