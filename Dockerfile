# Use a stable Debian-based Python image
FROM public.ecr.aws/docker/library/python:3.12-slim

ARG REPOSITORY_URI
ARG SCHEMA
ARG DB_NAME
ARG JWT_SECRET_KEY
ARG DATABASE_URL

ENV REPOSITORY_URI=${REPOSITORY_URI}
ENV SCHEMA=${SCHEMA}
ENV DB_NAME=${DB_NAME}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    vim \
    unzip \
    libz-dev \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*


RUN curl -o /tmp/zlib1g_1.3.dfsg+really1.3.1-1+b1_amd64.deb https://ftp.debian.org/debian/pool/main/z/zlib/zlib1g_1.3.dfsg+really1.3.1-1+b1_amd64.deb && \
    curl -o /tmp/zlib1g-dev_1.3.dfsg+really1.3.1-1+b1_amd64.deb https://ftp.debian.org/debian/pool/main/z/zlib/zlib1g-dev_1.3.dfsg+really1.3.1-1+b1_amd64.deb && \
    dpkg -i /tmp/zlib1g_1.3.dfsg+really1.3.1-1+b1_amd64.deb /tmp/zlib1g-dev_1.3.dfsg+really1.3.1-1+b1_amd64.deb || apt-get install -f -y && \
    rm -f /tmp/zlib1g_1.3.dfsg+really1.3.1-1+b1_amd64.deb /tmp/zlib1g-dev_1.3.dfsg+really1.3.1-1+b1_amd64.deb

# Create a non-root user for security
RUN useradd -m -s /bin/bash flaskuser && chown -R flaskuser:flaskuser /app

# Switch to non-root user
USER flaskuser

# Copy dependencies first
COPY --chown=flaskuser:flaskuser requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (adjust if .dockerignore excludes something)
COPY --chown=flaskuser:flaskuser . /app/

# Expose Flask port
EXPOSE 5000

# Copy the .env file
#COPY --chown=flaskuser:flaskuser docker/.env /app/

# Set environment variables
ENV PATH="/home/flaskuser/.local/bin:${PATH}"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Start the Streamlit application
CMD ["python3", "/app/backend/app.py"]
