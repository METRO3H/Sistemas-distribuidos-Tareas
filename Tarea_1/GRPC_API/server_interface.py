import grpc
from concurrent import futures
from GRPC_API import fetch_pb2
from GRPC_API import fetch_pb2_grpc


class GRPC_Server:
    def __init__(self) -> None:
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=None))

    def Add_Servicer(self, Response_Function):
        class Fetch_Servicer(fetch_pb2_grpc.Fetch_Service):
            def Fetch(self, request, context):
                response = Response_Function(request.anime_id)
                anime_title = response["anime_title"]
                mode = response["mode"]
                return fetch_pb2.Fetch_Response(anime_title=anime_title, mode=mode)
            
        fetch_pb2_grpc.add_Fetch_ServiceServicer_to_server(Fetch_Servicer(), self.server)
        self.server.add_insecure_port('[::]:50051')

    def Start(self):
        self.server.start()
        self.server.wait_for_termination()

""" def GRPC_Server(Servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fetch_pb2_grpc.add_Fetch_ServiceServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination() """
