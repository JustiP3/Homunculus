# Homunculus

Homunculus is a lightweight Python-based trading assistant designed for automated stock and options scanning, Discord-based trade management, and strategy experimentation.


---

# Features

- Automated stock scanner
- Discord bot command interface
- Discord webhook alerts
- SQLite trade database
- Position tracking
- Signal logging
- Watchlist management
- Scheduled scans and monitoring
- Modular architecture for future strategy expansion

---

# Architecture Overview

```text
Discord
    ↓
Discord Bot (discord.py)
    ├── Command Interface
    ├── Scheduled Tasks
    ├── Alert Routing
    └── Trade Management

Trading Engine
    ├── scanner.py
    ├── exit_engine.py
    ├── trade_manager.py
    └── alerts.py

Persistence Layer
    ├── db.py
    └── SQLite Database

External Services
    ├── Discord Webhooks
    └── Market Data APIs
```

---

# Core Components

## Discord Bot

The Discord bot acts as:
- the user interface
- the scheduler
- the command processor
- the remote control for the system

Example commands:

```text
!scan
!enter
!close
!positions
!watchlist
!signals
```

---

## Scanner Engine

`scanner.py` performs periodic market scans against a predefined ticker universe.

The scanner:
- calculates technical indicators
- scores trade setups
- generates candidate signals
- sends Discord alerts
- stores signals in the database

Example indicators:
- RSI
- EMA crossovers
- volume analysis
- momentum scoring

---

## Trade Manager

`trade_manager.py` manages:
- entering positions
- closing positions
- updating trade state
- coordinating database writes

This layer separates trading logic from Discord bot logic.

---

## Database Layer

SQLite is used for persistence.

Primary tables include:

| Table | Purpose |
|---|---|
| strategies | Strategy definitions |
| signals | Scanner-generated opportunities |
| positions | Active and historical trades |
| position_events | Timeline/history of trade activity |
| market_snapshots | Historical indicator snapshots |
| watchlist | High-priority monitored tickers |

---

# Signal Lifecycle

```text
Scanner
    ↓
Signals Table
    ↓
Human Evaluation
    ↓
Discord Command (!enter)
    ↓
Positions Table
    ↓
Exit Monitoring
    ↓
Position Events
```

---

# Scheduling

Scheduled tasks are handled directly through the Discord bot using:

- `discord.ext.tasks`

Examples:
- daily scans
- periodic watchlist monitoring
- exit condition checks
- PnL updates

---

# Security

Sensitive values are stored in `.env`:

```env
DISCORD_BOT_TOKEN=
DISCORD_WEBHOOK_URL=
ALPACA_API_KEY=
ALPACA_SECRET_KEY=
```

`.env` is excluded from version control via `.gitignore`.

---

# Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Bot Framework | discord.py |
| Database | SQLite |
| Environment | Linux |
| Scheduling | discord.ext.tasks |
| Market Data | Alpaca API |
| Alerts | Discord Webhooks |

---

# Project Goals

Homunculus is designed as:
- a research platform
- a strategy experimentation environment
- a lightweight portfolio management tool
- an automation framework for discretionary trading

The architecture prioritizes:
- simplicity
- modularity
- local deployment
- low infrastructure overhead
- extensibility

---

# Future Development

Planned features include:
- automated exit engine
- PnL analytics
- fills/executions tracking
- advanced watchlist logic
- web dashboard
- strategy backtesting
- multi-strategy support
- broker integration
- containerized deployment

---

# Disclaimer

This project is experimental software intended for educational and research purposes only.

No financial advice is provided.


