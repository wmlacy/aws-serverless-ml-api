# Serverless AWS API (Lambda, API Gateway, Terraform)

## What it does
Serverless API deployed on AWS using Lambda and API Gateway, demonstrating production-style cloud architecture and Infrastructure as Code practices.

The example payload is a churn-probability prediction (input: `monthly_spend`, `tenure_months`, `num_support_tickets`), but the infrastructure patterns apply to any containerized workload.

## Architecture
- Dockerized Lambda (Python 3.11, scikit-learn)
- API Gateway HTTP API
- Terraform for IaC
- ECR for image storage

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check, returns `{"status": "ok"}` |
| POST | /predict | Churn prediction with input validation |

### Request validation
The `/predict` endpoint validates:
- Required fields: `monthly_spend`, `tenure_months`, `num_support_tickets`
- Numeric types
- Non-negative values
- Reasonable ranges

Invalid requests return `400` with a clear error message.

## Quickstart
```bash
make deploy
# After apply, Terraform prints the base URL. Use:
curl -X POST "$INVOKE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"monthly_spend":70,"tenure_months":9,"num_support_tickets":1}'
```

## Cost
- ECR storage: pennies
- Lambda invocations: free tier covers thousands
- API Gateway HTTP API: ~$1–2 per million requests

## Troubleshooting
- **Module not found on Lambda**: Use the provided Dockerfile with Lambda base image
- **AccessDenied from API Gateway**: Re-run `terraform apply`
- **Cold starts slow**: Keep memory at 512–1024 MB
- **Different region**: Update `REGION` in Makefile and Terraform vars

## Why this project
This project serves as a reference implementatation for building and deploying cloud-native APIs on AWS using serverless architecture and Infrastructure as Code.

The emphasis is on repeatable deployment, clean system boundaries, and operational simplicity rather than application-level complexity.
