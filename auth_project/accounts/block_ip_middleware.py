from django.http import HttpResponseForbidden

BLOCKED_IPS = ['192.168.1.100','10.0.0.50'] # LIST OF BLOCKED IPS

class BlockIPMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR') #get the client ip
        if ip in BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked")
        return self.get_response(request)