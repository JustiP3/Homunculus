from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/positions")
def positions():

    positions = db.get_open_positions()

    return render_template(
        "positions.html",
        positions=positions
    )


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

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )