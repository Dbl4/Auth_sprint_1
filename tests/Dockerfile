FROM python:3.10

WORKDIR /opt/tests
COPY tests/functional functional
COPY tests/__init__.py .
COPY tests/conftest.py .
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["bash"]
