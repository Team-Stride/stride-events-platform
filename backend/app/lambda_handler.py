"""
AWS Lambda handler for Stride Events Platform
Wraps FastAPI application for Lambda execution
"""
from mangum import Mangum
from app.main import app

# Create Lambda handler
handler = Mangum(app, lifespan="off")
