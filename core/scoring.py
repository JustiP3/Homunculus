
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
