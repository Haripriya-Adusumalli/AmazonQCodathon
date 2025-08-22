# Note: Bedrock Agents are not yet fully supported in Terraform AWS Provider
# This file shows the intended configuration structure
# Use the CloudFormation template or AWS CLI/SDK for actual deployment

# Weather Agent (Placeholder - use CloudFormation or AWS CLI)
# resource "aws_bedrock_agent" "weather" {
#   agent_name               = "${var.project_name}-${var.environment}-weather-agent"
#   agent_resource_role_arn  = aws_iam_role.bedrock_agent.arn
#   foundation_model         = "anthropic.claude-3-haiku-20240307-v1:0"
#   instruction              = "You are a helpful weather assistant..."
# }

# Product Opportunity Agent (Placeholder - use CloudFormation or AWS CLI)
# resource "aws_bedrock_agent" "product_opportunity" {
#   agent_name               = "${var.project_name}-${var.environment}-product-opportunity-agent"
#   agent_resource_role_arn  = aws_iam_role.bedrock_agent.arn
#   foundation_model         = "anthropic.claude-3-haiku-20240307-v1:0"
#   instruction              = "You are a Product Opportunity Analyzer..."
# }

# For now, use null_resource to run deployment scripts
resource "null_resource" "deploy_bedrock_agents" {
  depends_on = [
    aws_lambda_function.weather,
    aws_lambda_function.market_demand,
    aws_lambda_function.competitor_scan,
    aws_lambda_function.capability_match
  ]

  provisioner "local-exec" {
    command = "echo 'Deploy Bedrock Agents using CloudFormation or Python scripts'"
  }

  triggers = {
    lambda_functions = join(",", [
      aws_lambda_function.weather.arn,
      aws_lambda_function.market_demand.arn,
      aws_lambda_function.competitor_scan.arn,
      aws_lambda_function.capability_match.arn
    ])
  }
}