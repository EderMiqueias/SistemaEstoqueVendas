import pymongo

url = "127.0.0.1"
port = 27017
client = pymongo.MongoClient(host=url, port=port)


def getdb():
    db = client['sistemaestoquevendas']
    return db
