class MongoDB():
    def __init__(self):
        pass
    
    def conectar(self):
        client = pymongo.MongoClient("mongodb+srv://ummilhao:<password>@cluster0.pfl98rw.mongodb.net/?retryWrites=true&w=majority")
        db = client.test