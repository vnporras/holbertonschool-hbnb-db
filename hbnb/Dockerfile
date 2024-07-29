FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -rf /tmp

COPY . .

ENV PORT 5000

EXPOSE $PORT

CMD gunicorn hbnb:app -w 2 -b 0.0.0.0:$PORT
