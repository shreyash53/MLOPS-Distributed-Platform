import mongoengine as db


database_name = 'logging_db'
DB_URI =  'mongodb+srv://kamal:kamal123@cluster0.lzygp.mongodb.net/{}?retryWrites=true&w=majority'.format(database_name)

class Logs(db.Document):
    service_name = db.StringField()
    msg = db.StringField()
    time = db.StringField()

    def to_json(self):
        return {
            "service_name": self.service_name,
            "msg":self.msg,
            "time":self.time
        }

def mongodb():
    db.connect(host=DB_URI)
    return db