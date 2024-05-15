import matplotlib.pyplot as plt
import numpy as np

# Datos para la gráfica
grupos = ['Centralizado', 'Particionado', 'Replicas']
items = ['LRU', 'LFU', 'Random']
tiempos = [10, 20, 30,  # Tiempos para LRU en cada grupo
           15, 25, 35,  # Tiempos para LFU en cada grupo
           12, 22, 32]  # Tiempos para Random en cada grupo

# Configuración de la gráfica
bar_width = 0.2
space_width = 0.05  # Espacio entre cada item
index = np.arange(len(grupos))

# Crear las barras para cada item en cada grupo
for i, item in enumerate(items):
    bars = plt.bar([x + i * (bar_width + space_width) for x in index], tiempos[i::len(items)], bar_width, label=item)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

# Configuración del eje Y
plt.yticks(np.arange(min(tiempos), max(tiempos)+1, 1))  # Establecer los límites y el intervalo del eje Y
plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))  # Formato de cadena para mostrar tres decimales en el eje Y

# Configuración de la gráfica
plt.xlabel('Grupos')
plt.ylabel('Tiempo (ms)')
plt.title('Tiempos de ejecución por grupo y algoritmo de reemplazo')
plt.xticks([i + bar_width * 1.5 - 0.1 for i in index], grupos, ha='center')  # Mover las etiquetas un poco a la izquierda
plt.legend()

# Mostrar la gráfica
plt.tight_layout()
plt.show()
