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