from enum import unique
import mongoengine as db

class Actor(db.Document):
    username = db.StringField(required=True,primary_key=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "username":self.username,
            "password": self.password,
            "author":self.role
        }

class applications(db.Document):
    _id = db.StringField(primary_key=True)
    appName = db.StringField(required=True,unique=True)
    path = db.StringField(required=True)
    contract= db.StringField(required=True)

    def to_json(self):
        return {
            "_id": self._id,
            "appName": self.appName,
            "path":self.path,
            "contract":self.contract
        }

class aimodels(db.Document):
    #appid = db.IntField(required=True)
    modelName = db.StringField(required=True,unique=True)
    modelId = db.StringField(reqired=True,unique=True)
    #pickleName = db.StringField(required=True)
    path = db.StringField(required=True)
    contract = db.StringField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "modelName": self.modelName,
            "modelId":self.modelId,
            #"pickleName":self.pickleName,
            "path":self.path,
            "contract":self.contract
        }