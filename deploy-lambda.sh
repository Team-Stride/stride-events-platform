#!/bin/bash
# AWS Lambda Deployment Script for Stride Events Platform

set -e

echo "🚀 Deploying Stride Events Platform to AWS Lambda"

# Variables
FUNCTION_NAME="stride-events-api"
REGION="ap-south-1"  # Mumbai region
RUNTIME="python3.11"
HANDLER="app.lambda_handler.handler"
ROLE_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role"

# Create deployment package
echo "📦 Creating deployment package..."
cd backend
pip install -r requirements.txt -t package/
cp -r app package/
cd package
zip -r ../deployment-package.zip .
cd ..

# Upload to Lambda
echo "⬆️  Uploading to AWS Lambda..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://deployment-package.zip \
    --region $REGION

# Update environment variables
echo "⚙️  Updating environment variables..."
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment "Variables={
        DATABASE_URL=$DATABASE_URL,
        JWT_SECRET=$JWT_SECRET,
        STRIDE_ID_API_KEY=$STRIDE_ID_API_KEY,
        SENDGRID_API_KEY=$SENDGRID_API_KEY,
        KARIX_API_KEY=$KARIX_API_KEY,
        RAZORPAY_KEY_ID=$RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET=$RAZORPAY_KEY_SECRET
    }" \
    --region $REGION

echo "✅ Deployment complete!"
echo "🔗 API Gateway URL: https://YOUR_API_ID.execute-api.$REGION.amazonaws.com/prod"
