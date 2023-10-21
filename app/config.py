import os

# Flask Config
DEBUG = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

# SQLAlchemy Config
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://your_db_user:your_db_password@db/your_db_name')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery Config
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# File Upload Config
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output')

# JWT Config
JWT_IDENTITY_CLAIM = os.getenv('JWT_IDENTITY_CLAIM', 'username')

# Token Expiry
JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', False)

# Redis
REDIS_HOST= os.getenv('REDIS_HOST', False)
REDIS_URL= os.getenv('REDIS_URL', "redis://redis:6379") 

# Postgres Variables
POSTGRES_DB=os.getenv('POSTGRES_DB', "test")
POSTGRES_USER=os.getenv('POSTGRES_USER', "test")
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD', "test")

# Marshmallow Config
from marshmallow import fields

class CustomFields:
    class Timestamp(fields.DateTime):
        def _serialize(self, value, attr, obj, **kwargs):
            if value is None:
                return None
            return value.timestamp()

# Create a dictionary with custom fields
# from marshmallow import Schema
# class MySchema(Schema):
#     class Meta:
#         fields = CustomFields.__dict__.keys()
