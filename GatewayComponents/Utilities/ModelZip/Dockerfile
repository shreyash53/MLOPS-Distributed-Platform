FROM python:3.8-slim-buster

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

# RUN source /home/app/shra/bin/activate
RUN ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
RUN pip install -r requirements.txt
RUN apt-get update -y && \
    apt-get install curl -y
    # rm -rf /var/cache/apk/*
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8001/err || exit 1
HEALTHCHECK --interval=20s --timeout=10s  CMD curl --fail -X POST -H "Content-type: application/json" -d "{\"service_id\" : \"<service_id>\", \"application_type\" : \"<service_type>\"}" "http://192.168.43.74:5001/heartbeat" || exit 1


CMD ["python","-u" ,"model_api.py"]