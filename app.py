from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/positions")
def positions():

    positions = db.get_all_positions()

    return render_template(
        "positions.html",
        positions=positions
    )

@app.route("/positions/create", methods=["POST"])
def create_position():

    symbol = request.form["symbol"]
    option_type = request.form["option_type"]

    entry_price = request.form["entry_price"]
    strike_price = request.form["strike_price"]

    expiration_date = request.form["expiration_date"]

    quantity = request.form["quantity"]

    current_price = request.form["current_price"]

    stop_loss = request.form.get("stop_loss") or None
    take_profit = request.form.get("take_profit") or None

    db.create_position(
        symbol,
        option_type,
        entry_price,
        strike_price,
        expiration_date,
        quantity,
        current_price,
        stop_loss,
        take_profit
    )

    return redirect("/positions")


@app.route("/signals")
def signals():

    signals = db.get_all_signals()

    return render_template(
        "signals.html",
        signals=signals
    )

@app.route("/signals/create", methods=["POST"])
def create_signal():

    strategy_id = request.form["strategy_id"]
    symbol = request.form["symbol"]
    signal_type = request.form["signal_type"]
    rsi = request.form["rsi"]

    db.create_signal(
        strategy_id,
        symbol,
        signal_type,
        rsi
    )

    return redirect("/signals")

@app.route("/market-snapshots")
def market_snapshots():

    snapshots = db.get_all_market_snapshots()

    return render_template(
        "market_snapshots.html",
        snapshots=snapshots
    )

@app.route("/market-snapshots/create", methods=["POST"])
def create_market_snapshot():

    symbol = request.form["symbol"]
    price = request.form["price"]
    rsi = request.form["rsi"]

    vix = request.form.get("vix") or None
    atr = request.form.get("atr") or None
    volume = request.form.get("volume") or None
    market_regime = request.form.get("market_regime") or None

    db.create_market_snapshot(
        symbol,
        price,
        rsi,
        vix,
        atr,
        volume,
        market_regime
    )

    return redirect("/market-snapshots")

@app.route("/position-events")
def position_events():

    events = db.get_all_position_events()

    return render_template(
        "position_events.html",
        events=events
    )

@app.route("/position-events/create", methods=["POST"])
def create_position_event():

    position_id = request.form["position_id"]
    event_type = request.form["event_type"]
    event_value = request.form["event_value"]
    message = request.form["message"]

    db.create_position_event(
        position_id,
        event_type,
        event_value,
        message
    )

    return redirect("/position-events")

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )