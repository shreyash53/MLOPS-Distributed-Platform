FROM python:3.8.13-alpine3.14

RUN mkdir -p /home/app
WORKDIR /home/app

COPY . .

# RUN source /home/app/shra/bin/activate
RUN pip install -r requirements.txt

CMD ["python","produce.py"]