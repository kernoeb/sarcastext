FROM python:3.13-alpine

WORKDIR /app

# Install deps first so they stay cached across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sarcastext.py .

# Run as non-root.
USER nobody

# config.ini holds the bot token and is NOT baked into the image.
# Mount it at runtime:
#   docker run --rm -v "$PWD/config.ini:/app/config.ini:ro" sarcastext
CMD ["python", "sarcastext.py"]
