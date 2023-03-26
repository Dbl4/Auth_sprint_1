FROM python:3.10

WORKDIR /auth

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY auth .
CMD /usr/local/bin/flask db upgrade head && /usr/local/bin/python app.py
