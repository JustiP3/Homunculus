# Read bars
# Calculate indicators
# Write hisotrical snapshot 

# backtest/h_features.py

import pandas as pd

from backtest.h_db import (
    get_historical_bars,
    insert_historical_snapshot,
    create_historical_run
)

from core.indicators import compute_indicators, compute_features


TICKER = "SPY"


# =====================================================
# FEATURE ENGINEERING PIPELINE
# =====================================================

def build_features(run_id: int, symbol: str = TICKER):

    print(f"\n=== BUILDING FEATURES FOR {symbol} | RUN {run_id} ===\n")

    # -------------------------------------------------
    # 1. LOAD HISTORICAL BARS
    # -------------------------------------------------

    bars = get_historical_bars(symbol)

    if not bars:
        raise ValueError("No historical bars found.")

    df = pd.DataFrame(bars)

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Standardize column names for indicator library
    df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }, inplace=True)

    # -------------------------------------------------
    # 2. COMPUTE CORE INDICATORS
    # -------------------------------------------------

    df = compute_indicators(df)

    # -------------------------------------------------
    # 3. DERIVED FEATURES 
    # -------------------------------------------------

    df = compute_features(df)

    # -------------------------------------------------
    # 4. WRITE TO historical_snapshot
    # -------------------------------------------------

    inserted = 0

    for _, row in df.iterrows():

        # Skip rows where indicators are not ready yet
        if pd.isna(row["EMA200"]):
            continue

        insert_historical_snapshot(
            run_id=run_id,
            symbol=symbol,
            snapshot_time=row["timestamp"].isoformat(),

            close_price=float(row["Close"]),

            rsi=float(row["RSI"]) if not pd.isna(row["RSI"]) else None,
            atr=float(row["ATR"]) if not pd.isna(row["ATR"]) else None,

            ema_9=None,  # optional later
            ema_20=float(row["EMA20"]),
            ema_50=float(row["EMA50"]),
            ema_200=float(row["EMA200"]),

            relative_volume=float(row["RELATIVE_VOLUME"])
            if not pd.isna(row["RELATIVE_VOLUME"]) else None,

            distance_from_ema20=float(row["DIST_EMA20"]),
            distance_from_ema50=float(row["DIST_EMA50"]),
            distance_from_ema200=float(row["DIST_EMA200"]),

            vix=None,  # optional future enhancement

            #market_regime=row["MARKET_REGIME"],
            sector=None,

            scan_id="H_FEATURES_V1"
        )

        inserted += 1

    print(f"\nInserted {inserted} snapshots into historical_snapshot\n")


# =====================================================
# TEST RUN
# =====================================================

if __name__ == "__main__":

    run_id = create_historical_run(
        name="SPY Feature Build Test",
        description="Generate historical_snapshot from bars",
        strategy_version="v1.0",
        universe="SPY"
    )

    build_features(run_id, TICKER)