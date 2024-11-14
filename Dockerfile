# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Create the generated_maps directory with correct permissions
RUN mkdir -p /app/generated_maps && chmod -R 755 /app/generated_maps

# Copy the requirements file and install dependencies
COPY requirements/*.txt ./requirements/

RUN apt-get update && apt-get install -y wkhtmltopdf && \
    pip install --no-cache-dir -r requirements/requirements-dev.txt

# Copy the application code
COPY ./src ./src

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
