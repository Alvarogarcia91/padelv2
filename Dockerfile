# Use the full Python image
FROM python:3.11

# Prevents Python from buffering logs
ENV PYTHONUNBUFFERED=1 

# Set the working directory inside the container
WORKDIR /code

# Install system dependencies for PostgreSQL and package compilation
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependencies file first (optimizes Docker cache)
COPY requirements.txt /code/

# Install all dependencies in a single step (more efficient)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code after installing dependencies
COPY . /code/

# Create a non-root user for security
RUN useradd --create-home django-user
USER django-user

# Expose port 8000 for Django
EXPOSE 8000

# Default command to run Django in development mode
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
