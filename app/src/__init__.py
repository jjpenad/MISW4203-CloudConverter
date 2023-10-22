
from flask import Flask
from flask_jwt_extended import JWTManager
from celery import Celery, Task
from dotenv import load_dotenv  # Import the load_dotenv function
from .models import db
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from src.views import api


url = URL.create(
    drivername="postgresql",
    username="coderpad",
    host="/tmp/postgresql/socket",
    database="coderpad"
)

engine = create_engine(url)

# Initialize extensions
jwt = JWTManager()

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app():
    app = Flask(__name__)

    # Load configuration from a .env file
    load_dotenv()

    # Load configuration from config.py
    app.config.from_pyfile('../config.py')

    # Configure the database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Configure JWT
    jwt.init_app(app)

    # Import and register blueprints
    app.register_blueprint(api, url_prefix='/api')

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    celery_init_app(app)
    return app

