# apisita_mamalona_app/middleware.py

class TrimStringsMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            if hasattr(request, 'POST'):
                request.POST._mutable = True
                for key, value in request.POST.items():
                    if isinstance(value, str):
                        request.POST[key] = value.strip()
                request.POST._mutable = False
        return self.get_response(request)


class ConvertEmptyStringsToNoneMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            if hasattr(request, 'POST'):
                request.POST._mutable = True
                for key, value in request.POST.items():
                    if value == '':
                        request.POST[key] = None
                request.POST._mutable = False
        return self.get_response(request)