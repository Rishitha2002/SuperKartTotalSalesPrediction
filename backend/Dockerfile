FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application and model
COPY app.py .
COPY superkart-total-sales-prediction.joblib .

# Flask/Gunicorn port
EXPOSE 7860

# Start Flask API using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "app:superkart_total_sales_predictor_api"]
