FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create temp directory with proper permissions
RUN mkdir -p /app/tmp && chmod 777 /app/tmp

# Set TMPDIR environment variable for Python's tempfile module
ENV TMPDIR=/app/tmp

COPY app.py .

USER nobody

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 