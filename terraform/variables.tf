variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "aws-ml-api"
}

variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "lambda_image_uri" {
  description = "ECR image URI for the Lambda container"
  type        = string
}
