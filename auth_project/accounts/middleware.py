from django.http import HttpResponseForbidden
from django.utils.timezone import now

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        print(f"[{now()}] Incoming request------------->: {request.path}")
        response =self.get_response(request)
        print("hello this the loggin middlware")
        print(f"[{now()}] Response status------------->: {response.status_code}")
        return response


    # def __call__(self, request):
    #     print(f"[{now()}] Incoming request: {request.path}")
    #     response = self.get_response(request)
    #     print(f"[{now()}] Response status: {response.status_code}")
    #     return response


# '127.0.0.1'
BLOCKED_IPS = ['192.168.1.100','10.0.0.50'] # LIST OF BLOCKED IPS

class BlockIPMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR') #get the client ip
        if ip in BLOCKED_IPS:
            return  ("Your IP is blocked")
        return self.get_response(request)