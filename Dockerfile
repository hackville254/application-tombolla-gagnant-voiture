FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8493", "tombolaApp.wsgi:application"]
