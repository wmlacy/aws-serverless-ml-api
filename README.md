# AWS ML Prediction API

## What it does
Serverless churn-probability prediction API on AWS Lambda behind API Gateway. Input features: monthly_spend, tenure_months, num_support_tickets.

## Architecture
- Dockerized Lambda (Python 3.11, scikit-learn)
- API Gateway HTTP API (POST /predict)
- Terraform for IaC
- ECR for image storage

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
This project was built to demonstrate practical cloud engineering skills:
deploying a machine learning model as a production-style, serverless API on AWS.
The emphasis is on infrastructure, automation, and clean deployment rather than
model complexity.
