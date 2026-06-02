from h_db import (
    create_historical_run,
    get_historical_run,
    insert_historical_bar,
    get_historical_bars,
    insert_historical_snapshot,
    get_historical_snapshots,
    insert_historical_score,
    get_scores_for_run,
    insert_historical_outcome,
    get_historical_outcomes
)


def test_historical_db():

    print("\n=== TESTING HISTORICAL DATABASE ===\n")

    # ==================================================
    # Create Historical Run
    # ==================================================

    run_id = create_historical_run(
        name="Unit Test Run",
        description="Testing CRUD functions",
        strategy_version="v1.0",
        universe="SPY",
        start_date="2024-01-01",
        end_date="2024-12-31"
    )

    print(f"Created historical run: {run_id}")

    run = get_historical_run(run_id)

    assert run is not None
    assert run["id"] == run_id

    print("✓ historical_runs insert/read successful")

    # ==================================================
    # Insert Historical Bar
    # ==================================================

    insert_historical_bar(
        symbol="SPY",
        timestamp="2024-01-02 09:30:00",
        open_price=470.0,
        high=472.5,
        low=469.0,
        close=471.0,
        volume=1000000,
        vwap=470.8,
        trade_count=15000,
        timeframe="1Day"
    )

    bars = get_historical_bars("SPY")

    assert len(bars) > 0

    print("✓ historical_bars insert/read successful")

    # ==================================================
    # Insert Historical Snapshot
    # ==================================================

    insert_historical_snapshot(
        run_id=run_id,
        symbol="SPY",
        snapshot_time="2024-01-02 09:30:00",

        close_price=471.0,

        rsi=62.4,
        atr=4.5,

        ema_9=469.8,
        ema_20=465.2,
        ema_50=455.3,
        ema_200=430.1,

        relative_volume=1.8,

        distance_from_ema20=1.25,
        distance_from_ema50=3.45,
        distance_from_ema200=9.53,

        vix=13.5,

        market_regime="Bullish",
        sector="ETF",

        scan_id="TEST_SCAN"
    )

    snapshots = get_historical_snapshots(run_id)

    assert len(snapshots) > 0

    print("✓ historical_snapshot insert/read successful")

    # ==================================================
    # Insert Historical Score
    # ==================================================

    insert_historical_score(
        run_id=run_id,
        symbol="SPY",
        snapshot_time="2024-01-02 09:30:00",
        trend_score=88,
        entry_score=92,
        strategy_version="v1.0",
        scan_id="TEST_SCAN"
    )

    scores = get_scores_for_run(run_id)

    assert len(scores) > 0

    print("✓ historical_scores insert/read successful")

    # ==================================================
    # Insert Historical Outcome
    # ==================================================

    insert_historical_outcome(
        run_id=run_id,
        symbol="SPY",
        snapshot_time="2024-01-02 09:30:00",
        close_price=471.0,

        return_1d=0.5,
        return_3d=1.2,
        return_5d=2.1,
        return_10d=3.8,
        return_20d=5.4,

        max_gain_5d=3.2,
        max_loss_5d=-0.8,

        max_gain_10d=5.1,
        max_loss_10d=-1.1,

        max_gain_20d=8.5,
        max_loss_20d=-2.0
    )

    outcomes = get_historical_outcomes(run_id)

    assert len(outcomes) > 0

    print("✓ historical_outcomes insert/read successful")

    # ==================================================
    # Display Sample Records
    # ==================================================

    print("\n=== SAMPLE DATA ===\n")

    print("RUN:")
    print(run)

    print("\nBAR:")
    print(bars[-1])

    print("\nSNAPSHOT:")
    print(snapshots[-1])

    print("\nSCORE:")
    print(scores[-1])

    print("\nOUTCOME:")
    print(outcomes[-1])

    print("\n=== ALL TESTS PASSED ===\n")


if __name__ == "__main__":
    test_historical_db()