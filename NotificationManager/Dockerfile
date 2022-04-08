FROM python:3.10-alpine3.14

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

RUN pip install -r requirements.txt

CMD ["python","notificationmanager.py"]
EXPOSE 8000