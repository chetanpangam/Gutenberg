# Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /bookstore

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run migrations and start the server
CMD ["sh", "-xc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

