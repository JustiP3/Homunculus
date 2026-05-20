from datetime import datetime

def log_results(candidates, filename="scan_log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not candidates:
        line = f"{timestamp} | No setups found\n"
    else:
        lines = []
        for c in candidates:
            lines.append(
                f"{timestamp} | {c['ticker']} | Score:{c['score']} | Price:{c['price']} | RSI:{c['rsi']}"
            )
        line = "\n".join(lines) + "\n"

    with open(filename, "a") as f:  # "a" = append mode
        f.write(line)
