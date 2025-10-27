# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements if you have them
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
