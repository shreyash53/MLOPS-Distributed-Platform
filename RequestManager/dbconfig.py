from flask import Flask
import mongoengine as db

database_name = 'sample'
password = 'test123'
DB_URI =  'mongodb+srv://kamal:kamal123@cluster0.lzygp.mongodb.net/firstdb?retryWrites=true&w=majority'

def mongodb():
    db.connect(host=DB_URI)
    return db