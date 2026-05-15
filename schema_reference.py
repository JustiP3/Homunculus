import sqlite3

DB_NAME = "homunculus.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# =========================
# STRATEGIES TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    strategy_type TEXT,
    description TEXT
)
""")

# =========================
# SIGNALS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id INTEGER,
    symbol TEXT NOT NULL,
    signal_type TEXT,
    signal_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    underlying_price REAL,
    rsi REAL,
    volume INTEGER,               

    ema_9 REAL,
    ema_20 REAL,

    confidence REAL,
    status TEXT DEFAULT 'NEW',

    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
)
""")

# =========================
# POSITIONS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    signal_id INTEGER,

    symbol TEXT NOT NULL,
    option_symbol TEXT,

    option_type TEXT,
    strike REAL,
    expiration DATE,

    quantity INTEGER,

    entry_price REAL,
    current_price REAL,

    stop_loss REAL,
    take_profit REAL,

    status TEXT DEFAULT 'OPEN',

    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,

    FOREIGN KEY(signal_id) REFERENCES signals(id)
)
""")

# =========================
# POSITION EVENTS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS position_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    position_id INTEGER,

    event_type TEXT,
    event_value TEXT,

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(position_id) REFERENCES positions(id)
)
""")

# =========================
# MARKET SNAPSHOTS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS market_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,

    snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    underlying_price REAL,
    rsi REAL,
    vix REAL,

    atr REAL,
    volume INTEGER,

    market_regime TEXT
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")