#!/usr/bin/env python3
import json
import sys

def generate_mermaid_diagram():
    """Generate Mermaid diagram for the React Cognito Bedrock architecture"""
    
    mermaid_code = """
graph TD
    A[Users] --> B[CloudFront CDN]
    B --> C[S3 Static Hosting]
    C --> D[React App<br/>Cognito Auth UI]
    
    D --> E[Cognito User Pool<br/>us-east-1_liYtIs82R]
    E --> F[IAM Role<br/>Cognito_WeatherAppAuth_Role]
    
    D --> G[Bedrock Agent<br/>Weather Assistant]
    G --> H[Lambda Function<br/>weather-function]
    H --> I[OpenWeatherMap API]
    
    I --> H
    H --> G
    G --> D
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#fff3e0
    style G fill:#e8f5e8
    style I fill:#fce4ec
"""
    
    return mermaid_code.strip()

def generate_plantuml_diagram():
    """Generate PlantUML diagram for the architecture"""
    
    plantuml_code = """
@startuml
!define AWSPuml https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v15.0/dist
!includeurl AWSPuml/AWSCommon.puml
!includeurl AWSPuml/ApplicationIntegration/APIGateway.puml
!includeurl AWSPuml/Compute/Lambda.puml
!includeurl AWSPuml/SecurityIdentityCompliance/Cognito.puml
!includeurl AWSPuml/MachineLearning/Bedrock.puml
!includeurl AWSPuml/Storage/S3.puml
!includeurl AWSPuml/NetworkingContentDelivery/CloudFront.puml

actor Users as users
CloudFront(cloudfront, "CloudFront CDN", "Content Delivery")
S3(s3, "S3 Bucket", "Static Hosting")
rectangle "React App" as react
Cognito(cognito, "User Pool", "us-east-1_liYtIs82R")
rectangle "IAM Role" as iam
Bedrock(bedrock, "Bedrock Agent", "Weather Assistant")
Lambda(lambda, "Lambda Function", "weather-function")
cloud "OpenWeatherMap API" as weather

users --> cloudfront
cloudfront --> s3
s3 --> react
react --> cognito
cognito --> iam
react --> bedrock
bedrock --> lambda
lambda --> weather
weather --> lambda
lambda --> bedrock
bedrock --> react

@enduml
"""
    
    return plantuml_code.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp-diagram-server.py <format>")
        print("Formats: mermaid, plantuml")
        sys.exit(1)
    
    format_type = sys.argv[1].lower()
    
    if format_type == "mermaid":
        diagram = generate_mermaid_diagram()
        print("# Mermaid Diagram")
        print("```mermaid")
        print(diagram)
        print("```")
        print("\nTo render: Copy to https://mermaid.live/")
        
    elif format_type == "plantuml":
        diagram = generate_plantuml_diagram()
        print("# PlantUML Diagram")
        print("```plantuml")
        print(diagram)
        print("```")
        print("\nTo render: Copy to https://www.plantuml.com/plantuml/")
        
    else:
        print(f"Unknown format: {format_type}")
        print("Available formats: mermaid, plantuml")

if __name__ == "__main__":
    main()