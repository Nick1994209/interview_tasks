FROM python:3.7.2-alpine3.8

# mypy, certifi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/
COPY . .

#CMD uwsgi --http=":8000" --wsgi-file=/usr/src/app/project/wsgi.py --processes=2 --threads=2 --harakiri=60
