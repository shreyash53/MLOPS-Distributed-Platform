

from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField, URLField, ListField, DictField

class ServicesRunning(Document):
    serviceId = StringField()
    serviceName = StringField()
    serviceType = StringField()
    serviceDockerTagName = StringField()
    serviceDockerContainerName = StringField()
    serviceDockerFileLocation = StringField()
    serviceNodeId = StringField()
    serviceDockerPort = StringField()
