from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from app.client import urls as client_urls
from app.dashbboard import urls as ds_urls

urlpatterns = [
    path('dashboard/',include(ds_urls)),
    path('client/',include(client_urls))
]
urlpatterns += staticfiles_urlpatterns()