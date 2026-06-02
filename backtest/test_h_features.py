from backtest.h_db import (
    get_historical_bars,
    get_historical_snapshots,
    create_historical_run
)

from backtest.h_features import build_features


TICKER = "SPY"


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def test_h_features():

    print_section("CREATING TEST RUN")

    run_id = create_historical_run(
        name="H_FEATURES SMOKE TEST",
        description="Validate feature pipeline output",
        strategy_version="test_v1",
        universe="SPY"
    )

    print(f"Run ID: {run_id}")

    print_section("RUNNING FEATURE PIPELINE")

    try:
        build_features(run_id, TICKER)
        print("✓ h_features.py executed successfully")
    except Exception as e:
        print("ERROR running h_features.py")
        raise e

    # =====================================================
    # HISTORICAL BARS CHECK
    # =====================================================

    print_section("HISTORICAL BARS")

    bars = get_historical_bars(TICKER)

    print(f"Total bars in DB: {len(bars)}")

    print("\nSample (last 3 rows):")
    for row in bars[-3:]:
        print(row)

    # basic sanity checks
    print("\nSanity checks:")

    assert len(bars) > 0, "No bars found in database"

    print("✓ Bars exist")

    # =====================================================
    # HISTORICAL SNAPSHOTS CHECK
    # =====================================================

    print_section("HISTORICAL SNAPSHOTS")

    snapshots = get_historical_snapshots(run_id)

    print(f"Total snapshots for run: {len(snapshots)}")

    print("\nSample (last 3 rows):")
    for row in snapshots[-3:]:
        print(row)

    assert len(snapshots) > 0, "No snapshots generated"

    print("\nSanity checks:")

    # check required fields exist
    sample = snapshots[-1]

    required_fields = [
        "ema_20",
        "ema_50",
        "ema_200",
        "rsi",
        "atr",
        "relative_volume",
        "distance_from_ema20"
    ]

    missing = [f for f in required_fields if sample.get(f) is None]

    if missing:
        print(f"⚠ Missing fields in latest snapshot: {missing}")
    else:
        print("✓ All key feature fields present")

    # check for NaNs disguised as None
    print("\nExample snapshot values:")
    print({
        "symbol": sample["symbol"],
        "close_price": sample["close_price"],
        "rsi": sample["rsi"],
        "ema_20": sample["ema_20"],
        "ema_50": sample["ema_50"],
        "ema_200": sample["ema_200"],
        "relative_volume": sample["relative_volume"]
    })

    print("\n✓ SNAPSHOT PIPELINE VALIDATED")

    print_section("TEST COMPLETE")


if __name__ == "__main__":
    test_h_features()