import mongoengine as db


database_name = 'test'
DB_URI =  'mongodb://localhost/test'.format(database_name)

def mongodb():
    db.connect(host=DB_URI)
    return db