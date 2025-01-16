# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    gfortran \
    openblas-dev \
    lapack-dev \
    linux-headers \
    cython

# Copy requirements.txt first to leverage Docker cache if dependencies don’t change
COPY requirements.txt .

# Install numpy and scipy first, as scikit-learn depends on them
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir numpy scipy

# Install remaining dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application using Uvicorn
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
