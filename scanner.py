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

    # One large batch request
    data = get_data_batch(build_symbol_universe())

    # Market context
    vix_df = data.get("VIXY")
    spy_df = data.get("SPY")
    qqq_df = data.get("QQQ")

    if vix_df is not None and not vix_df.empty:
        vix_df = compute_indicators(vix_df)

    if spy_df is not None and not spy_df.empty:
        spy_df = compute_indicators(spy_df)

    if qqq_df is not None and not qqq_df.empty:
        qqq_df = compute_indicators(qqq_df)

    # ----------------------------
    # Scan individual tickers
    # ----------------------------

    for ticker, meta in TICKERS.items():

        try:

            sector_symbol = meta["sector"]

            df = data.get(ticker)
            sector_df = data.get(sector_symbol)

            # ----------------------------
            # Validate stock data
            # ----------------------------

            if df is None or df.empty:
                continue

            

            if df.empty:
                continue

            # ----------------------------
            # Validate sector ETF data
            # ----------------------------

            if sector_df is None or sector_df.empty:
                continue

            

            if sector_df.empty:
                continue

            # ----------------------------
            # Compute indicators
            # ----------------------------

            df = compute_indicators(df)
            sector_df = compute_indicators(sector_df)

            df = df.dropna()
            sector_df = sector_df.dropna()

            if df.empty or sector_df.empty:
                continue

            latest = df.iloc[-1]
            sector_latest = sector_df.iloc[-1]

            # ----------------------------
            # Base stock score
            # ----------------------------

            score, latest = score_stock(df)

            # ----------------------------
            # Sector confirmation
            # ----------------------------

            sector_trending_up = (
                sector_latest["Close"] >
                sector_latest["EMA50"]
            )

            if sector_trending_up:
                score += 2

            # ----------------------------
            # Relative strength
            # ----------------------------

            stock_strength = (
                latest["Close"] /
                latest["EMA20"]
            )

            sector_strength = (
                sector_latest["Close"] /
                sector_latest["EMA20"]
            )

            relative_strength = (
                stock_strength -
                sector_strength
            )

            if relative_strength > 0:
                score += 2

            # ----------------------------
            # Volatility filter
            # ----------------------------

            vix_value = None

            if vix_df is not None and not vix_df.empty:

                vix_latest = vix_df.iloc[-1]

                vix_value = round(
                    vix_latest["Close"],
                    2
                )

                # Penalize extreme volatility
                if vix_latest["Close"] > 30:
                    score -= 3

            # ----------------------------
            # Final candidate filter
            # ----------------------------

            if score >= 5:

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

                    "relative_strength": round(
                        relative_strength,
                        3
                    ),

                    "sector_trending": sector_trending_up,

                    "vix": vix_value
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
    