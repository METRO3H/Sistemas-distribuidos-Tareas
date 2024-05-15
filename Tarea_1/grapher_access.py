import matplotlib.pyplot as plt
import numpy as np
import json

def Render_Graph(database_accesses, cache_accesses):
    # Datos
    cache_types = ['Centralizado', 'Particionado', 'Replicas']
    colors = ['darkblue', 'green', 'purple']  # Define los colors para cada grupo
    removal_policies = ['LRU', 'LFU', "Random"]

    # Configuración de la gráfica
    barWidth = 0.25
    r1 = np.arange(len(cache_accesses))
    r2 = [x + barWidth for x in r1]

    # Creación de la gráfica
    plt.figure(figsize=(10,7))
    plt.bar(r1, database_accesses, color='blue', width=barWidth, edgecolor='black', label='Database')
    plt.bar(r2, cache_accesses, color='red', width=barWidth, edgecolor='black', label='Cache')

    # Adición de etiquetas
    xticks = plt.xticks([r + barWidth/2 for r in range(len(cache_accesses))], 
            [f'{s}' for g in cache_types for s in removal_policies])

    plt.yticks(np.arange(0, max(database_accesses)+1, 500))
    # Cambia el color de las etiquetas de los removal_policies para que coincidan con sus cache_types
    for i, label in enumerate(xticks[1]):
        label.set_color(colors[i//len(removal_policies)])

    # Adición de etiquetas de grupo
    group_labels = [f'{g}' for g in cache_types for _ in removal_policies]
    plt.gca().margins(x=0.02)
    for group in range(len(cache_types)):
        label = plt.text(group*len(removal_policies) + len(removal_policies)/2 -0.35, -0.1, group_labels[group*len(removal_policies)], ha='center', transform=plt.gca().get_xaxis_transform(), fontsize=10, weight='bold')
        label.set_color(colors[group])  # Cambia el color de las etiquetas de los cache_types

    # Adición de los valores de cada barra
    for i in range(len(database_accesses)):
        plt.text(r1[i], database_accesses[i], str(database_accesses[i]), ha = 'center', va = 'bottom', fontsize=8)
        plt.text(r2[i]+0.04, cache_accesses[i], str(cache_accesses[i]), ha = 'center', va = 'bottom', fontsize=8)

    plt.ylabel('Cantidad de Accesos')
    plt.title('Comparación de Accesos a cache o base de Datos con distintas configuraciones')

    plt.legend(loc='upper left', bbox_to_anchor=(1,1))
    plt.show()



def Get_Stats():
    cache_types = ["classic","partitioned", "replic"]

    database_accesses = []
    cache_accesses = []

    for cache_type in cache_types:

        file_path = f"results/{cache_type}.json"
        # Open the file in read mode
        try:
            # Intenta abrir el archivo en modo de lectura
            with open(file_path, "r") as f:
                # Carga los datos JSON
                results = json.load(f)
        except FileNotFoundError:
            database_accesses.append(0)
            database_accesses.append(0)
            database_accesses.append(0)

            cache_accesses.append(0)
            cache_accesses.append(0)
            cache_accesses.append(0)
            continue

        removal_policy_results = {
            "allkeys-lru": {
                "database_counter": 0,
                "cache_counter": 0,
                "item_counter":0
            },
                "allkeys-lfu": {
                "database_counter": 0,
                "cache_counter": 0,
                "item_counter":0
            },
                "allkeys-random": {
                "database_counter": 0,
                "cache_counter": 0,
                "item_counter":0
            }
        }
    # Iterar sobre cada objeto en la lista
        for item in results:
            removal_policy = item.get("removal_policy")
            database_counter = item.get("database_counter")
            cache_counter = item.get("cache_counter")

            removal_policy_results[removal_policy]["database_counter"] += database_counter
            removal_policy_results[removal_policy]["cache_counter"] += cache_counter
            removal_policy_results[removal_policy]["item_counter"] += 1


        classic_db_LRU = removal_policy_results['allkeys-lru']["database_counter"]/9
        classic_db_LFU = removal_policy_results['allkeys-lfu']["database_counter"]/9
        classic_db_Random = removal_policy_results['allkeys-random']["database_counter"]/9

        # print(classic_db_LRU, classic_db_LFU, classic_db_Random)

        classic_cache_LRU = removal_policy_results['allkeys-lru']["cache_counter"]/9
        classic_cache_LFU = removal_policy_results['allkeys-lfu']["cache_counter"]/9
        classic_cache_Random = removal_policy_results['allkeys-random']["cache_counter"]/9

        # print(classic_cache_LRU, classic_cache_LFU, classic_cache_Random)

        database_accesses.append(round(classic_db_LRU))
        database_accesses.append(round(classic_db_LFU))
        database_accesses.append(round(classic_db_Random))

        cache_accesses.append(round(classic_cache_LRU))
        cache_accesses.append(round(classic_cache_LFU))
        cache_accesses.append(round(classic_cache_Random))
    return {
        "database_accesses" : database_accesses,
        "cache_accesses" : cache_accesses
    }


stats = Get_Stats()


Render_Graph(stats["database_accesses"],stats["cache_accesses"])