from flask import Flask, render_template
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


@app.route("/watchlist")
def watchlist():

    symbols = db.get_watchlist()

    return render_template(
        "watchlist.html",
        symbols=symbols
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )