FROM python:3.9-slim

WORKDIR /docker

# Install system-level dependencies
RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]