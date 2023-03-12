FROM python:3.10

WORKDIR /opt/etl

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY etl .

CMD ["python", "main.py"]
