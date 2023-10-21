from src import create_app

# Create the Flask app
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)
