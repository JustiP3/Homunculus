import ta


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

def compute_features(df):

    df["RELATIVE_VOLUME"] = (
        df["Volume"] / df["Volume"].rolling(20).mean()
    )

    df["DIST_EMA20"] = df["Close"] - df["EMA20"]
    df["DIST_EMA50"] = df["Close"] - df["EMA50"]
    df["DIST_EMA200"] = df["Close"] - df["EMA200"]

    df["ATR_PCT"] = df["ATR"] / df["Close"]

    return df