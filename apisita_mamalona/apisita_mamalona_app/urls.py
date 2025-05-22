from django.urls import path, include

urlpatterns = [
    # otras urls
    path('api/', include('apisita_mamalona_app.urls')),
]