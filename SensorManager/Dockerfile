FROM python:3.8.13-alpine3.14
RUN mkdir -p /home/app
COPY . /home/app
# RUN source /home/app/shra/bin/activate
RUN pip install -r /home/app/requirements.txt
CMD ["python3", "/home/app/Sensor_Manager_Driver.py"]