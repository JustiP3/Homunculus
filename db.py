from contextlib import closing
import sqlite3


#Configuration


DB_NAME = "homunculus.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn



#Database CRUD functions:

#Strategies 
def create_strategy(name, strategy_type, description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO strategies (name, strategy_type, description)
        VALUES (?, ?, ?)
    """, (name, strategy_type, description))

    conn.commit()
    strategy_id = cursor.lastrowid
    conn.close()

    return strategy_id


def get_strategy(strategy_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM strategies
        WHERE id = ?
    """, (strategy_id,))

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None

def get_all_strategies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM strategies
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def update_strategy(
    strategy_id,
    name=None,
    strategy_type=None,
    description=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE strategies
        SET
            name = COALESCE(?, name),
            strategy_type = COALESCE(?, strategy_type),
            description = COALESCE(?, description)
        WHERE id = ?
    """, (
        name,
        strategy_type,
        description,
        strategy_id
    ))

    conn.commit()
    conn.close()


def delete_strategy(strategy_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM strategies
        WHERE id = ?
    """, (strategy_id,))

    conn.commit()
    conn.close()



#Signals 
def create_signal(strategy_id, symbol, signal_type, rsi):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO signals (
            strategy_id, symbol, signal_type, rsi
        )
        VALUES (?, ?, ?, ?)
    """, (
        strategy_id,
        symbol,
        signal_type,
        rsi,
    ))

    conn.commit()
    signal_id = cursor.lastrowid
    conn.close()

    return signal_id


def get_signal(signal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM signals
        WHERE id = ?
    """, (signal_id,))

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None
def get_all_signals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM signals
        ORDER BY signal_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_signal_status(signal_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE signals
        SET status = ?
        WHERE id = ?
    """, (
        status,
        signal_id
    ))

    conn.commit()
    conn.close()


def delete_signal(signal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM signals
        WHERE id = ?
    """, (signal_id,))

    conn.commit()
    conn.close()



#Positions
def create_position(
    signal_id,
    symbol,
    option_type,
    entry_price,
    strike_price,
    expiration_date,
    quantity,
    current_price,
    stop_loss=None,
    take_profit=None,
    status="OPEN"
):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO positions (
            signal_id, symbol, option_type, entry_price, strike, expiration,
            quantity, current_price, stop_loss, take_profit, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        signal_id,
        symbol,
        option_type,
        entry_price,
        strike_price,
        expiration_date,
        quantity,
        current_price,
        stop_loss,
        take_profit,
        status
    ))

    conn.commit()
    position_id = cursor.lastrowid
    conn.close()

    return position_id

def get_position(position_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM positions
        WHERE id = ?
    """, (position_id,))

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None

def get_all_positions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM positions
        ORDER BY opened_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_position_price(
    position_id,
    current_price
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE positions
        SET current_price = ?
        WHERE id = ?
    """, (
        current_price,
        position_id
    ))

    conn.commit()
    conn.close()


def update_position_status(
    position_id,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE positions
        SET status = ?
        WHERE id = ?
    """, (
        status,
        position_id
    ))

    conn.commit()
    conn.close()


def delete_position(position_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM positions
        WHERE id = ?
    """, (position_id,))

    conn.commit()
    conn.close()



#Position Events
def create_position_event(position_id, event_type, event_value, message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO position_events (
            position_id, event_type, event_value, notes
        )
        VALUES (?, ?, ?, ?)
    """, (
        position_id,
        event_type,
        event_value,
        message
    ))

    conn.commit()
    event_id = cursor.lastrowid
    conn.close()

    return event_id
    
def get_position_events(position_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM position_events
        WHERE position_id = ?
        ORDER BY created_at ASC
    """, (position_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def delete_position_event(event_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM position_events
        WHERE id = ?
    """, (event_id,))

    conn.commit()
    conn.close()



#Market Snapshots
def create_market_snapshot(symbol, price, rsi, vix=None, atr=None, volume=None, market_regime=None):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO market_snapshots (
            symbol, underlying_price, rsi, vix, atr, volume, market_regime
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        price,
        rsi,
        vix,
        atr,
        volume,
        market_regime
    ))

    conn.commit()
    snapshot_id = cursor.lastrowid
    conn.close()

    return snapshot_id

def get_market_snapshots(
    symbol,
    limit=50
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM market_snapshots
        WHERE symbol = ?
        ORDER BY snapshot_time DESC
        LIMIT ?
    """, (
        symbol,
        limit
    ))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def delete_market_snapshot(snapshot_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM market_snapshots
        WHERE id = ?
    """, (snapshot_id,))

    conn.commit()
    conn.close()



#Misc

def execute_query(query, params=()):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    conn.close()