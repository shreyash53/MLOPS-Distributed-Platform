FROM python:3.8-slim-buster

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

# RUN source /home/app/shra/bin/activate
RUN pip install -r requirements.txt
RUN apk update && \
    apk add curl \
    rm -rf /var/cache/apk/*

HEALTHCHECK --interval=20s --timeout=10s  CMD curl --fail -X POST -H "Content-type: application/json" -d "{\"service_id\" : \"John\", \"application_type\" : \"Smith\"}" "http://10.2.136.88:5000/heartbeat" || exit 1


CMD ["python","logging_service.py"]