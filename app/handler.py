# app/handler.py
import json
import pickle
import numpy as np
import os
import time

# Load once on cold start
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(MODEL_PATH, "rb") as f:
    MODEL = pickle.load(f)

REQUIRED_FIELDS = ["monthly_spend", "tenure_months", "num_support_tickets"]


def log_request(request_id, route, input_data, output_data, latency_ms, status):
    """Structured logging for CloudWatch."""
    print(json.dumps({
        "request_id": request_id,
        "route": route,
        "input": input_data,
        "output": output_data,
        "latency_ms": round(latency_ms, 2),
        "status": status
    }))


def validate_input(body):
    """Validate request body. Returns (is_valid, error_message)."""
    if body is None:
        return False, "Request body is required"

    # Check required fields
    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    # Check numeric types and ranges
    for field in REQUIRED_FIELDS:
        value = body.get(field)
        try:
            num = float(value)
        except (TypeError, ValueError):
            return False, f"Field '{field}' must be numeric, got: {type(value).__name__}"

        if num < 0:
            return False, f"Field '{field}' cannot be negative, got: {num}"

    # Sanity checks
    if float(body["tenure_months"]) > 600:  # 50 years
        return False, "tenure_months seems unreasonably high (max 600)"
    if float(body["monthly_spend"]) > 100000:
        return False, "monthly_spend seems unreasonably high (max 100000)"
    if float(body["num_support_tickets"]) > 1000:
        return False, "num_support_tickets seems unreasonably high (max 1000)"

    return True, None


def handle_health():
    """Handle GET /health."""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "ok"})
    }


def handle_predict(event, request_id):
    """Handle POST /predict."""
    start = time.time()

    # Parse body
    body = event.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            log_request(request_id, "/predict", None, {"error": str(e)}, 0, 400)
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"Invalid JSON: {e}"})
            }

    # Validate input
    is_valid, error_msg = validate_input(body)
    if not is_valid:
        latency = (time.time() - start) * 1000
        log_request(request_id, "/predict", body, {"error": error_msg}, latency, 400)
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": error_msg})
        }

    # Make prediction
    features = [
        float(body["monthly_spend"]),
        float(body["tenure_months"]),
        float(body["num_support_tickets"]),
    ]
    X = np.array(features, dtype=float).reshape(1, -1)
    prob = float(MODEL.predict_proba(X)[0, 1])
    result = {"churn_probability": round(prob, 4)}

    latency = (time.time() - start) * 1000
    log_request(request_id, "/predict", body, result, latency, 200)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }


def lambda_handler(event, context):
    request_id = context.aws_request_id if context else "local"

    # Route based on path
    raw_path = event.get("rawPath", event.get("path", "/"))
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if raw_path == "/health" and method == "GET":
        return handle_health()
    elif raw_path == "/predict" and method == "POST":
        return handle_predict(event, request_id)
    else:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Not found: {method} {raw_path}"})
        }
