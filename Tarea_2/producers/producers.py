from kafka import KafkaProducer
from json import dumps
import uuid
import random
import string

servidores_bootstrap = 'kafka:9092'
topic_products = 'topic_products'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def generate_random_id(length=8):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def enviar_formulario():

    try:
            message = {
                "id": generate_random_id(),
                "product_name": "bob",
                "price": "250.02",
                "email": "bob@bob.cl",
            }
            productor.send(topic_products, value=message)
            print(f"Enviando JSON")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")



if __name__ == "__main__":

    while True:
        print("\nMenú:")
        print("1. Enviar 1000 data")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            for i in range(1000):      
                enviar_formulario()
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
