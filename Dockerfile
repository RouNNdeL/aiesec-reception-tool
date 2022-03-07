FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./receptiontool /app/receptiontool
COPY ./bin /app/bin
COPY ./setup.py /app
RUN pip install .

CMD [ "python", "/app/bin/receptiontool" ]
