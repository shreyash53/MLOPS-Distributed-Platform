from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField, URLField, ListField, DictField

class NodeDocument(Document):
    nodeName = StringField(required=True)
    nodeIpAddress = StringField()
    nodePortNo = StringField()
    nodeUrl = URLField()
    nodeType = StringField(default="platform") #platform, node_app, node_model
    nodeSize = IntField()
    nodeKafkaTopicName = StringField()

# class NodeUtilization(Document):
#     node = ReferenceField(NodeDocument)
#     cpu_utilization

class RunningServices(Document):
    serviceId = StringField()
    seviceType = StringField(default='app') #app, model
    node = ReferenceField(NodeDocument)
