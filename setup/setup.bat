@echo off
echo ========================================
echo Product Opportunity Recommendation System
echo Quick Setup Script
echo ========================================

echo.
echo [1/5] Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)

echo.
echo [2/5] Checking AWS CLI configuration...
aws sts get-caller-identity >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: AWS CLI not configured. Run 'aws configure' first.
    echo Press any key to continue anyway...
    pause >nul
)

echo.
echo [3/5] Checking Bedrock model access...
python simple-bedrock-check.py
if %errorlevel% neq 0 (
    echo WARNING: Bedrock access issue. Check model permissions in AWS Console.
)

echo.
echo [4/5] Deploying weather agent...
cd bedrock-agent
python complete-deploy.py
cd ..

echo.
echo [5/5] Deploying product opportunity agent...
cd bedrock-agent\product-opportunity-agent
python simple-deploy.py
cd ..\..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update src/aws-config.js with your agent IDs
echo 2. Run 'npm start' to launch the application
echo 3. Open http://localhost:3000 in your browser
echo.
pause