
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"


def get_logs():
    if not LOG_FILE.exists():
        return []

    logs = []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" | ", 2)

            if len(parts) == 3:
                logs.append({
                    "timestamp": parts[0],
                    "level": parts[1],
                    "message": parts[2]
                })

    return logs


def get_log_stats():
    logs = get_logs()

    return {
        "total_logs": len(logs),
        "info": sum(log["level"] == "INFO" for log in logs),
        "warnings": sum(log["level"] == "WARNING" for log in logs),
        "errors": sum(log["level"] == "ERROR" for log in logs)
    }
