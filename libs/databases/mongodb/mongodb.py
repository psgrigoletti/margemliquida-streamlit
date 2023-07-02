from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def buscar_credenciais(password)
    uri = f"mongodb+srv://ummilhao:{password}@cluster0.pfl98rw.mongodb.net/?retryWrites=true&w=majority"
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client.streamlit


def consultarUsuarioPorNome(db, nome):
    usuario = db.usuarios.find_one({'nome': nome})
    return usuario




u = consultarUsuarioPorNome(db, 'psgrigoletti')
print(u)
