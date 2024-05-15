import sqlite3
import redis
from GRPC_API.server_interface import GRPC_Server 

redis_server = redis.Redis(host='localhost', port=6379, db=0)

def Fetch_Response(anime_id):

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