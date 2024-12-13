FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY app /app

# Specify the command to run the application
CMD ["python", "app.py"]
