# ML Ops-Distributed-Platform

This is an AI/IOT platform wherein Data Scientists can upload ML Models and Application Developers to build AI Applications and deploy them to the platform. 

The platform implements a micro-service based architecture with features like scaling, fault tolerance, scheduling,
centralized logging and monitoring. 

The platform consists of many actors, namely Platform Admin, Data Scientist, Application Developer, and End User (Application Runner).
It consists of several components like Service Lifecycle Manager, Node
Manager, Scheduler, Monitoring Service, Deployment Manager and Sensor Manager.

## Application Diagram
![alt text](https://raw.githubusercontent.com/shreyash53/MLOPS-Distributed-Platform/main/Application%20Diagram.jpg)

## Technology used 
### Flask
Flask is a web framework, it's a Python module that lets you develop web applications easily. 

Flask is used for developing RESTful APIs and Web services for the platform.
### MongoDB
MongoDB is a document database with the scalability and flexibility and provid querying and indexing over the data.

Centralized database is created for AI models, user applications, Platform repository and sensor data.
### Kafka
Kafka is a distributed data store optimized for ingesting and processing streaming data in real-time. 
Kafka used for communication among the micro-services, especially where the data flow is unidirectional.

### Docker
Docker is a software platform that allows you to build, test, and deploy applications quickly. 

All the micro-services are Dockerized like SLCM, Node manager, etc. Similarly, all user applications are first dockerized and then run on a child node.

### Azure Web Apps



## Start up