@echo off
echo Installing AWS CLI and Python dependencies...

REM Install AWS CLI (if not already installed)
pip install awscli boto3

echo.
echo Configure AWS credentials by running:
echo aws configure
echo.
echo You'll need:
echo - AWS Access Key ID
echo - AWS Secret Access Key  
echo - Default region (e.g., us-east-1)
echo - Default output format (json)