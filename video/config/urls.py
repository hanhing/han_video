from django.urls import path, include
from app.client import urls as client_urls
from app.dashbboard import urls as dashboard_urls

urlpatterns = [
    path('dashborad/',include(dashboard_urls)),
    path('client/',include(client_urls))
]
