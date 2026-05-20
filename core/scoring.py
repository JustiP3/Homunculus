def score_stock(df, sector_df=None, vix_df=None):

    latest = df.iloc[-1]

    if len(df) < 7:
        return None

    score = 0

    # -------------------------
    # PRICE FILTER
    # -------------------------

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

    if 55 <= latest["RSI"] <= 65:
        score += 3

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

    distance_from_ema20 = (
        (latest["Close"] - latest["EMA20"])
        / latest["EMA20"]
    )

    if 0 <= distance_from_ema20 <= 0.08:
        score += 3

    elif 0.08 < distance_from_ema20 <= 0.15:
        score += 1

    # -------------------------
    # EMA20 SLOPE
    # -------------------------

    ema20_now = latest["EMA20"]
    ema20_prev = df.iloc[-5]["EMA20"]

    if ema20_now > ema20_prev:
        score += 2

    # -------------------------
    # SECTOR CONFIRMATION
    # -------------------------

    sector_trending_up = False
    relative_strength = 0

    if sector_df is not None and not sector_df.empty:

        sector_latest = sector_df.iloc[-1]

        sector_trending_up = (
            sector_latest["Close"] >
            sector_latest["EMA50"]
        )

        if sector_trending_up:
            score += 2

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

    # -------------------------
    # VIX FILTER
    # -------------------------

    vix_value = None

    if vix_df is not None and not vix_df.empty:

        vix_latest = vix_df.iloc[-1]

        vix_value = round(
            vix_latest["Close"],
            2
        )

        if vix_latest["Close"] > 30:
            score -= 3

    return {

        "score": score,

        "latest": latest,

        "relative_strength": round(
            relative_strength,
            3
        ),

        "sector_trending": sector_trending_up,

        "vix": vix_value
    }