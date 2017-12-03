FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
# mariadb-dev - see https://bugs.alpinelinux.org/issues/4768 for libmysqlclient-dev
# postgresql-dev - see https://bugs.alpinelinux.org/issues/3642 for libpq-devs
RUN apk add --update \
    mariadb-dev \
    libffi-dev \
    gcc \
    jpeg-dev \
    linux-headers \
    musl-dev \
    postgresql-dev
RUN mkdir /code /code/production
WORKDIR /code
COPY requirements/*.txt /code/requirements/
RUN pip install --no-cache-dir -r requirements/local.txt && pip install --no-cache-dir -r requirements/test.txt
COPY . /code/
