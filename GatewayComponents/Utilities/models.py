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
    appName = db.StringField(required=True,unique=True)
    path = db.StringField(required=True)
    contract= db.StringField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "appName": self.appName,
            "path":self.path,
            "contract":self.contract
        }

class aimodels(db.Document):
    #appid = db.IntField(required=True)
    modelName = db.StringField(required=True,unique=True)
    #pickleName = db.StringField(required=True)
    path = db.StringField(required=True)
    contract = db.StringField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "modelName": self.modelName,
            #"pickleName":self.pickleName,
            "path":self.path,
            "contract":self.contract
        }