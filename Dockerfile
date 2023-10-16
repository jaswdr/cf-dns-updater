FROM python:3.10-alpine

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY ./main.py ./main.py

CMD ["python", "main.py"]