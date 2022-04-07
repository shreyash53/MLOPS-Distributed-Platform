FROM python:3.8-slim-buster

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

# RUN source /home/app/shra/bin/activate
RUN pip install -r requirements.txt
RUN apk update && \
    apk add curl \
    rm -rf /var/cache/apk/*
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8001/err || exit 1
HEALTHCHECK --interval=20s --timeout=10s  CMD curl --fail -X POST -H "Content-type: application/json" -d "{\"service_id\" : \"John\", \"application_type\" : \"Smith\"}" "192.168.96.74:5001/heartbeat" || exit 1


CMD ["python","-u" ,"<app_name>.py"]



