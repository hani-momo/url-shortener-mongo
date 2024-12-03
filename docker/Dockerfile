FROM python:3.12-alpine

LABEL maintainer="hani"

WORKDIR /app

ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ../requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ../url_shortener/ .

EXPOSE 8000

COPY ../api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]