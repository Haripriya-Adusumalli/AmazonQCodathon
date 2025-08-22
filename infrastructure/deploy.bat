@echo off
REM Product Opportunity Recommendation System - Windows Deployment Script

setlocal enabledelayedexpansion

set PROJECT_NAME=product-opportunity-system
set ENVIRONMENT=dev
set REGION=us-east-1

echo 🚀 Deploying Product Opportunity Recommendation System
echo ==================================================

REM Check if AWS CLI is configured
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS CLI not configured. Run 'aws configure' first.
    exit /b 1
)

echo ✅ AWS CLI configured

REM Deploy using CloudFormation by default
set DEPLOYMENT_TYPE=%1
if "%DEPLOYMENT_TYPE%"=="" set DEPLOYMENT_TYPE=cloudformation

if "%DEPLOYMENT_TYPE%"=="cloudformation" goto deploy_cf
if "%DEPLOYMENT_TYPE%"=="cf" goto deploy_cf
if "%DEPLOYMENT_TYPE%"=="terraform" goto deploy_tf
if "%DEPLOYMENT_TYPE%"=="tf" goto deploy_tf

echo Usage: %0 [cloudformation^|terraform]
echo Default: cloudformation
exit /b 1

:deploy_cf
echo 📦 Deploying with CloudFormation...

REM Deploy main stack
aws cloudformation deploy ^
    --template-file cloudformation\main-stack.yaml ^
    --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main ^
    --parameter-overrides file://cloudformation/parameters.json ^
    --capabilities CAPABILITY_IAM ^
    --region %REGION%

if errorlevel 1 (
    echo ❌ Main stack deployment failed
    exit /b 1
)

echo ✅ Main stack deployed

REM Get outputs from main stack
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`BedrockAgentRoleArn`].OutputValue" --output text --region %REGION%') do set BEDROCK_ROLE_ARN=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`WeatherFunctionArn`].OutputValue" --output text --region %REGION%') do set WEATHER_FUNCTION_ARN=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`MarketDemandFunctionArn`].OutputValue" --output text --region %REGION%') do set MARKET_DEMAND_FUNCTION_ARN=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`CompetitorScanFunctionArn`].OutputValue" --output text --region %REGION%') do set COMPETITOR_SCAN_FUNCTION_ARN=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`CapabilityMatchFunctionArn`].OutputValue" --output text --region %REGION%') do set CAPABILITY_MATCH_FUNCTION_ARN=%%i

REM Deploy Bedrock agents stack
aws cloudformation deploy ^
    --template-file cloudformation\bedrock-agents.yaml ^
    --stack-name %PROJECT_NAME%-%ENVIRONMENT%-agents ^
    --parameter-overrides ^
        ProjectName=%PROJECT_NAME% ^
        Environment=%ENVIRONMENT% ^
        BedrockAgentRoleArn=%BEDROCK_ROLE_ARN% ^
        WeatherFunctionArn=%WEATHER_FUNCTION_ARN% ^
        MarketDemandFunctionArn=%MARKET_DEMAND_FUNCTION_ARN% ^
        CompetitorScanFunctionArn=%COMPETITOR_SCAN_FUNCTION_ARN% ^
        CapabilityMatchFunctionArn=%CAPABILITY_MATCH_FUNCTION_ARN% ^
    --capabilities CAPABILITY_IAM ^
    --region %REGION%

if errorlevel 1 (
    echo ❌ Bedrock agents deployment failed
    exit /b 1
)

echo ✅ Bedrock agents deployed

REM Get final outputs and generate config
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue" --output text --region %REGION%') do set USER_POOL_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`UserPoolClientId`].OutputValue" --output text --region %REGION%') do set USER_POOL_CLIENT_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-main --query "Stacks[0].Outputs[?OutputKey==`IdentityPoolId`].OutputValue" --output text --region %REGION%') do set IDENTITY_POOL_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-agents --query "Stacks[0].Outputs[?OutputKey==`WeatherAgentId`].OutputValue" --output text --region %REGION%') do set WEATHER_AGENT_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-agents --query "Stacks[0].Outputs[?OutputKey==`WeatherAgentAliasId`].OutputValue" --output text --region %REGION%') do set WEATHER_AGENT_ALIAS_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-agents --query "Stacks[0].Outputs[?OutputKey==`ProductOpportunityAgentId`].OutputValue" --output text --region %REGION%') do set PRODUCT_AGENT_ID=%%i
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %PROJECT_NAME%-%ENVIRONMENT%-agents --query "Stacks[0].Outputs[?OutputKey==`ProductOpportunityAgentAliasId`].OutputValue" --output text --region %REGION%') do set PRODUCT_AGENT_ALIAS_ID=%%i

REM Generate aws-config.js
(
echo export const awsConfig = {
echo   Auth: {
echo     Cognito: {
echo       userPoolId: '%USER_POOL_ID%',
echo       userPoolClientId: '%USER_POOL_CLIENT_ID%',
echo       region: '%REGION%',
echo       identityPoolId: '%IDENTITY_POOL_ID%'
echo     }
echo   }
echo };
echo.
echo export const bedrockConfig = {
echo   agentId: '%WEATHER_AGENT_ID%',
echo   aliasId: '%WEATHER_AGENT_ALIAS_ID%',
echo   region: '%REGION%'
echo };
echo.
echo export const productOpportunityConfig = {
echo   agentId: '%PRODUCT_AGENT_ID%',
echo   aliasId: '%PRODUCT_AGENT_ALIAS_ID%',
echo   region: '%REGION%'
echo };
) > ..\src\aws-config.js

echo ✅ AWS configuration updated
goto end

:deploy_tf
echo 📦 Deploying with Terraform...
cd terraform

terraform init
if errorlevel 1 (
    echo ❌ Terraform init failed
    exit /b 1
)

terraform plan -var-file="terraform.tfvars"
if errorlevel 1 (
    echo ❌ Terraform plan failed
    exit /b 1
)

terraform apply -var-file="terraform.tfvars" -auto-approve
if errorlevel 1 (
    echo ❌ Terraform apply failed
    exit /b 1
)

echo ✅ Terraform deployment complete
echo ⚠️  Deploy Bedrock agents separately using CloudFormation or Python scripts
cd ..

:end
echo.
echo 🎉 Deployment complete!
echo ==================================================
echo Next steps:
echo 1. Update src/aws-config.js with your API keys if needed
echo 2. Run: npm install ^&^& npm start
echo 3. Open: http://localhost:3000
echo.