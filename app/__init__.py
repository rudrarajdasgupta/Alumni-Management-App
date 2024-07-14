from flask import Flask
import logging
from config import Config
from .extensions import db, migrate, bcrypt, jwt
from .api import register_apis
import boto3

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Set up DynamoDB
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=app.config['ENDPOINT_URL'],
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=app.config['AWS_REGION']
        
    )
    app.dynamodb = dynamodb
    app.dynamodb_file_management_table = dynamodb.Table(app.config['DYNAMODB_FILE_MANAGEMENT_TABLE_NAME'])
    app.dynamodb_config_table = dynamodb.Table(app.config['DYNAMODB_CONFIG_TABLE_NAME'])

    # Register APIs
    register_apis(app)

    # Logging
    logging.basicConfig(filename='app.log', level=logging.NOTSET, format='%(asctime)s:%(levelname)s:%(message)s')

    return app