output "predict_endpoint" {
  value = "${aws_apigatewayv2_api.http.api_endpoint}/predict"
}

output "health_endpoint" {
  value = "${aws_apigatewayv2_api.http.api_endpoint}/health"
}
