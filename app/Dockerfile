# Use the official Python image as the base image
FROM python:3.9

# Set environment variables for Flask
# ENV FLASK_APP=app/__init__.py
# ENV FLASK_ENV=development
# ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start-server.sh /start-server.sh
RUN sed -i 's/\r$//g' ./start-server.sh
RUN chmod +x ./start-server.sh

COPY ./start-worker.sh /start-worker.sh
RUN sed -i 's/\r$//g' ./start-worker.sh
RUN chmod +x ./start-worker.sh

# Start the Flask application
#CMD ["python", "run.py"]

#CMD ["sh", "-c", "celery -A run worker --loglevel INFO && python run.py"]

ENTRYPOINT ["/entrypoint.sh"]
