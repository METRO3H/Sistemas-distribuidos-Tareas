import grpc
import GRPC_API.fetch_pb2 as fetch_pb2
import GRPC_API.fetch_pb2_grpc as fetch_pb2_grpc
import time

def Get_Anime(anime_id):
    time_error = 0
    for i in range(5):  # Número de reintentos
        try:
            with grpc.insecure_channel('localhost:50051') as channel:

                stub = fetch_pb2_grpc.Fetch_ServiceStub(channel)
                response = stub.Fetch(fetch_pb2.Fetch_Request(anime_id=str(anime_id)))
                return {                
                        "anime_title": response.anime_title,
                        "mode": response.mode,
                        "time_error": time_error
                       }
        except grpc._channel._InactiveRpcError as e:
            print(f"    Error al intentar conectar con el servidor: Intento {i+1} de 5.")
            time_error += 5
            time.sleep(5)  # Tiempo de espera antes del siguiente intento
            
    print("No se pudo establecer conexión con el servidor después de 5 intentos.")
    
    return None

