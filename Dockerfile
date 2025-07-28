FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create data directories including PDFs subdirectory
RUN mkdir -p /data/input/PDFs /data/output

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl

# Copy source code and tests
COPY src/ ./src/
COPY tests/ ./tests/
COPY approach_explanation.md .
COPY README.md .

# Set Python path
ENV PYTHONPATH=/app

# Create volume for input/output
VOLUME ["/data"]

# Run the application
ENTRYPOINT ["python", "-m", "src.main"]