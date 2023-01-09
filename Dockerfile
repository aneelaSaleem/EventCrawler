FROM python:3.10

# Install the PostgreSQL client library
RUN apt-get update && apt-get install -y libpq-dev

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Run the application
CMD ["python3", "main.py"]
