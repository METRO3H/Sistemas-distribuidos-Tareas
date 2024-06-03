# Tarea 2 Sistemas Distribuidos

## Ejecución de instancias
Para poder ejecutar los contenedores que fueron descargados gracias al paso anterior, se debe hacer lo siguiente en la carpeta raíz del proyecto:
```
docker compose up -d
```

Para así poder iniciar los contenedores deseados, se pueden ejecutar los 3 compose al mismo tiempo.

## Acceso a los contenedores

Para acceder al contenedor para la ejecución correcta de los datos:

### Para kafka
```
docker exec -it kafka bash
```

### Para los producers

```
docker exec -it producer_kafka2 bash
```

### Para los consumer

```
docker exec -it consumer_kafka bash
```

### Para el acceso a la base de datos

```
docker exec -it db bash
```

## Ejecución del programa

Cabe señalar que lo primero que se tiene que hacer es crear los tópicos en la red de Apache Kafka

### Crear tópicos
Dentro del contendor de Kafka se deben poner los siguientes comandos
```
chmod +x init.sh && ./init.sh
```

### Iniciar los datos de los productores
Dentro del contenedor de los producers se debe poner el siguiente comando
```
python producers.py
```
### Iniciar el consumo de mensajes de los consumidores
Dentro del contenedor de los consumers se debe poner el siguiente comando
```
python consumers.py
```

### Acceder a la base de datos
```
psql -U postgres -d proyecto
```
