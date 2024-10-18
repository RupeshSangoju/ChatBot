# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

# Set the Flask environment variable
ENV FLASK_APP=backend.py
