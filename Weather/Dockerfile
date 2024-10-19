# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "weather_app.py"]
