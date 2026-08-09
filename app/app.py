from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import logging
import os

app = Flask(__name__)

# Automatically expose /metrics
metrics = PrometheusMetrics(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


@app.route("/")
def home():
    logger.info("GET /")

    return jsonify({
        "application": "Enterprise Monitoring Platform",
        "environment": os.getenv("APP_ENV", "Development"),
        "version": "2.0.0",
        "status": "Running Successfully"
    })


@app.route("/health")
def health():
    logger.info("GET /health")

    return jsonify({
        "status": "healthy"
    })


@app.route("/version")
def version():
    logger.info("GET /version")

    return jsonify({
        "version": "2.0.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)