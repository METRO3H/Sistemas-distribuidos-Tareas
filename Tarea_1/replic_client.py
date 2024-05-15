
from GRPC_API.client_interface import Get_Anime
import random
import time
import json
import os
import redis

random.seed(5)

def Run_Test(policy):
    time_response_list = []
    counter = {
        "cache": 0,
        "db": 0,
        "error": 0           
    }

    anime_ids = [random.randint(1, 10000) for _ in range(10000)]

    for anime_id in anime_ids:
        start = time.time()

        response = Get_Anime(anime_id)

        end = time.time()

        if response is None:
            counter["error"] += 1
            continue

        counter[response["mode"]] += 1

        time_response = end - start - float(response["time_error"])
        time_response_list.append(time_response)

    average_time_response = sum(time_response_list)/len(time_response_list)
    average_time_response = round(average_time_response * 1000, 3)

    # print("\nAverage time response : ", average_time_response, "ms")
    # print("Cache COUNTER : ", counter["cache"])
    # print("Database COUNTER : ", counter["db"])
    # print("Error COUNTER : ", counter["error"])
    
    
    results = {
        "removal_policy": policy,
        "average_time_response": average_time_response,
        "cache_counter": counter["cache"],
        "database_counter": counter["db"]
    }

    cache_type = "replic"
    file_path = f"results/{cache_type}.json"


    # Verificar si el archivo ya existe
    if os.path.isfile(file_path):
        # Si el archivo existe, abrirlo y cargar los datos existentes
        with open(file_path, "r") as file:
            existing_data = json.load(file)

        # Agregar los nuevos datos al diccionario existente
        existing_data.append(results)
        results = existing_data
    else:
        results = [results]
        
    # Escribir los datos en el archivo json
    with open(file_path, "w") as file:
        json.dump(results, file, indent=4)


redis_server = redis.Redis(host='127.0.0.1', port=6379, db=0)
redis_server.config_set('maxmemory', '2225kb')

removal_policies = ["allkeys-lru","allkeys-lfu", "allkeys-random"]

for policy in removal_policies:
 redis_server.flushdb()
 redis_server.config_set("maxmemory-policy", policy)
 time.sleep(5)
 for i in range(11):
    Run_Test(policy)
    print("Test",policy, i + 1, "completado 👌")
    time.sleep(20)