output "user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.main.id
}

output "user_pool_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.main.id
}

output "identity_pool_id" {
  description = "Cognito Identity Pool ID"
  value       = aws_cognito_identity_pool.main.id
}

output "weather_function_arn" {
  description = "Weather Lambda Function ARN"
  value       = aws_lambda_function.weather.arn
}

output "market_demand_function_arn" {
  description = "Market Demand Lambda Function ARN"
  value       = aws_lambda_function.market_demand.arn
}

output "competitor_scan_function_arn" {
  description = "Competitor Scan Lambda Function ARN"
  value       = aws_lambda_function.competitor_scan.arn
}

output "capability_match_function_arn" {
  description = "Capability Match Lambda Function ARN"
  value       = aws_lambda_function.capability_match.arn
}

output "bedrock_agent_role_arn" {
  description = "Bedrock Agent Role ARN"
  value       = aws_iam_role.bedrock_agent.arn
}

output "aws_config_js" {
  description = "AWS configuration for React app"
  value = <<-EOT
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: '${aws_cognito_user_pool.main.id}',
      userPoolClientId: '${aws_cognito_user_pool_client.main.id}',
      region: '${var.aws_region}',
      identityPoolId: '${aws_cognito_identity_pool.main.id}'
    }
  }
};
EOT
}