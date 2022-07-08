from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^authenticate',Authentication.as_view()),
    url(r'^send_data',Data.as_view()),
]
