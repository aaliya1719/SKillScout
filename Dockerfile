# Use the official lightweight Python image.
FROM python:3.9-slim

# Set working directory.
WORKDIR /app

# Copy local code to the container image.
COPY . .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit uses port 8501 by default, but Cloud Run prefers 8080.
EXPOSE 8080

# Run the web service on container startup.
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]