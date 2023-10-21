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

# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask application
CMD ["python", "run.py"]
