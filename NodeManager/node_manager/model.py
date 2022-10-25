from mongoengine.document import Document
from mongoengine.fields import IntField,FloatField, ReferenceField, StringField, URLField, ListField, DictField

class NodeDocument(Document):
    nodeName = StringField(unique=True, required=True)
    nodeIpAddress = StringField()
    nodePortNo = StringField()
    nodeUrl = URLField()
    nodeType = StringField(default="platform") #platform, node_app, node_model
    nodeSize = IntField()
    nodeKafkaTopicName = StringField()
    node_cpu_usage = FloatField(default=0)
    node_ram_usage=FloatField(default=0)

    def get_usage(self):
        return {
            "node_name" : self.nodeName,
            "cpu" : int(self.node_cpu_usage),
            "memory" : int(self.node_ram_usage),
        }

# class NodeUtilization(Document):
#     node = ReferenceField(NodeDocument)
#     cpu_utilization

class RunningServices(Document):
    serviceId = StringField()
    serviceType = StringField(default='app') #app, model
    node = ReferenceField(NodeDocument)
