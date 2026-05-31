# CRUD functions for historical data



import sqlite3
from typing import Optional


DB_PATH = "../homunculus.db"


# =====================================================
# CONNECTION HELPERS
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =====================================================
# HISTORICAL_RUNS
# =====================================================

def create_historical_run(
    name: str,
    description: Optional[str] = None,
    strategy_version: Optional[str] = None,
    universe: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO historical_runs (
            name,
            description,
            strategy_version,
            universe,
            start_date,
            end_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        description,
        strategy_version,
        universe,
        start_date,
        end_date
    ))

    conn.commit()

    run_id = cur.lastrowid

    conn.close()

    return run_id


def get_historical_run(run_id):
    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM historical_runs
        WHERE id = ?
    """, (run_id,)).fetchone()

    conn.close()

    return dict(row) if row else None


# =====================================================
# HISTORICAL_BARS
# =====================================================

def insert_historical_bar(
    symbol,
    timestamp,
    open_price,
    high,
    low,
    close,
    volume,
    vwap=None,
    trade_count=None,
    timeframe="1Day"
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO historical_bars (
            symbol,
            timestamp,
            open,
            high,
            low,
            close,
            volume,
            vwap,
            trade_count,
            timeframe
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        timestamp,
        open_price,
        high,
        low,
        close,
        volume,
        vwap,
        trade_count,
        timeframe
    ))

    conn.commit()
    conn.close()


def get_historical_bars(
    symbol,
    start_time=None,
    end_time=None
):
    conn = get_connection()

    sql = """
        SELECT *
        FROM historical_bars
        WHERE symbol = ?
    """

    params = [symbol]

    if start_time:
        sql += " AND timestamp >= ?"
        params.append(start_time)

    if end_time:
        sql += " AND timestamp <= ?"
        params.append(end_time)

    sql += " ORDER BY timestamp"

    rows = conn.execute(sql, params).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =====================================================
# HISTORICAL_SNAPSHOT
# =====================================================

def insert_historical_snapshot(
    run_id,
    symbol,
    snapshot_time,
    **kwargs
):
    conn = get_connection()

    columns = [
        "run_id",
        "symbol",
        "snapshot_time"
    ]

    values = [
        run_id,
        symbol,
        snapshot_time
    ]

    for k, v in kwargs.items():
        columns.append(k)
        values.append(v)

    placeholders = ",".join(["?"] * len(values))

    conn.execute(
        f"""
        INSERT INTO historical_snapshot
        ({",".join(columns)})
        VALUES ({placeholders})
        """,
        values
    )

    conn.commit()
    conn.close()


# =====================================================
# HISTORICAL_SCORES
# =====================================================

def insert_historical_score(
    run_id,
    symbol,
    snapshot_time,
    trend_score,
    entry_score,
    strategy_version=None,
    scan_id=None
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO historical_scores (
            run_id,
            symbol,
            snapshot_time,
            trend_score,
            entry_score,
            strategy_version,
            scan_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        symbol,
        snapshot_time,
        trend_score,
        entry_score,
        strategy_version,
        scan_id
    ))

    conn.commit()
    conn.close()


def get_scores_for_run(run_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM historical_scores
        WHERE run_id = ?
        ORDER BY snapshot_time
    """, (run_id,)).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =====================================================
# HISTORICAL_OUTCOMES
# =====================================================

def insert_historical_outcome(
    run_id,
    symbol,
    snapshot_time,
    close_price,
    return_1d=None,
    return_3d=None,
    return_5d=None,
    return_10d=None,
    return_20d=None,
    max_gain_5d=None,
    max_loss_5d=None,
    max_gain_10d=None,
    max_loss_10d=None,
    max_gain_20d=None,
    max_loss_20d=None
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO historical_outcomes (
            run_id,
            symbol,
            snapshot_time,
            close_price,

            return_1d,
            return_3d,
            return_5d,
            return_10d,
            return_20d,

            max_gain_5d,
            max_loss_5d,

            max_gain_10d,
            max_loss_10d,

            max_gain_20d,
            max_loss_20d
        )
        VALUES (
            ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?, ?
        )
    """, (
        run_id,
        symbol,
        snapshot_time,
        close_price,

        return_1d,
        return_3d,
        return_5d,
        return_10d,
        return_20d,

        max_gain_5d,
        max_loss_5d,

        max_gain_10d,
        max_loss_10d,

        max_gain_20d,
        max_loss_20d
    ))

    conn.commit()
    conn.close()


# =====================================================
# GENERIC HELPERS
# =====================================================

def delete_run(run_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM historical_runs
        WHERE id = ?
    """, (run_id,))

    conn.commit()
    conn.close()


def execute_query(sql, params=None):
    conn = get_connection()

    rows = conn.execute(sql, params or []).fetchall()

    conn.close()

    return [dict(r) for r in rows]