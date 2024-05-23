# pull official base image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir /app/app_web

COPY ./requirements.txt /app/app_web/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade  -r /app/app_web/requirements.txt

COPY . /app/app_web

# Collect static files
RUN python /app/app_web/manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

WORKDIR /app/app_web

# Run app.py when the container launches
CMD ["gunicorn", "--bind", ":8000", "--chdir", "/app/app_web", "app_web.wsgi:application"]