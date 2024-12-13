FROM python:3.12-alpine

LABEL maintainer="hani"

WORKDIR /app 

ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

COPY api/start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]