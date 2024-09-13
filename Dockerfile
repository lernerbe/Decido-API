FROM python:3.11-alpine

WORKDIR /usr/app

COPY ./requirements.txt ./

ENV TZ UTC

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn src.main:app --host 0.0.0.0 --port 8000


