FROM python:3.9

WORKDIR /buda-api

COPY . /buda-api|

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
