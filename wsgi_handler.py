from aws_lambda_wsgi import response
from src.main import app  # Import your Flask app

def lambda_handler(event, context):
    return response(app, event, context)