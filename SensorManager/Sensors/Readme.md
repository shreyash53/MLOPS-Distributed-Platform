# Sensor Manager

Sensor Manager is the component which takes care of most the sensor related activities.(Registration, Binding, Sending data from Sensor to kafka topic and recieving data from the topic to the controller)

## Usage


```bash
python3 Sensor_Manager_Driver.py
```

When the platform admin provides the json file for registration and binding then the sensor manager will start a new thread according to the data provided(is it a sensor or a controller) to produce the data to the topic or consume the data from the topic.  