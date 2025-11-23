from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden

# Set up logging to a file
logging.basicConfig(filename='requests.log', level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access restricted to business hours (9am-6pm).")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = self.get_client_ip(request)
            now = datetime.now()
            
            if ip_address not in self.requests:
                self.requests[ip_address] = []
            
            # Remove requests older than 1 minute
            self.requests[ip_address] = [
                req_time for req_time in self.requests[ip_address]
                if now - req_time < timedelta(minutes=1)
            ]
            
            if len(self.requests[ip_address]) >= 5:
                return HttpResponseForbidden("Too many messages sent. Please wait a moment.")
            
            self.requests[ip_address].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        response = self.get_response(request)
        return response