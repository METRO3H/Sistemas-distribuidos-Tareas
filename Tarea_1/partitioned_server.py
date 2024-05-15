import sqlite3
import hashlib
import redis
from GRPC_API.server_interface import GRPC_Server 


# Define tus instancias de Redis aquí
redis_instances = [
    redis.Redis(host='127.0.0.1', port=6379, db=0),
    redis.Redis(host='127.0.0.1', port=6370, db=0),
    redis.Redis(host='127.0.0.1', port=6350, db=0)
]

num_redis_instances = len(redis_instances)

def get_redis_instance(key):
    hash_object = hashlib.md5(key.encode())
    hash_key = int(hash_object.hexdigest(), 16)
    redis_instance = hash_key % num_redis_instances
    return redis_instances[redis_instance]

def set_value(key, value):
    r = get_redis_instance(key)
    r.set(key, value)

def get_value(key):
    r = get_redis_instance(key)
    return r.get(key)


def Fetch_Response(anime_id):
    redis_server = get_redis_instance(anime_id)
    if redis_server.exists(anime_id):
        # Obtener el anime de la caché
        anime_title = redis_server.get(anime_id)

        return {
            "anime_title": anime_title,
            "mode": "cache"
        }

    SQLite_connection = sqlite3.connect('database/database.db')
    SQLite_cursor = SQLite_connection.cursor()
    
    SQLite_cursor.execute("SELECT title FROM anime WHERE id=?", (anime_id,))
    anime_title = SQLite_cursor.fetchone()[0]
    print(anime_title)

    SQLite_cursor.close()
    SQLite_connection.close()

    # Almacenar el anime en la caché
    redis_server.set(anime_id, anime_title)

    return {
            "anime_title": anime_title,
            "mode": "db"
            }

grpc_server = GRPC_Server()
grpc_server.Add_Servicer(Fetch_Response)
grpc_server.Start()