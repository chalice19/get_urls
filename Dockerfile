FROM python:3.12-alpine
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY links.py ./

RUN adduser -S app
USER app

ENTRYPOINT ["python3", "./links.py"]