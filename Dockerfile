FROM python:3.9

WORKDIR /buda-api

COPY ./requirements.txt buda-api/requirements.text

RUN pip install --no-cache-dir --upgrade -r /buda-api/requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
