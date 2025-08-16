FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements_flask.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_flask.txt

# Copy application files
COPY flask_app.py .
COPY superkart_model.pkl .
COPY superkart_preprocessor.pkl .

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Set environment variables
ENV FLASK_APP=flask_app.py
ENV FLASK_ENV=production
ENV PORT=7860

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120", "flask_app:app"]