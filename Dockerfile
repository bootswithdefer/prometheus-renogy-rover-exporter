FROM python:3-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY prometheus-rover-exporter.py .

CMD [ "python3", "prometheus-rover-exporter.py" ]
