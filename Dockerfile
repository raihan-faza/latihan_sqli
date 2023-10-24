FROM python:3.11.4-alpine
WORKDIR /flaskr
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["flask","--app","flaskr","init-db"]
CMD ["flask","--app","flaskr","run"]