# Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt update
RUN apt install tshark -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY zeus_controller.py .

ENTRYPOINT ["python", "zeus_controller.py"]

