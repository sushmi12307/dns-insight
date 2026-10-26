
from flask import Flask, request, jsonify
from pathlib import Path

from dns_service import lookup
from cache_manager import get_cache_stats, clear_cache
from trace_service import get_trace
from diagnostics import explain_status
from history_manager import (
    initialize_database,
    save_query,
    get_history
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Flask application
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)


# Create the SQLite database and history table
initialize_database()


# Home page
@app.get("/")
def home():
    return app.send_static_file("index.html")


# Check whether the backend is running
@app.get("/api/health")
def health():
    return jsonify({
        "status": "running",
        "project": "DNS Insight"
    })


# Perform a DNS lookup
@app.get("/api/lookup")
def dns_lookup():
    domain = request.args.get("domain", "").strip()
    record_type = request.args.get("type", "A").upper()

    try:
        result = lookup(domain, record_type)

        # Add a diagnostic explanation
        result["diagnosis"] = explain_status(
            result.get("status", "unknown")
        )

        # Save the query and its result in SQLite
        save_query(result)

        return jsonify(result)

    except ValueError as error:
        return jsonify({
            "status": "invalid_input",
            "message": str(error)
        }), 400

    except Exception as error:
        app.logger.exception("DNS lookup failed")

        return jsonify({
            "status": "server_error",
            "message": "An unexpected server error occurred."
        }), 500


# Simulated DNS resolution trace
@app.get("/api/trace")
def dns_trace():
    domain = request.args.get("domain", "").strip()

    if (
        not domain
        or len(domain) > 253
        or any(char.isspace() for char in domain)
    ):
        return jsonify({
            "error": "Please enter a valid domain name."
        }), 400

    return jsonify({
        "domain": domain,
        "stages": get_trace(domain)
    })


# Cache statistics
@app.get("/api/stats")
def stats():
    return jsonify(get_cache_stats())


# Clear the application DNS cache
@app.post("/api/cache/clear")
def cache_clear():
    return jsonify(clear_cache())


# Retrieve saved DNS query history
@app.get("/api/history")
def history():
    return jsonify({
        "count": len(get_history()),
        "history": get_history()
    })


# Run the Flask development server
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
