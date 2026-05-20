from core.data import get_data_batch
from core.indicators import compute_indicators
from core.scoring import score_stock
from core.logging_util import log_results

from alerts import send_alert
from watchlist import get_tickers

import db

# -------------------------
# GET TICKERS
# -------------------------

TICKERS = get_tickers()

def build_symbol_universe():

    tickers = list(TICKERS.keys())

    sectors = list({
        meta["sector"]
        for meta in TICKERS.values()
    })

    extras = [
        "SPY",
        "QQQ",
        "VIXY"
    ]

    return tickers + sectors + extras

# -------------------------
# SCAN PLUS POSTSCORE FILTER
# -------------------------

def scan():

    results = []

    data = get_data_batch(
        build_symbol_universe()
    )

    vix_df = data.get("VIXY")

    if vix_df is not None and not vix_df.empty:
        vix_df = compute_indicators(vix_df)

    for ticker, meta in TICKERS.items():

        try:

            sector_symbol = meta["sector"]

            df = data.get(ticker)
            sector_df = data.get(sector_symbol)

            # -------------------------
            # Validate data
            # -------------------------

            if (
                df is None or
                df.empty or
                sector_df is None or
                sector_df.empty
            ):
                continue

            # -------------------------
            # Compute indicators
            # -------------------------

            df = compute_indicators(df)
            sector_df = compute_indicators(sector_df)

            df = df.dropna()
            sector_df = sector_df.dropna()

            if df.empty or sector_df.empty:
                continue

            # -------------------------
            # Score stock
            # -------------------------

            result = score_stock(
                df=df,
                sector_df=sector_df,
                vix_df=vix_df
            )

            if result is None:
                continue

            score = result["score"]

            if score < 5:
                continue

            latest = result["latest"]

            results.append({

                "ticker": ticker,

                "sector": sector_symbol,

                "industry": meta["industry"],

                "score": score,

                "price": round(
                    latest["Close"],
                    2
                ),

                "rsi": round(
                    latest["RSI"],
                    2
                ),

                "volume": int(
                    latest["Volume"]
                ),

                "atr": round(
                    latest["ATR"],
                    2
                ),

                "relative_strength":
                    result["relative_strength"],

                "sector_trending":
                    result["sector_trending"],

                "vix":
                    result["vix"]
            })

        except Exception as e:

            print(f"Error with {ticker}: {e}")

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


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
    