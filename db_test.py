import db


def print_section(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


# =========================================================
# STRATEGIES
# =========================================================

print_section("TESTING STRATEGIES")

db.create_strategy(name="RSI Oversold Calls", strategy_type="LONG_CALL", description="Buy calls on oversold RSI")

strategies = db.get_all_strategies()
print("All Strategies:")
print(strategies)

strategy_id = strategies[-1]["id"]

strategy = db.get_strategy(strategy_id)
print("Single Strategy:")
print(strategy)

db.update_strategy(
    strategy_id,
    description="Updated description"
)

updated_strategy = db.get_strategy(strategy_id)
print("Updated Strategy:")
print(updated_strategy)

db.delete_strategy(strategy_id)

print("Strategies After Delete:")
print(db.get_all_strategies())


# =========================================================
# SIGNALS
# =========================================================

print_section("TESTING SIGNALS")

db.create_signal(
    strategy_id=1,
    symbol="AAPL",
    signal_type="BUY",
    rsi=28.5,
)

signals = db.get_all_signals()
print("All Signals:")
print(signals)

signal_id = signals[-1]["id"]

signal = db.get_signal(signal_id)
print("Single Signal:")
print(signal)

db.update_signal_status(signal_id, "EXECUTED")

updated_signal = db.get_signal(signal_id)
print("Updated Signal:")
print(updated_signal)

db.delete_signal(signal_id)

print("Signals After Delete:")
print(db.get_all_signals())


# =========================================================
# POSITIONS
# =========================================================

print_section("TESTING POSITIONS")

db.create_position(
    signal_id=1,
    symbol="NVDA",
    option_type="CALL",
    strike_price=180,
    expiration_date="2026-09-18",
    entry_price=5.25,
    quantity=2,
    current_price=5.25,
    status="OPEN"
)

positions = db.get_all_positions()

print("All Positions:")
print(positions)

position_id = positions[-1]["id"]

position = db.get_position(position_id)
print("Single Position:")
print(position)

db.update_position_price(
    position_id,
    6.80
)

db.update_position_status(
    position_id,
    "CLOSED"
)

updated_position = db.get_position(position_id)

print("Updated Position:")
print(updated_position)

db.delete_position(position_id)

print("Positions After Delete:")
print(db.get_all_positions())


# =========================================================
# POSITION EVENTS
# =========================================================

print_section("TESTING POSITION EVENTS")

db.create_position_event(
    position_id=1,
    event_type="EXIT_ALERT",
    event_value=70,
    message="RSI crossed above 70"
)

events = db.get_position_events(1)

print("Position Events:")
print(events)

if events:
    event_id = events[-1]["id"]

    db.delete_position_event(event_id)

    print("Events After Delete:")
    print(db.get_position_events(1))


# =========================================================
# MARKET SNAPSHOTS
# =========================================================

print_section("TESTING MARKET SNAPSHOTS")

db.create_market_snapshot(
    symbol="SPY",
    price=620.55,
    rsi=72.4,
    volume=1000000
)

snapshots = db.get_market_snapshots("SPY")

print("Market Snapshots:")
print(snapshots)

if snapshots:
    snapshot_id = snapshots[0]["id"]

    db.delete_market_snapshot(snapshot_id)

    print("Snapshots After Delete:")
    print(db.get_market_snapshots("SPY"))


print_section("ALL DB TESTS COMPLETE")