from kafka import KafkaConsumer
import psycopg2
import json
import random
import string, time
from datetime import datetime
from mailer import mail

servidores_bootstrap = 'kafka:9092'

DATABASE_CONFIG = {
    'dbname': 'proyecto',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

counter = 0

def consume_messages(topic_name, table_name):
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=servidores_bootstrap,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=5000  # Cierra el consumidor después de 5 segundos si no se reciben mensajes
)

    mensajes_guardados = []  # Lista para guardar los primeros 10 mensajes
    cont = 0
    global counter
    try:
        for message in consumer:
            if cont < counter:
             continue
            
            print(f"Recibido mensaje de {message.topic} :")
            
            # Agregamos el mensaje a la lista
            mensajes_guardados.append(message.value)
            
            product_id = str(message.value["id"])
            product_name = message.value["product_name"]
            product_price = message.value["price"]
            product_email = message.value["email"]
            
            insert_product = "INSERT INTO products (id, name, price, email) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"

            try:
                cursor.execute(insert_product, (product_id, product_name, product_price, product_email))
                conn.commit()
                cont += 1
            except psycopg2.Error as e:
                print(f"Error al insertar en la base de datos: {e}")
                conn.rollback()

    finally:
        # Cerramos el consumidor explícitamente
        consumer.close()
        cursor.close()
        conn.close()
        counter = cont
        # Imprimir los mensajes guardados
        print("Mensajes guardados:", mensajes_guardados)

if __name__ == "__main__":
 while True:
     print("Menú Consumidores:")
     print("1. Consumir mensajes")
     print("5. Salir")

     opcion = input("Elige una opción: ")

     if opcion == "1":
         consume_messages('topic_products', 'products')
     else:
         print("Opción no válida.")
