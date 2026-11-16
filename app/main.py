from app.database import get_monitoring_stats
from datetime import datetime, timezone
from fastapi import FastAPI, Request
import logging
import time
from pathlib import Path

from app.analyzer import get_logs, get_log_stats
from app.database import (
    initialize_database,
    save_monitoring_log,
    get_monitoring_logs
)

# Create logs directory
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "app.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SmartOps")

# Create FastAPI application
app = FastAPI(
    title="SmartOps",
    description="AI-Powered Application Monitoring System",
    version="1.0.0"
)

# Initialize database when application starts
@app.on_event("startup")
def startup():
    initialize_database()


# Monitor every HTTP request
@app.middleware("http")
async def monitor_requests(request: Request, call_next):

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        timestamp = datetime.now(timezone.utc).isoformat()

        logger.info(
            "method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        # Save request details into SQLite
        save_monitoring_log(
            timestamp,
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response

    except Exception:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path
        )
        raise


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartOps!",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SmartOps API"
    }


@app.get("/demo/warning")
def demo_warning():
    logger.warning("This is a simulated warning!")
    return {"message": "Warning generated successfully"}


@app.get("/demo/error")
def demo_error():
    logger.error("This is a simulated application error!")
    return {"message": "Error log generated successfully"}


@app.get("/logs")
def view_logs():
    return get_logs()


@app.get("/logs/stats")
def log_statistics():
    return get_log_stats()


# View monitoring records from SQLite
@app.get("/monitoring/history")
def monitoring_history():
    return get_monitoring_logs()


@app.get("/monitoring/stats")
def monitoring_statistics():
    return get_monitoring_stats()
