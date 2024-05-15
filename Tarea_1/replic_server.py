import sqlite3
import redis
from GRPC_API.server_interface import GRPC_Server 

master_instance = redis.Redis(host='127.0.0.1', port=6379, db=0)

slave_instances = [
    redis.Redis(host='127.0.0.1', port=6307, db=0),
    redis.Redis(host='127.0.0.1', port=6302, db=0),
    redis.Redis(host='127.0.0.1', port=6303, db=0)
]

slave_counter = -1
# Función para obtener un esclavo de forma rotativa
def get_slave():
    global slave_counter
    slave_counter += 1

    if slave_counter >= len(slave_instances):
        slave_counter = 0

    return slave_instances[slave_counter]


def Fetch_Response(anime_id):
    global master_instance
    redis_slave = get_slave()

    if redis_slave.exists(anime_id):
        # Obtener el anime de la caché
        anime_title = redis_slave.get(anime_id)

        return {
            "anime_title": anime_title,
            "mode": "cache"
        }

    SQLite_connection = sqlite3.connect('database/database.db')
    SQLite_cursor = SQLite_connection.cursor()
    
    SQLite_cursor.execute("SELECT title FROM anime WHERE id=?", (anime_id,))
    anime_title = SQLite_cursor.fetchone()[0]


    SQLite_cursor.close()
    SQLite_connection.close()
    
    master_instance.set(anime_id, anime_title)

    print(anime_title)
    return {
            "anime_title": anime_title,
            "mode": "db"
            }

grpc_server = GRPC_Server()
grpc_server.Add_Servicer(Fetch_Response)
grpc_server.Start()