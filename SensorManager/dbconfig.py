import mongoengine as db


database_name = 'SensorDB'
DB_URI = 'mongodb+srv://kamal:kamal123@cluster0.lzygp.mongodb.net/{}?retryWrites=true&w=majority'.format(
    database_name)


def mongodb():
    db.connect(host=DB_URI)
    return db
