FROM python:3.8.13-alpine3.14

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

# RUN source /home/app/shra/bin/activate
RUN pip install -r requirements.txt
RUN apk update && \
    apk add curl \
    rm -rf /var/cache/apk/*
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8001/err || exit 1

CMD ["python", "<app_name>.py"]