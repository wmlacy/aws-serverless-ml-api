# app/handler.py
import json
import pickle
import numpy as np
import os

# Load once on cold start
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(MODEL_PATH, "rb") as f:
    MODEL = pickle.load(f)

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif body is None and "queryStringParameters" in event:
            # Allow quick GET tests
            body = event["queryStringParameters"] or {}

        features = [
            float(body.get("monthly_spend", 50)),
            float(body.get("tenure_months", 6)),
            float(body.get("num_support_tickets", 2)),
        ]
        X = np.array(features, dtype=float).reshape(1, -1)
        prob = float(MODEL.predict_proba(X)[0,1])

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"churn_probability": round(prob, 4)})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
