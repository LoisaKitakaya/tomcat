FROM python:3.10-alpine3.18

WORKDIR /app

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    openssl-dev \
    python3-dev \
    postgresql-dev \
    postgresql-client \
    && rm -rf /var/cache/apk/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -u 1000 -D testuser

RUN chown -R testuser:testuser /app

USER testuser

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
