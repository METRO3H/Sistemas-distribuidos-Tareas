import matplotlib.pyplot as plt
import numpy as np
import json

def Render_Graph(average_time_response_list):
    # Datos
    cache_types = ['Centralizado', 'Particionado', 'Replicas']
    removal_policies = ['LRU', 'LFU', "Random"]

    # Configuración de la gráfica
    bar_width = 0.2
    space_width = 0.05  # Espacio entre cada item
    index = np.arange(len(cache_types))

    # Crear las barras para cada item en cada grupo
    for i, item in enumerate(removal_policies):
        bars = plt.bar([x + i * (bar_width + space_width) for x in index], average_time_response_list[i::len(removal_policies)], bar_width, label=item)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Calcular límites y el intervalo del eje Y
    mean_response = np.mean(average_time_response_list)
    std_response = np.std(average_time_response_list)
    y_lower = max(0, mean_response - 2 * std_response)
    y_upper = mean_response + 2 * std_response

    # Configuración del eje Y
    plt.ylim(y_lower, y_upper)
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))  # Formato de cadena para mostrar tres decimales en el eje Y

    # Configuración de la gráfica
    plt.ylabel('Tiempo (ms)')
    plt.title('Tiempos de ejecución por grupo y algoritmo de reemplazo')
    plt.xticks([i + bar_width * 1.5 - 0.1 for i in index], cache_types, ha='center')  # Mover las etiquetas un poco a la izquierda
    plt.legend()

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()




def Get_Stats():
    cache_types = ["classic","partitioned", "replic"]
    average_time_response_list = []
    for cache_type in cache_types:

        file_path = f"results/{cache_type}.json"

        with open(file_path, "r") as f:
                # Carga los datos JSON
                results = json.load(f)


        time_response = {
            "allkeys-lru": {
                    "average_time_response": 0
            },
            "allkeys-lfu": {
                    "average_time_response": 0
            },
            "allkeys-random": {
                    "average_time_response": 0
            }
        }
    # Iterar sobre cada objeto en la lista
        for item in results:
            removal_policy = item.get("removal_policy")

            time_response[removal_policy]["average_time_response"] += item.get("average_time_response")


        time_response_LRU = time_response['allkeys-lru']["average_time_response"]/9
        time_response_LFU = time_response['allkeys-lfu']["average_time_response"]/9
        time_response_Random = time_response['allkeys-random']["average_time_response"]/9


        # print(classic_cache_LRU, classic_cache_LFU, classic_cache_Random)

        average_time_response_list.append(round(time_response_LRU, 3))
        average_time_response_list.append(round(time_response_LFU, 3))
        average_time_response_list.append(round(time_response_Random, 3))



    return average_time_response_list


average_time_response_list = Get_Stats()

print(average_time_response_list)

Render_Graph(average_time_response_list)