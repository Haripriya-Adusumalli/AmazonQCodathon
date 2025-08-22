terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "product-opportunity-system"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "weather_api_key" {
  description = "OpenWeatherMap API Key"
  type        = string
  sensitive   = true
}

# Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.project_name}-${var.environment}-users"

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_uppercase = true
    require_lowercase = true
    require_numbers   = true
    require_symbols   = false
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-user-pool"
    Environment = var.environment
  }
}

resource "aws_cognito_user_pool_client" "main" {
  name         = "${var.project_name}-${var.environment}-client"
  user_pool_id = aws_cognito_user_pool.main.id

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
}

resource "aws_cognito_identity_pool" "main" {
  identity_pool_name               = "${var.project_name}-${var.environment}-identity"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    client_id     = aws_cognito_user_pool_client.main.id
    provider_name = aws_cognito_user_pool.main.endpoint
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-identity-pool"
    Environment = var.environment
  }
}

# IAM Role for Cognito Authenticated Users
resource "aws_iam_role" "cognito_authenticated" {
  name = "${var.project_name}-${var.environment}-cognito-authenticated"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.main.id
          }
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr" = "authenticated"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "cognito_authenticated_bedrock" {
  name = "BedrockAccess"
  role = aws_iam_role.cognito_authenticated.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeAgent",
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_cognito_identity_pool_roles_attachment" "main" {
  identity_pool_id = aws_cognito_identity_pool.main.id

  roles = {
    "authenticated" = aws_iam_role.cognito_authenticated.arn
  }
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_execution" {
  name = "${var.project_name}-${var.environment}-lambda-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_execution.name
}

resource "aws_iam_role_policy" "lambda_bedrock" {
  name = "BedrockAccess"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:ListFoundationModels"
        ]
        Resource = "*"
      }
    ]
  })
}

# Bedrock Agent Role
resource "aws_iam_role" "bedrock_agent" {
  name = "${var.project_name}-${var.environment}-bedrock-agent"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "bedrock_agent_policy" {
  name = "BedrockAgentPolicy"
  role = aws_iam_role.bedrock_agent.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "lambda:InvokeFunction"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda Functions
resource "aws_lambda_function" "weather" {
  filename         = "weather_function.zip"
  function_name    = "${var.project_name}-${var.environment}-weather"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "index.lambda_handler"
  runtime         = "python3.9"

  environment {
    variables = {
      WEATHER_API_KEY = var.weather_api_key
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-weather"
    Environment = var.environment
  }
}

resource "aws_lambda_function" "market_demand" {
  filename         = "market_demand_function.zip"
  function_name    = "${var.project_name}-${var.environment}-market-demand"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "index.lambda_handler"
  runtime         = "python3.9"

  tags = {
    Name        = "${var.project_name}-${var.environment}-market-demand"
    Environment = var.environment
  }
}

resource "aws_lambda_function" "competitor_scan" {
  filename         = "competitor_scan_function.zip"
  function_name    = "${var.project_name}-${var.environment}-competitor-scan"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "index.lambda_handler"
  runtime         = "python3.9"

  tags = {
    Name        = "${var.project_name}-${var.environment}-competitor-scan"
    Environment = var.environment
  }
}

resource "aws_lambda_function" "capability_match" {
  filename         = "capability_match_function.zip"
  function_name    = "${var.project_name}-${var.environment}-capability-match"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "index.lambda_handler"
  runtime         = "python3.9"

  tags = {
    Name        = "${var.project_name}-${var.environment}-capability-match"
    Environment = var.environment
  }
}

# Lambda Permissions for Bedrock
resource "aws_lambda_permission" "weather_bedrock" {
  statement_id  = "AllowExecutionFromBedrock"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather.function_name
  principal     = "bedrock.amazonaws.com"
}

resource "aws_lambda_permission" "market_demand_bedrock" {
  statement_id  = "AllowExecutionFromBedrock"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.market_demand.function_name
  principal     = "bedrock.amazonaws.com"
}

resource "aws_lambda_permission" "competitor_scan_bedrock" {
  statement_id  = "AllowExecutionFromBedrock"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.competitor_scan.function_name
  principal     = "bedrock.amazonaws.com"
}

resource "aws_lambda_permission" "capability_match_bedrock" {
  statement_id  = "AllowExecutionFromBedrock"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.capability_match.function_name
  principal     = "bedrock.amazonaws.com"
}